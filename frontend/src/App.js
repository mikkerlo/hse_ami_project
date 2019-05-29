import React from 'react';
import {BrowserRouter} from 'react-router-dom';
import {Route} from 'react-router-dom';
import Exp from './exp';
import DeadlinesPage from './components/DeadlinesPage.jsx'

import logo from './logo.svg';
import './App.css';
import NavBar from './components/NavBar.jsx'
import {Switch} from "react-router";
import CoursePage from "./components/CoursePage";
import DeadlineEditPage from "./components/DeadlineEditPage";
import Cookies from "universal-cookie";
import AuthenticationPage from "./components/AuthenticationPage";
import CourseListPage from "./components/CourseListPage";
import CourseEditPage from "./components/CourseEditPage";
import CourseInviteHandlerPage from "./components/CourseInviteHandlerPage";


class SimplePage extends React.Component {
    render() {
        return (
            <div className="App">
                <NavBar/>
                <header className="App-header">
                    <img src={logo} className="App-logo" alt="logo"/>
                </header>
            </div>
        );
    }
}


class HandleLogin extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const cookie = new Cookies();
        let token = cookie.get('userToken');
        if (token) {
            return this.props.logged;
        } else {
            return this.props.unlogged;
        }
    }
}

class App extends React.Component {
    render() {
        return (
            <BrowserRouter>
                <>
                    <HandleLogin
                        unlogged={<AuthenticationPage/>}
                        logged={
                            <Switch>
                                <Route
                                    path='/deadlines' component={DeadlinesPage}/>
                                <Route
                                    path='/exp' component={Exp}/>
                                <Route
                                    path='/handleGroupInvite/:token' component={CourseInviteHandlerPage}/>
                                <Route
                                    path='/deadline/:number/edit' component={DeadlineEditPage}/>
                                <Route
                                    path='/deadline/new' component={DeadlineEditPage}/>
                                <Route
                                    path='/courses/new' component={CourseEditPage}/>
                                <Route
                                path='/courses/:number/edit' component={CourseEditPage}/>
                                <Route path='/courses/:number' component={CoursePage}/>
                                <Route path='/courses' component={CourseListPage}/>


                                <Route
                                    path='/'
                                    component={SimplePage}/>
                            </Switch>
                        }
                    />

                </>
            </BrowserRouter>
        );
    }
}

export default App;
