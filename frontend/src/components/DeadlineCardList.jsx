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

        xhr.open("GET", "/api/deadlines");
        xhr.onload = function () {
            if (xhr.status === 200) {
                try {
                    let result = JSON.parse(xhr.response);
                    self.setState({deadlines: result.response});
                } catch (e) {
                    console.log('error occured')
                }
            }
        };
        xhr.send();
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
