import React from "react";
import {getFromApi} from "../utils";
import CourseCard from './CourseCard';
import {groupUrl} from "../apiUrls";

class ApiCourseCard extends React.Component {
    constructor(props) {
        super(props);
        this.apiID = props.apiID;
        this.state = {}
    }

    fetchData() {
        getFromApi(groupUrl(this.apiID), function (err, res) {
            if (err) {
                console.log('error occurred');
            } else {
                this.setState(res);
            }
        }.bind(this));
    }

    componentDidMount() {
        this.fetchData();
    }

    componentWillReceiveProps(nextProps, nextContext) {
        if (nextProps.apiID !== this.apiID) {
            this.apiID = nextProps.apiID;
            this.fetchData();
        }
    }

    render() {
        const {id, full_name, description} = this.state;
        if (id && full_name && description) {
            return <CourseCard
                text={description}
                caption={full_name}
                courseID={id}
            />
        } else {
            return <div/>
        }

    }
}

export default ApiCourseCard;