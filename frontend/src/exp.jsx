import React from 'react';
import Typography from '@material-ui/core/Typography';
import Fab from '@material-ui/core/Fab';
import NavigationIcon from '@material-ui/icons/Navigation';
import Card from '@material-ui/core/Card';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';

import NavBar from './components/NavBar.jsx'
import DeadlineCardList from "./components/DeadlineCardList";
import TinyCourseList from "./components/TinyCourseList";
import DeadlineCard from './components/DeadlineCard';
import CourseCard from './components/CourseCard';


function Elements() {
    return (
        <div>
            <NavBar/>
            <CourseCard
                caption="Матан"
                text="Шаповал крут, будь как Шаповал!"
            >
            </CourseCard>
            <h1>Simple text inside h1</h1>
            <Typography variant="h4" gutterBottom>
                Typography text
            </Typography>
            <Fab variant="extended" aria-label="Delete" color="primary">
                <NavigationIcon/>
                Extended
                <img alt={"kek"} src={"https://material-ui.com/static/images/grid-list/breakfast.jpg"} height={"40"}/>
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
            <div className="box">
                <div>One</div>
                <div>Two</div>
                <div>Three</div>
                <div className="push">Four</div>
                <div>Five</div>
            </div>
            <br/>
            <DeadlineCard
                text={"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."}
                caption={"Caption"}
                files={["file1.txt", "kek.pdf", "lections.pdf", "cheatsheet.pdf", "yet_another_file.pdf"]}
                date={1554}/>
            <DeadlineCardList/>
            <TinyCourseList/>
        </div>
    )
}


export default Elements;
