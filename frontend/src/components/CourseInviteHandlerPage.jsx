import React from 'react';
import NavBar from './NavBar.jsx'
import {withStyles} from '@material-ui/core/styles';
import CourseList from "./CourseList";
import {postToApi} from "../utils";
import {applyInviteUrl} from "../apiUrls";
import {Redirect} from "react-router";


const styles = {};

class CourseInviteHandlerPage extends React.Component {
    constructor(props) {
        super(props);
        this.processInvite(props.match.params.token);
        this.state = {
            status: 'processing',
            group: null,
        }
    }

    processInvite(token) {
        postToApi(applyInviteUrl(), {token: token}, response => {
            if (response.ok) {
                this.setState({
                    status: 'ok',
                    group: response.result,
                });
            } else {
                this.setState({status: 'fail'});
            }
        })
    }

    render() {
        const {classes} = this.props;
        return (
            <div>
                <NavBar/>
                {this.state.status}
                {this.state.status === 'ok' ?
                    <Redirect to={`/courses/${this.state.group.id}`}/>
                    :
                    <div/>
                }
            </div>
        )
    }
}


export default withStyles(styles)(CourseInviteHandlerPage);