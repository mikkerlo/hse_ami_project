import React from 'react';
import NavBar from './NavBar.jsx';
import Login from "./Login";
import Registration from "./Register";


class AuthenticationPage extends React.Component {
    render() {
        return (
            <div>
                <NavBar/>
                <Registration/>
                <Login/>
            </div>
        )
    }
}


export default AuthenticationPage;
