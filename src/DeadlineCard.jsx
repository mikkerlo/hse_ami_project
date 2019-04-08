import React from "react";
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
// import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import AttachmentIcon from '@material-ui/icons/AttachFile';

const styles = {
  card: {
    minWidth: 275,
    maxWidth: 500,
    boxSizing: 'inherit',
  },
  bullet: {
    display: 'inline-block',
    margin: '0 2px',
    transform: 'scale(0.8)',
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
};

function DeadlineCard(props) {
  const { classes, text, caption, files, date } = props;
  console.log(files);
  let files_buttons = <div>
    {files.map(tile => (
          <Button variant="contained" style={{margin: '10px'}}>
            <AttachmentIcon/>
      {tile}
    </Button>))}
  </div>;

  return (
    <Card className={classes.card}>
      <CardContent>
        <div>
        <Typography variant="h5" component="h2">
          {caption}
        </Typography>
        </div>
        <div>
        <Typography>
          {date}
        </Typography>
        </div>
        <hr></hr>
        <Typography component="p">
          {text}
          <br />
        </Typography>
        <hr></hr>
        {files_buttons}
      </CardContent>
    </Card>
  );
}

DeadlineCard.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(DeadlineCard);
