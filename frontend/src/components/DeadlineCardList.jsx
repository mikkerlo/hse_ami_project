import React from "react";
import DeadlineCard from "./DeadlineCard";

class DeadlineCardList extends React.Component {
    constructor(props) {
        super(props);
        let deadlines = [];
        const self = this;
        this.state = {};
        this.state.deadlines = deadlines;
        const xhr = new XMLHttpRequest();
        console.log('xhr launch');

        xhr.open("GET", "/api/deadlines");
        xhr.onload = function () {
            console.log(xhr);
            if (xhr.status === 200) {
                try {
                    let result = JSON.parse(xhr.response);
                    self.setState({deadlines: result.response});
                    console.log(result.response);
                } catch (e) {
                    console.log(e);
                }
            }
        };
        xhr.send();
    }

    render() {
        console.log(this.state.deadlines);
        return <div>
            {this.state.deadlines.map(deadline => (
                <DeadlineCard
                    text={deadline.content}
                    caption={deadline.header}
                    files={[]}
                    date={deadline.valid_until}
                />
            ))}
        </div>;
    }
}

export default (DeadlineCardList);