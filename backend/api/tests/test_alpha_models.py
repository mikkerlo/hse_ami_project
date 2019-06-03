import pytest


@pytest.mark.run(after='test_student_creation')
@pytest.mark.django_db
def test():
    pass