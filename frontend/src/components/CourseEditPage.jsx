import React from 'react';
import NavBar from './NavBar.jsx'
import {withStyles} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import {getFromApi, patchApi, postToApi} from "../utils";
import Button from "@material-ui/core/Button";
import {Typography} from "@material-ui/core";
import {deadlineUrl, groupUrl, newGroupUrl, newDeadlineUrl} from "../apiUrls";
import CourseCard from "./CourseCard";


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
            </div>
        )
    }
}


export default withStyles(styles)(CourseEditPage);
