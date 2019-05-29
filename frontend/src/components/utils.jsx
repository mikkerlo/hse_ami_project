import React from "react";
import {Link} from "react-router-dom";
import {Button} from "@material-ui/core";


export class LinkUndecorated extends React.Component {
    render() {
        return <Link {...this.props} style={{textDecoration: 'none'}}/>
    }
}


export class InviteLink extends React.Component {
    render() {
        return <LinkUndecorated to={"/j/" + this.props.inviteToken}>
            <Button>
                {`Присоединиться к "${this.props.full_name}"`}
            </Button>
        </LinkUndecorated>
    }
}