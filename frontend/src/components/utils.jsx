import React from "react";
import {Link} from "react-router-dom";


export class LinkUndecorated extends React.Component {
    render() {
        return <Link {...this.props} style={{textDecoration: 'none'}}/>
    }
}