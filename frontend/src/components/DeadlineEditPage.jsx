import React from 'react';
import NavBar from './NavBar.jsx'
import DeadlineCard from './DeadlineCard';
import {withStyles} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import TextField from "@material-ui/core/TextField";
import FormControl from "@material-ui/core/FormControl";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import {getFromApi, patchApi, postToApi} from "../utils";
import Button from "@material-ui/core/Button";
import FormHelperText from "@material-ui/core/FormHelperText";
import {Typography} from "@material-ui/core";


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

class CourseSelector extends React.Component {
    constructor(props) {
        super(props);
        this.classes = props.classes;
        this.state = {courses: []};
    }

    fetchData() {
        getFromApi('/api/groups/all', function (err, res) {
            if (!err) {
                this.setState({courses: res});
            }
        }.bind(this));
    }

    componentDidMount() {
        this.fetchData();
    }

    render() {
        const {handleChange, classes, group_name} = this.props;
        let group_obj;
        for (let i = 0; i < this.state.courses.length; ++i) {
            if (this.state.courses[i].full_name === group_name) {
                group_obj = this.state.courses[i];
            }
        }
        return <div>
            <FormControl className={classes.formControl}>
                <Select
                    value={group_obj}
                    onChange={handleChange}
                    inputProps={{
                        name: 'course',
                        id: 'course-id',
                    }}
                >
                    {this.state.courses.map(course => (
                        <MenuItem value={course}>{course.full_name}</MenuItem>
                    ))}
                </Select>
                <FormHelperText>Группа</FormHelperText>
            </FormControl>
        </div>;
    }
}

class DeadlineEditPage extends React.Component {
    constructor(props) {
        super(props);
        this.init(props);
        this.handleTextChange = this.handleTextChange.bind(this);
        this.handleCaptionChange = this.handleCaptionChange.bind(this);
        this.handleDeadlineDateChange = this.handleDeadlineDateChange.bind(this);
        this.handleCourseChange = this.handleCourseChange.bind(this);
        this.handleSave = this.handleSave.bind(this);
    }

    init(props) {
        this.state = {
            deadline: {
                id: 0,
                group_id: 0,
                group_name: 'loading',
                text: 'loading',
                caption: 'loading',
                files: [],
                date: 0,
                is_done: false,
            },
            isNew: true,
            timeText: "2019-01-01T00:00",
        };
        if (props.match && props.match.params.number) {

            this.state.isNew = false;
            this.state.deadline.id = Number(props.match.params.number);
            this.fetchData();
        }

    }

    fetchData() {
        getFromApi('/api/deadlines/' + this.state.deadline.id + '/', function (err, res) {
            if (err) {
                console.log('error occurred');
                alert('deadline not found; creating new deadline');
                this.setState({isNew: true});
            } else {
                let dateIsoStr = (new Date(res.valid_until * 1000)).toISOString();
                this.setState({
                    deadline: {
                        id: res.id,
                        group_id: res.group_id,
                        group_name: res.group_name,
                        text: res.content,
                        caption: res.header,
                        files: [],
                        date: res.valid_until,
                        is_done: false,
                    },
                    timeText: dateIsoStr.split('.')[0]
                });

            }
        }.bind(this));
    }

    componentWillReceiveProps(nextProps, nextContext) {
        this.init(nextProps);
    }

    handleTextChange(event) {
        let newText = event.target.value;
        this.setState(prevState => {
            prevState.deadline.text = newText;
            return prevState;
        });
    }

    handleCaptionChange(event) {
        let newCaption = event.target.value;
        this.setState(prevState => {
            prevState.deadline.caption = newCaption;
            return prevState;
        });
    }

    handleCourseChange(event) {
        let newCourse = event.target.value;
        this.setState(prevState => {
            prevState.deadline.group_name = newCourse.full_name;
            prevState.deadline.group_id = newCourse.id;
            return prevState;
        });
    }

    handleDeadlineDateChange(event) {
        let text = event.target.value;
        let newDate = new Date(event.target.value).getTime() / 1000;
        this.setState(prevState => {
            prevState.deadline.date = newDate;
            prevState.timeText = text;
            return prevState;
        });
    }

    handleSave(event) {
        let body = {
            id: this.state.deadline.id,
            group_id: this.state.deadline.group_id,
            group_name: this.state.deadline.group_name,
            valid_until: this.state.deadline.date,
            header: this.state.deadline.caption,
            content: this.state.deadline.text,
            created_at: this.state.deadline.date, // temporary until backend fix it
        };
        if (this.state.isNew) {
            postToApi('/api/deadlines/new/', body, response => {
            });
        } else {
            patchApi('/api/deadlines/' + this.state.deadline.id + '/', body, response => {
            });
        }

    }


    render() {
        const {classes} = this.props;
        return (
            <div>
                <NavBar/>
                <div>
                    <Typography className={classes.editControls} noWrap>Описание дедлайна: </Typography>
                    <Input
                        multiline={true}
                        value={this.state.deadline.text}
                        onChange={this.handleTextChange}
                        className={classes.editControls}
                    />
                </div>
                <div>
                    <Typography className={classes.editControls} noWrap>Текст дедлайна: </Typography>
                    <Input
                        multiline={true}
                        value={this.state.deadline.caption}
                        onChange={this.handleCaptionChange}
                        className={classes.editControls}
                    />
                </div>

                <form className={classes.container} noValidate>
                    <div>
                        <Typography className={classes.editControls} noWrap>Дата дедлайна: </Typography>
                        <TextField
                            id="deadline-date"
                            label="Дедлайн"
                            type="datetime-local"
                            value={this.state.timeText}
                            InputLabelProps={{
                                shrink: true,
                            }}
                            onChange={this.handleDeadlineDateChange}
                            className={classes.editControls}
                        />
                    </div>
                </form>
                {this.state.isNew ? <CourseSelector
                    hidden={this.state.isNew}
                    handleChange={this.handleCourseChange}
                    classes={classes}
                    group_name={this.state.deadline.group_name}
                /> : null
                }

                <DeadlineCard {...this.state.deadline}/>
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


export default withStyles(styles)(DeadlineEditPage);
