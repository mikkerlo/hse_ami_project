import React from 'react';
import Typography from '@material-ui/core/Typography';
import Fab from '@material-ui/core/Fab';
import NavigationIcon from '@material-ui/icons/Navigation';
import NavBar from './components/NavBar.jsx'
import {AllDeadlineCardList} from "./components/ApiDeadlineCardList";
import TinyCourseList from "./components/TinyCourseList";
import DeadlineCard from './components/DeadlineCard';
import CourseCard from './components/CourseCard';
import Login from "./components/Login";
import Registration from "./components/Register";


class Elements extends React.Component {
    render() {
        return (
            <div>
                <NavBar/>
                <Registration/>
                <Login/>

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
                    <img alt={"kek"} src={"https://material-ui.com/static/images/grid-list/breakfast.jpg"}
                         height={"40"}/>
                </Fab>
                <div className="box">
                    <div>One</div>
                    <div>Two</div>
                    <div>Three</div>
                    <div className="push">Four</div>
                    <div>Five</div>
                </div>
                <br/>
                <DeadlineCard
                    content={"Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum."}
                    header={"Caption"}
                    files={[{name: "file1.txt", id: 123, url: '/'}]}
                    valid_until={1554}/>
                <AllDeadlineCardList/>
                <TinyCourseList/>
            </div>
        )
    }
}


export default Elements;
