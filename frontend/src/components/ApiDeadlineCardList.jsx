import React from 'react';
import DeadlineCardList from './DeadlineCardList';
import {allDeadlinesUrl, groupDeadlinesUrl, studentDeadlinesUrl} from "../apiUrls";

export function AllDeadlineCardList() {
    return <DeadlineCardList
        link={allDeadlinesUrl()}
    />
}

export function StudentDeadlineCardList() {
    return <DeadlineCardList
        link={studentDeadlinesUrl()}
    />
}

export function CourseDeadlineCardList(props) {
    return <DeadlineCardList
        link={groupDeadlinesUrl(props.id)}
    />
}


