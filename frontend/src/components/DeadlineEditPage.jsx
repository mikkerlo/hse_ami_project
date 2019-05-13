import React from 'react';
import NavBar from './NavBar.jsx'
import DeadlineCard from './DeadlineCard';
import {withStyles} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';
import TextField from "@material-ui/core/TextField";
import FormControl from "@material-ui/core/FormControl";
import InputLabel from "@material-ui/core/InputLabel";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import {getFromApi, postToApi} from "../utils";
import Button from "@material-ui/core/Button";


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
};

class CourseSelector extends React.Component {
    constructor(props) {
        super(props);
        this.classes = props.classes;
        this.state = {courses: []};
    }

    fetchData() {
        getFromApi('/api/groups/all', function (err, res) {
            if (err) {
                console.log('error occurred');
            } else {
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
                <InputLabel>Группа</InputLabel>
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
            </FormControl>
        </div>;
    }
}

class DeadlineEditPage extends React.Component {
    constructor(props) {
        super(props);
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
            }
        };
        this.handleTextChange = this.handleTextChange.bind(this);
        this.handleCaptionChange = this.handleCaptionChange.bind(this);
        this.handleDeadlineDateChange = this.handleDeadlineDateChange.bind(this);
        this.handleCourseChange = this.handleCourseChange.bind(this);
        this.handleSave = this.handleSave.bind(this);
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
        let newDate = new Date(event.target.value).getTime() / 1000;
        console.log(event.target.value);
        console.log(newDate);
        this.setState(prevState => {
            prevState.deadline.valid_until = newDate;
            return prevState;
        });
    }

    handleSave(event) {
        console.log(event);
        let body = {
            id: this.state.deadline.id,
            group_id: this.state.deadline.group_id,
            group_name: this.state.deadline.group_name,
            valid_until: this.state.deadline.date,
            header: this.state.deadline.caption,
            content: this.state.deadline.text,
            created_at: this.state.deadline.date, // temporary until backend fix it
        };
        postToApi('/api/deadlines/new/', body, response => {
            console.log(response);
        })

    }


    render() {
        const {classes} = this.props;
        console.log(this.state);
        return (
            <div>
                <NavBar/>
                <Input multiline={"true"} value={this.state.deadline.text} onChange={this.handleTextChange}/>
                <p/>
                <Input value={this.state.deadline.caption} onChange={this.handleCaptionChange}/>
                <p/>
                <form className={classes.container} noValidate>
                    <TextField
                        id="deadline-date"
                        label="Дедлайн"
                        type="datetime-local"
                        defaultValue="2017-05-24T10:30"
                        InputLabelProps={{
                            shrink: true,
                        }}
                        onChange={this.handleDeadlineDateChange}
                    />
                </form>
                <p/>
                <CourseSelector
                    handleChange={this.handleCourseChange}
                    classes={classes}
                    group_name={this.state.deadline.group_name}
                />
                <DeadlineCard {...this.state.deadline}/>
                <Button
                    color='primary'
                    variant='contained'
                    onClick={this.handleSave}
                    >
                    Save
                </Button>
            </div>
        )
    }
}


export default withStyles(styles)(DeadlineEditPage);