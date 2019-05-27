import React from 'react';
import DeadlineCardList from './DeadlineCardList';

export function AllDeadlineCardList() {
    return <DeadlineCardList
        link={'/api/deadlines/all/'}
    />
}

export function StudentDeadlineCardList() {
    return <DeadlineCardList
        link={'/api/students/deadlines/'}
    />
}

export function CourseDeadlineCardList(props) {
    return <DeadlineCardList
        link={'/api/groups/' + props.id + '/deadlines/'}
    />
}


