import React from "react";
import {getFromApi} from "../utils";
import CourseCard from "./CourseCard";
import {studentGroupsUrl} from "../apiUrls";


class CourseList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            courses: [],
        };
    }

    fetchData() {
        getFromApi(studentGroupsUrl(), function (err, res) {
            if (err) {
                console.log('error occurred');
            } else {
                this.setState({courses: res});
            }
        }.bind(this));
    }

    componentDidMount() {
        this.fetchData();
    }

    render() {
        return <div style={{width: '100%'}}>
            {this.state.courses.map(course => (
                <CourseCard
                    {...course}
                />
            ))}
        </div>;
    }
}

export default (CourseList);