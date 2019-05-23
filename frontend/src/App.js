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


class App extends React.Component {
    render() {
        return (
            <BrowserRouter>
                <>
                    <Switch>
                        <Route
                            path='/deadlines' component={DeadlinesPage}/>
                        <Route
                            path='/exp' component={Exp}/>
                        <Route
                            path='/deadline/:number/edit' component={DeadlineEditPage}/>
                        <Route path='/courses/:number' component={CoursePage}/>
                        <Route
                            path='/'
                            component={SimplePage}/>
                    </Switch>
                </>
            </BrowserRouter>
        );
    }
}

export default App;
