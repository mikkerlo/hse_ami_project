import React from 'react';
import NavBar from './NavBar.jsx'
import {withStyles} from '@material-ui/core/styles';
import CourseList from "./CourseList";


const styles = {};

class CoursePage extends React.Component {
    render() {
        const {classes} = this.props;
        return (
            <div>
                <NavBar/>
                <CourseList/>
            </div>
        )
    }
}


export default withStyles(styles)(CoursePage);