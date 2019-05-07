import React from 'react';
import NavBar from './NavBar.jsx'
import DeadlineCardList from "./DeadlineCardList";
import TinyCourseList from "./TinyCourseList";
import {withStyles} from '@material-ui/core/styles';
import CourseCard from './CourseCard';
import ApiCourseCard from "./ApiCourseCard";


const styles = {
    sidebar: {
        width: '20%',
        float: 'right',
        paddingTop: 20,
        boxSizing: 'border-box',
    },
    courseDescription: {
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

class CoursePage extends React.Component {
    render() {
        const {classes} = this.props;
        const apiID = Number(this.props.match.params.number);
        return (
            <div>
                <NavBar/>
                <div className={classes.main}>
                    <div className={classes.courseDescription}>
                        <ApiCourseCard
                        apiID={apiID}/>
                    </div>
                    <div className={classes.sidebar}>
                        <TinyCourseList/>
                    </div>
                </div>
            </div>
        )
    }
}


export default withStyles(styles)(CoursePage);