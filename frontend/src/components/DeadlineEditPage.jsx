import React from 'react';
import NavBar from './NavBar.jsx'
import {AllDeadlineCardList} from "./ApiDeadlineCardList";
import TinyCourseList from "./TinyCourseList";
import DeadlineCard from './DeadlineCard';
import {withStyles} from '@material-ui/core/styles';
import Input from '@material-ui/core/Input';


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

    }
};

class NameForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {value: ''};

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(event) {
        console.log('update' + event.target.value);
        this.setState({value: event.target.value + 'kek'});
    }

    handleSubmit(event) {
        alert('A name was submitted: ' + this.state.value);
        event.preventDefault();
    }

    render() {
        return (
            <form onSubmit={this.handleSubmit}>
                <label>
                    Name:
                    <input type="text" value={this.state.value} onChange={this.handleChange}/>
                </label>
                <input type="submit" value="Submit"/>
            </form>
        );
    }
}


class DeadlineEditPage extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            deadlineText: 'loading',
            deadlineCaption: 'loading',
            deadlineFiles: [],
            deadlineDate: 0,
            deadlineIs_done: false,
        };
        this.handleTextChange = this.handleTextChange.bind(this);
    }

    handleTextChange(event) {
        console.log('update ' + event.target.value);
        console.log(this.state);
        this.setState({deadlineText: event.target.value});
    }

    renderDeadlineCard(props) {
        console.log(this.state);
        return <DeadlineCard
            text={this.state.deadlineText}
            caption={this.state.deadlineCaption}
            files={this.state.deadlineFiles}
            date={this.state.deadlineDate}
            is_done={this.state.deadlineIs_done}
        />
    }


    render() {
        const {classes} = this.props;
        console.log(this.state);
        return (
            <div>
                <NavBar/>
                <Input multiline={"true"} value={this.state.deadlineText} onChange={this.handleTextChange}/>
                {/*<DeadlineCard {...this.state.deadline}/>*/}
                {this.renderDeadlineCard()}
                <NameForm/>
            </div>
        )
    }
}


export default withStyles(styles)(DeadlineEditPage);