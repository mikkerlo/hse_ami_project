import React from "react";
import DeadlineCard from "./DeadlineCard";
import {getFromApi} from "../utils";
import PropTypes from "prop-types";


class DeadlineCardList extends React.Component {
    constructor(props) {
        super(props);
        let deadlines = [];
        this.apiLink = props.link;
        this.state = {};
        this.state.deadlines = deadlines;
    }

    fetchData() {
        getFromApi(this.apiLink, function (err, res) {
            if (err) {
                console.log('error occurred');
            } else {
                this.setState({deadlines: res});
            }
        }.bind(this));
    }

    componentDidMount() {
        this.fetchData();
    }

    componentWillReceiveProps(nextProps, nextContext) {
        this.apiLink = nextProps.link;
        this.setState({deadlines:[]});
        this.fetchData();
    }

    render() {
        return <div style={{width: '100%'}}>
            {this.state.deadlines.map(deadline => (
                <DeadlineCard
                    text={deadline.content}
                    caption={deadline.header}
                    files={[]}
                    date={deadline.valid_until}
                    key={deadline.id}
                />
            ))}
        </div>;
    }
}


DeadlineCardList.propTypes = {
    link: PropTypes.string.isRequired,
};

export default DeadlineCardList;
