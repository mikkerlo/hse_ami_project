import React from "react";
import PropTypes from 'prop-types';
import {withStyles} from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import DeleteIcon from '@material-ui/icons/Delete';


const styles = {
    card: {
        minWidth: 275,
        maxWidth: 600,
        boxSizing: 'inherit',
        borderRadius: 30,
        margin: '10px',
    },
    caption: {
        display: 'inline-block',
    },
    leave: {
        display: 'inline-block',
    },
    leaveButton: {
        marginBottom: '5px',
    },
    headBlock: {
        display: 'flex',
        justifyContent: 'space-between'
    },
};


class CourseCard extends React.Component {
    render() {
        const {classes, text, caption, courseID} = this.props;
        return (
            <Card
                className={classes.card}
            >
                <CardContent>
                    <div className={classes.headBlock}>
                        <Typography
                            className={classes.caption}
                            variant="h5"
                            component="h2"
                        >
                            {caption}
                        </Typography>
                        <Typography className={classes.leave}
                                    variant="h5"
                                    component="h2"
                        >
                            <Button className={classes.leaveButton}
                                    variant="contained"
                                    color="secondary"
                                    key={courseID}
                            >
                                Отписаться
                                <DeleteIcon/>
                            </Button>
                        </Typography>
                    </div>
                    <Divider/>
                    <Typography
                        component="p"
                    >
                        {text}
                    </Typography>
                </CardContent>
            </Card>
        );
    }
}

CourseCard.propTypes = {
    classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(CourseCard);
