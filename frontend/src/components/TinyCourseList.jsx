import React from "react";
import {getFromApi} from "../utils";
import {withStyles} from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';


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
        this.update();
    }

    update() {
        getFromApi('/api/groups/all', function (err, res) {
            if (err) {
                console.log('error occurred');
            } else {
                this.setState({courses: res});
            }
        }.bind(this));
    }

    render() {
        return <div className={this.classes.root}>
            <List component="nav">
                {this.state.courses.map(course => (
                    <ListItem button>
                        <ListItemText primary={course.full_name}/>
                    </ListItem>
                ))}
            </List>

        </div>;
    }
}

export default withStyles(styles)(TinyCourseList);
