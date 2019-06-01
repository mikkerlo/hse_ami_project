import React from 'react';
import NavBar from './NavBar.jsx'
import {withStyles} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import {deleteApi, getFromApi, patchApi, PERMISSIONS, postToApi} from "../utils";
import Button from "@material-ui/core/Button";
import {Typography} from "@material-ui/core";
import {
    groupUrl,
    newGroupUrl,
    groupTokenUrl,
    groupStudentsUrl,
    addModeratorUrl, removeModeratorUrl
} from "../apiUrls";
import CourseCard from "./CourseCard";
import {InviteLink} from "./utils";


import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Checkbox from '@material-ui/core/Checkbox';


const useStylesForTable = () => {
    return {
        root: {
            width: '100%',
            marginTop: 15,
            overflowX: 'auto',
        }
        ,
        table: {
            minWidth: 650,
        }
        ,
    }
};

class StudentTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            students: [],
        };
        this.fetchData();
    }

    fetchData() {
        getFromApi(groupStudentsUrl(this.props.group_id), (err, result) => {
            console.log(result);
            if (!err) {
                this.setState({
                    students: result
                });
            }
        })
    }

    getUpdatePermissionHandler(student_index) {
        return function updatePermissionHandler(event) {

            let isChecked = event.target.checked;
            let url = isChecked ? addModeratorUrl(this.props.group_id) : removeModeratorUrl(this.props.group_id);
            postToApi(url, {student_id: this.state.students[student_index].id}, response => {
                if (response.ok) {
                    this.setState(prevState => {
                        prevState.students[student_index].permission = isChecked ? PERMISSIONS.EDITING : PERMISSIONS.READING;
                        return prevState;
                    });
                }
            });
        }.bind(this);
    }

    render() {
        const classes = useStylesForTable();
        return (
            <Paper className={classes.root}>
                <Table className={classes.table}>
                    <TableHead>
                        <TableRow>
                            <TableCell>Модератор</TableCell>
                            <TableCell>Имя</TableCell>
                            <TableCell>Фамилия</TableCell>
                            <TableCell>Отчество</TableCell>
                            <TableCell>Почта</TableCell>
                            <TableCell>Телеграм</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {this.state.students.map((student, index) => (
                            <TableRow key={student.id}>
                                <TableCell>
                                    {student.permission === PERMISSIONS.CREATOR ? "Создатель" :
                                        <Checkbox
                                            checked={student.permission >= PERMISSIONS.EDITING}
                                            onChange={this.getUpdatePermissionHandler(index)}
                                            disabled={(student.permission === PERMISSIONS.CREATOR)}
                                        />
                                    }
                                </TableCell>
                                <TableCell>{student.name.first_name}</TableCell>
                                <TableCell>{student.name.last_name || '-'}</TableCell>
                                <TableCell>{student.name.patronymic_name || '-'}</TableCell>
                                <TableCell>{student.email || '-'}</TableCell>
                                <TableCell>{student.telegram_account || '-'}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>
        );
    }
}


const styles = {
    sidebar: {
        width: '20%',
        float: 'right',
        paddingTop: 20,
        boxSizing: 'border-box',
    },
    deadlineList: {
        width: '80%',
        float: 'left',
        paddingRight: 10,
        boxSizing: 'border-box'
    },
    main: {
        marginRight: 'auto',
        marginLeft: 'auto',
        maxWidth: 1000

    },
    formControl: {
        margin: 5,
        minWidth: 120,
    },
    editControls: {
        display: 'inline-block',
        width: 'auto',
        margin: "1em",
    }
};


class CourseEditPage extends React.Component {
    constructor(props) {
        super(props);
        this.init(props);
        this.handleDescriptionChange = this.handleDescriptionChange.bind(this);
        this.handleFullNameChange = this.handleFullNameChange.bind(this);
        this.handleSave = this.handleSave.bind(this);
        this.createInviteToken = this.createInviteToken.bind(this);
        this.deleteInviteToken = this.deleteInviteToken.bind(this);
    }

    init(props) {
        this.state = {
            group: {
                id: 0,
                full_name: 'loading',
                short_name: 'loading',
                description: 'loading',
                is_hidden: false,
            },
            isNew: true,
            inviteToken: null,
        };
        if (props.match && props.match.params.number) {
            this.state.isNew = false;
            this.state.group.id = Number(props.match.params.number);
            this.fetchData();
        }

    }

    fetchData() {
        getFromApi(groupUrl(this.state.group.id), function (err, res) {
            if (err) {
                console.log('error occurred');
                alert('group not found; creating new deadline');
                this.setState({isNew: true});
            } else {
                this.setState({
                    group: res,
                });

            }
        }.bind(this));
        getFromApi(groupTokenUrl(this.state.group.id), (err, result) => {
            if (!err) {
                this.setState({
                    inviteToken: result.token
                })
            }
        });
    }

    componentWillReceiveProps(nextProps, nextContext) {
        this.init(nextProps);
    }

    handleDescriptionChange(event) {
        let newText = event.target.value;
        this.setState(prevState => {
            prevState.group.description = newText;
            return prevState;
        });
    }

    createInviteToken() {
        postToApi(groupTokenUrl(this.state.group.id), '', response => {
            if (response.ok) {
                this.setState({
                    inviteToken: response.result.token
                });
            }
        });
    }

    deleteInviteToken() {
        deleteApi(groupTokenUrl(this.state.group.id), '', response => {
            if (response.ok) {
                this.setState({
                    inviteToken: null
                });
            }
        });
    }

    handleFullNameChange(event) {
        let newCaption = event.target.value;
        this.setState(prevState => {
            prevState.group.full_name = newCaption;
            prevState.group.short_name = newCaption;
            return prevState
        });
    }

    handleSave(event) {
        let body = {
            ...this.state.group,
        };
        if (this.state.isNew) {
            postToApi(newGroupUrl(), body, response => {
            });
        } else {
            patchApi(groupUrl(this.state.group.id), body, response => {
            });
        }

    }


    render() {
        const {classes} = this.props;
        return (
            <div>
                <NavBar/>
                <div>
                    <Typography className={classes.editControls} noWrap>Название курса: </Typography>
                    <Input
                        multiline={false}
                        value={this.state.group.full_name}
                        onChange={this.handleFullNameChange}
                        className={classes.editControls}
                    />
                </div>
                <div>
                    <Typography className={classes.editControls} noWrap>Описание: </Typography>
                    <Input
                        multiline={true}
                        value={this.state.group.description}
                        onChange={this.handleDescriptionChange}
                        className={classes.editControls}
                    />
                </div>

                <CourseCard {...this.state.group}/>
                <Button
                    color='primary'
                    variant='contained'
                    onClick={this.handleSave}
                >
                    {this.state.isNew ? 'Создать' : 'Сохранить'}
                </Button>
                <p/>
                {
                    this.state.isNew ?
                        <div/>
                        :
                        this.state.inviteToken ?
                            <div>
                                <InviteLink
                                    inviteToken={this.state.inviteToken}
                                    full_name={this.state.group.full_name}
                                />
                                <Button
                                    onClick={this.deleteInviteToken}
                                >
                                    {'Удалить инвайт-токен'}
                                </Button>
                            </div>
                            :
                            <Button
                                onClick={this.createInviteToken}
                            >
                                {'Создать инвайт-токен'}
                            </Button>
                }
                <p/>
                {this.state.isNew ?
                    <div/>
                    :
                    <StudentTable
                        group_id={this.state.group.id}
                    />
                }
            </div>
        )
    }
}


export default withStyles(styles)(CourseEditPage);
