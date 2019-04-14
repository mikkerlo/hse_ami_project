import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import NavBar from './components/NavBar.jsx'


class App extends Component {
  render() {
    return (
        <>
        <NavBar />
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
        </header>
      </div>
        </>
    );
  }
}

export default App;
