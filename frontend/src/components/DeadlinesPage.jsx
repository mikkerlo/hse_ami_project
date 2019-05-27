import React from 'react';
import NavBar from './NavBar.jsx'
import {AllDeadlineCardList, StudentDeadlineCardList} from "./ApiDeadlineCardList";
import TinyCourseList from "./TinyCourseList";
import {withStyles} from '@material-ui/core/styles';
import AuthenticationPage from "./AuthenticationPage";


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

class DeadlinesPage extends React.Component {
    render() {
        const {classes} = this.props;
        return (
            <div>
                <NavBar/>
                <div className={classes.main}>
                    <div className={classes.deadlineList}>
                        <AllDeadlineCardList/>
                    </div>
                    <div className={classes.sidebar}>
                        <TinyCourseList/>
                    </div>
                </div>
            </div>
        )
    }
}


export default withStyles(styles)(DeadlinesPage);