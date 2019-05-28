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

const styles = {
    card: {
        minWidth: 275,
        maxWidth: 800,
        boxSizing: 'inherit',
        borderRadius: 30,
        margin: '10px',
    },
    valid_until: {
        maxWidth: 300,
        marginLeft: 'auto',
        display: 'inline-block',
    },
    done: {
        display: 'inline-block',
    },
    header: {
        display: 'inline-block',
    },
    group_name: {
        display: 'inline-block',
    }
};


class DeadlineCard extends React.Component {
    render() {
        const {classes, content, header, files, valid_until, group_name, group_id, id} = this.props;
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
                <hr/>
                {files_buttons}
            </div>;
        }
        return (
            <Card className={classes.card}>
                <CardContent>
                    <div style={{display: 'flex'}}>
                        <Typography className={classes.header} variant="h5" component="h2">
                            {header}
                        </Typography>
                        <Typography className={classes.valid_until}>
                            {dateFormat(new Date(valid_until * 1000), "HH:MM hh.mm yyyy")}
                        </Typography>
                        <Link to={`/courses/${group_id}`}>
                        <Typography  className={classes.group_name}>
                            {group_name}
                        </Typography>
                        </Link>
                        {/*<Typography className={classes.done}>*/}
                        {/*    <Checkbox checked={is_done} enabled={"false"}/>*/}
                        {/*    Done*/}
                        {/*</Typography>*/}
                        <Button onClick={() => window.location = '/deadline/'+ id + '/edit'}>
                        <EditIcon/>
                        </Button>
                    </div>
                    <hr style={{clear: 'both'}}/>
                    <Typography component="p">
                        {content}
                        <br/>
                    </Typography>
                    {files_buttons}
                </CardContent>
            </Card>
        );
    }
}

DeadlineCard.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DeadlineCard);
