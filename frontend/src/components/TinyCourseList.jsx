import React from "react";
import {getFromApi} from "../utils";
import {withStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';
import Card from '@material-ui/core/Card';
import {LinkUndecorated} from "./utils";
import {studentGroupsUrl} from "../apiUrls";


const styles = theme => ({
    root: {
        width: '100%',
        maxWidth: 360,
        backgroundColor: theme.palette.background.paper,
    },
});


class TinyCourseList extends React.Component {
    constructor(props) {
        super(props);
        this.classes = props.classes;
        this.state = {courses: []};
    }

    fetchData() {
        getFromApi(studentGroupsUrl(), function (err, res) {
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
        return <Card className={this.classes.root}>
            <List component="nav">
                {this.state.courses.map(course => (
                    <LinkUndecorated to={"/courses/" + course.id} key={course.id}>
                        <ListItem button divider>
                            <ListItemText primary={course.full_name}/>
                        </ListItem>
                    </LinkUndecorated>
                ))}
            </List>

        </Card>;
    }
}

export default withStyles(styles)(TinyCourseList);
