import React from 'react';
import NavBar from './NavBar.jsx';
import Login from "./Login";
import Registration from "./Register";
import withStyles from "@material-ui/core/es/styles/withStyles";


const styles = {
    'login': {
        margin: '200px 30px 30px 650px',
    },
    'loginEl': {
        display: 'inline-block',
    }
};


class AuthenticationPage extends React.Component {
    render() {
        const {classes} = this.props;
        return (
            <div>
                <NavBar/>
                <div className={classes.login}>
                    <Login className={classes.loginEl}/>
                </div>
            </div>
        )
    }
}


export default withStyles(styles)(AuthenticationPage);

