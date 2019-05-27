import React from 'react';
import {Component} from 'react';
import TextField from "@material-ui/core/TextField";
import {Button, Card, Snackbar, SnackbarContent} from "@material-ui/core";
import withStyles from "@material-ui/core/es/styles/withStyles";
import {postToApi} from "../utils";
import Cookies from "universal-cookie";
import ErrorIcon from '@material-ui/icons/Error';
import red from '@material-ui/core/colors/red';
import {Redirect} from "react-router";

const styles = {};

class Registration extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            alert: false,
            alertMessage: 'default alert',
        };
        this.SubmitHandler = this.SubmitHandler.bind(this);
    }

    SubmitHandler() {
        let body = {
            username: this.state.username,
            password: this.state.password,
        };

        postToApi('/api/auth/login/', body, request => {
            console.log(request);
            if (request.ok) {
                const cookies = new Cookies();
                cookies.set('userToken', request.result.token, {path: '/'});
                window.location = '/deadlines';
            } else {
                this.setState({
                    alert: true,
                    alertMessage: request.error,
                })
            }
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
                <Snackbar
                    anchorOrigin={{
                        vertical: 'bottom',
                        horizontal: 'left',
                    }}
                    open={this.state.alert}
                    autoHideDuration={6000}
                >
                    <SnackbarContent
                        variant="success"
                        style={{
                            backgroundColor: red[600],
                        }}
                        message={
                            <span id="client-snackbar" style={{
                                display: 'flex',
                                alignItems: 'center',
                            }}>
                            <ErrorIcon/>
                                {this.state.alertMessage}
                            </span>
                        }
                    />
                </Snackbar>
            </Card>
        );
    }
}


export default withStyles(styles)(Registration);