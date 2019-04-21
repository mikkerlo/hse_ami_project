import React, {Component} from 'react';
import BrowserRouter from 'react-router-dom/BrowserRouter';
import Route from 'react-router-dom/Route';
import Exp from './exp';

import logo from './logo.svg';
import './App.css';
import NavBar from './components/NavBar.jsx'
import {Switch} from "react-router";


class SimplePage extends Component {
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
                            path='/exp' component={Exp}/>
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
