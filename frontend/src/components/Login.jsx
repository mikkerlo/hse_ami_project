import React from 'react';
import {Component} from 'react';
import TextField from "@material-ui/core/TextField";
import {Button, Card} from "@material-ui/core";
import withStyles from "@material-ui/core/es/styles/withStyles";
import {postToApi} from "../utils";
import Cookies from "universal-cookie";


const styles = {};

class Registration extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
        };
        this.SubmitHandler = this.SubmitHandler.bind(this);
    }

    SubmitHandler() {
        postToApi('/api/auth/login/', this.state, request => {
            console.log(request);
            const cookies = new Cookies();
            cookies.set('userToken', request.result.token, {path: '/'});
            window.location = '/';
        });
    }

    render() {
        return (
            <Card style={{width: '300px'}}>
                <div style={{padding: '0px 0px 0px 80px'}}>
                    <TextField
                        id="login"
                        label="Имя пользователя"
                        defaultValue=""
                        margin="normal"
                        value={this.state.username}
                        onChange={event => this.setState({username: event.target.value})}
                    />

                    <TextField
                        type='password'
                        id="password"
                        label="Пароль"
                        defaultValue=""
                        margin="normal"
                        value={this.state.password}
                        onChange={event => this.setState({password: event.target.value})}
                    />
                </div>
                <div style={{padding: '10px 0px 10px 80px'}}>
                    <Button
                        color='primary'
                        variant='contained'
                        onClick={this.SubmitHandler}
                    >
                        Войти
                    </Button>
                </div>
            </Card>
        );
    }
}


export default withStyles(styles)(Registration);