import React from "react";
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import EditIcon from '@material-ui/icons/Edit';
import Typography from '@material-ui/core/Typography';
import AttachmentIcon from '@material-ui/icons/AttachFile';
import Checkbox from '@material-ui/core/Checkbox';
import Link from "@material-ui/core/Link";
import dateFormat from 'dateformat';
import {LinkUndecorated} from "./utils";
import {PERMISSIONS} from "../utils";
import {Divider, ListItemText, MenuItem} from "@material-ui/core";
import List from "@material-ui/core/List";

const styles = {
    card: {
        minWidth: 275,
        maxWidth: 800,
        borderRadius: 30,
        margin: '10px',
    },
    valid_until: {
        maxWidth: 300,
        marginLeft: 'auto',
    },
    done: {
    },
    header: {
        boxSizing: 'border-box',
        borderBottom: '2px solid #efefef',
        padding: 10,
    },
    filesPanel: {
        float: 'right',
        width: '100%',
        // display: 'inline-block',
        boxSizing: 'border-box',
        borderTop: '2px solid #efefef',
        // padding: 10,
    },
    group_name: {
    },
    leftInfo: {
        float: 'left',
        width: 'auto',
        boxSizing: 'border-box',
        // borderRight: '2px solid #efefef',
    },
    rightInfo: {
        float: 'right',
        width: '70%',
        height: '100%',
        // borderLeft: '2px solid #efefef',
        display: 'inline-block',
        boxSizing: 'border-box',
    },
};


class DeadlineCard extends React.Component {
    render() {
        const {classes, content, header, files, valid_until, group_name, group_id, id, permission, is_done} = this.props;
        let files_buttons = <div>
            {files.map(file => (
                <Button
                    variant="contained"
                    style={{margin: '10px'}}
                    key={file.id}
                    onClick={() => window.location = file.url}
                >
                    <AttachmentIcon/>
                    {file.name}
                </Button>
            ))
            }
        </div>;
        if (files.length > 0) {
            files_buttons = <div>
                {files_buttons}
            </div>;
        }
        return (
            <Card className={classes.card}>
                <CardContent>
                    <div className={classes.header}>
                        <Typography variant={"h6"}>
                            {header}
                        </Typography>
                    </div>
                    <div className={classes.leftInfo}>


                        <LinkUndecorated to={`/courses/${group_id}`}>
                            <Typography variant={"h7"}>
                                {group_name}
                            </Typography>
                        </LinkUndecorated>
                        <p/>
                        <Typography className={classes.valid_until}>
                            {dateFormat(new Date(valid_until * 1000), "HH:MM hh.mm yyyy")}
                        </Typography>
                        <Checkbox checked={is_done} enabled={"false"}/>
                        {
                            permission >= PERMISSIONS.EDITING
                                ?
                                <Button onClick={() => window.location = '/deadline/' + id + '/edit'}>
                                    <EditIcon/>
                                </Button>
                                :
                                <div/>
                        }

                    </div>
                    <div className={classes.rightInfo}>
                        <Typography component="p">
                            {content}
                            <br/>
                        </Typography>
                    </div>
                    <div className={classes.filesPanel}>
                        {files_buttons}
                    </div>
                </CardContent>
            </Card>
        );
    }
}

DeadlineCard.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DeadlineCard);
