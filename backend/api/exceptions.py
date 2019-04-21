class AMIBaseException(Exception):
    """
    Base exception for API unexpected situations
    """

    def __init__(self):
        super(AMIBaseException, self).__init__()
        self.error: str = ''
        self.status_code: int = 0


class DeadlineDoesNotExists(AMIBaseException):
    def __init__(self, deadline_id):
        super(DeadlineDoesNotExists, self).__init__()
        self.error = f'Deadline with id={deadline_id} does not exists'
        self.status_code = 404

class GroupDoesNotExists(AMIBaseException):
    def __init__(self, group_id):
        super(GroupDoesNotExists, self).__init__()
        self.error = f'Group with id={group_id} does not exists'
        self.status_code = 404