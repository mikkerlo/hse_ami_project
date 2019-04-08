import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import Typography from '@material-ui/core/Typography';

import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';

import NavigationIcon from '@material-ui/icons/Navigation';
import Fab from '@material-ui/core/Fab';
import InputAdornment from "@material-ui/core/InputAdornment";
import People from "@material-ui/core/SvgIcon/SvgIcon";
import DeadlineCard from "./DeadlineCard";

const styles = {
  root: {
    flexGrow: 1,
  },
  grow: {
    flexGrow: 1,
  },
  menuButton: {
    marginLeft: -12,
    marginRight: 20,
  },
};

function ButtonAppBar(props) {
  const { classes, caption } = props;

  return (
    <div className={"classes.root"}>
      <AppBar position="static" className={"kek"}>
        <Toolbar className={"kek1"}>
          <IconButton className={classes.menuButton} color="inherit" aria-label="Menu">
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" color="inherit" className={classes.grow}>
            {caption}
          </Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>
    </div>
  );
}

ButtonAppBar.propTypes = {
  classes: PropTypes.object.isRequired,
};

let Kek = withStyles(styles)(ButtonAppBar);


ReactDOM.render(
    <div>
        <Kek className={"Kek3"}
          caption="Hello world"
        />
        <h1>Hello, world!</h1>
        <Typography variant="h4" gutterBottom>
          AMI
        </Typography>
              <Fab variant="extended" aria-label="Delete" color="primary">
        <NavigationIcon/>
                  Extended
                  <img src={"https://material-ui.com/static/images/grid-list/breakfast.jpg"} height={"50"}/>
      </Fab>
        <Card style={{width: '300px'}}>
            <div style={{padding: '0px 0px 0px 80px'}}>
            <TextField
          id="standard-uncontrolled"
          label="Login"
          defaultValue=""
          margin="normal"
        />
            </div>
            <div style={{padding: '0px 0px 0px 80px'}}>
        <TextField
          id="standard-uncontrolled"
          label="Password"
          defaultValue=""
          margin="normal"
        />
            </div>
            <div style={{padding: '10px 0px 10px 80px'}}>
            <Button
            color='primary'
            variant="contained">
                GO
            </Button>
            </div>
        </Card>
        <br></br>
        <DeadlineCard
        text={"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."}
        caption={"Caption"}
        files={["file1.txt", "kek.pdf"]}
        date={"вчера"}/>

    </div>,
    document.getElementById('root')
);