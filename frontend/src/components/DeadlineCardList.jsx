import React from "react";
import DeadlineCard from "./DeadlineCard";
import {getFromApi} from "../utils";


class DeadlineCardList extends React.Component {
    constructor(props) {
        super(props);
        let deadlines = [];
        this.state = {};
        this.state.deadlines = deadlines;
        getFromApi('/api/deadlines/all', function (err, res) {
            if (err) {
                console.log('error occured');
            } else {
                this.setState({deadlines: res});
            }
        }.bind(this));
    }

    render() {
        return <div>
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

export default (DeadlineCardList);
