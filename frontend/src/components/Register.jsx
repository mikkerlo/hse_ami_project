import React from 'react';
import {Component} from 'react';
import TextField from "@material-ui/core/TextField";
import {Button, Card} from "@material-ui/core";
import withStyles from "@material-ui/core/es/styles/withStyles";
import {postToApi} from "../utils";


const styles = {};

class Registration extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            name: {
                first_name: '',
                last_name: '',
                patronymic_name: '',
            },
            email: '',
        };
        this.SubmitHandler = this.SubmitHandler.bind(this);
    }

    SubmitHandler() {
        postToApi('/api/students/new/', this.state, request => {
            if (!request.ok) {
                alert(request.error);
                console.log(request.error);
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
                        id="first_name"
                        label="Фамилия"
                        defaultValue=""
                        margin="normal"
                        value={this.state.name.first_name}
                        onChange={event => {
                            let newValue = event.target.value;
                            this.setState(prevState => {
                                prevState.name.first_name = newValue;
                                return prevState;
                            });
                        }}
                    />
                    <TextField
                        id="last_name"
                        label="Имя"
                        defaultValue=""
                        margin="normal"
                        value={this.state.name.last_name}
                        onChange={event => {
                            let newValue = event.target.value;
                            this.setState(prevState => {
                                prevState.name.last_name = newValue;
                                return prevState;
                            });
                        }}
                    />
                    <TextField
                        id="patronymic_name"
                        label="Отчество"
                        defaultValue=""
                        value={this.state.name.patronymic_name}
                        onChange={event => {
                            let newValue = event.target.value;
                            this.setState(prevState => {
                                prevState.name.patronymic_name = newValue;
                                return prevState;
                            });
                        }}
                    />
                    <TextField
                        id="login"
                        label="email"
                        defaultValue=""
                        margin="normal"
                        value={this.state.email}
                        onChange={event => this.setState({email: event.target.value})}
                    />
                    <TextField
                        type='password'
                        id="password"
                        label="Password"
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
                        Зарегистрироваться
                    </Button>
                </div>
            </Card>
        );
    }
}


export default withStyles(styles)(Registration);
