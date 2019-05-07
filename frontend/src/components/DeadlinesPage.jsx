import React from 'react';
import NavBar from './NavBar.jsx'
import DeadlineCardList from "./DeadlineCardList";
import TinyCourseList from "./TinyCourseList";
import DeadlineCard from "./DeadlineCard";


function Elements() {
    return (
        <div>
            <NavBar/>
            <div style={{
                marginRight: 'auto',
                marginLeft: 'auto',
                maxWidth: 1000
            }}>
                <div style={{
                    width: '80%',
                    float: 'left',
                    paddingRight: 10,
                    boxSizing: 'border-box'
                }}>
                    <DeadlineCardList/>
                </div>
                <div style={{
                    width: '20%',
                    float: 'right',
                    paddingTop: 20,
                    boxSizing: 'border-box',
                }}>
                    <TinyCourseList/>
                </div>
            </div>
        </div>
    )
}


export default Elements;