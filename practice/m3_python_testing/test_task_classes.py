"""
Write tests for classes in 2_python_part_2/task_classes.py (Homework, Teacher, Student).
Check if all methods working correctly.
Also check corner-cases, for example if homework number of days is negative.
"""

import pytest
from practice.m2_python_part_2 import task_classes
from datetime import datetime, timedelta


class TestTeacher:

    def setup_method(self, method):
        self.teacher = task_classes.Teacher("Mark", "Willy")

    def test_create_homework_with_positve_days(self):
        homework = self.teacher.create_homework("Lorem", 3)
        assert isinstance(homework, task_classes.Homework)
        assert isinstance(homework.deadline, datetime)
        assert homework.is_active() == True

    def test_create_homework_with_negative_days(self):
        with pytest.raises(task_classes.NegativeDaysToCompleteException):
            homework = self.teacher.create_homework("Lorem", -3)


@pytest.fixture
def future_date_10_days():
    date = datetime.now() + timedelta(days=10)
    return date


@pytest.fixture
def past_date_10_days():
    date = datetime.now() - timedelta(days=10)
    return date


class TestStudent:

    def test_init(self):
        student = task_classes.Student("Adam", "Smith")
        assert isinstance(student, task_classes.Student)
        assert student.first_name == "Adam"
        assert student.last_name == "Smith"

    def test_do_homework_on_time(self, future_date_10_days, past_date_10_days):
        student = task_classes.Student("Adam", "Smith")
        homework = task_classes.Homework(
            "Lorem", future_date_10_days, past_date_10_days
        )
        homework = student.do_homework(homework)
        assert isinstance(homework, task_classes.Homework)

    def test_do_homework_late(self, capfd, past_date_10_days):
        student = task_classes.Student("Adam", "Smith")
        homework = task_classes.Homework("Lorem", past_date_10_days, past_date_10_days)
        homework = student.do_homework(homework)
        assert homework == None
        out, err = capfd.readouterr()
        assert "You are late" in out


class TestHomework:
    def test_init(self, past_date_10_days, future_date_10_days):
        homework = task_classes.Homework(
            "Lorem", future_date_10_days, past_date_10_days
        )
        assert isinstance(homework, task_classes.Homework)

    def test_is_active_past_dealine(self, past_date_10_days):
        homework = task_classes.Homework("Lorem", past_date_10_days, past_date_10_days)
        assert homework.is_active() == False

    def test_is_active_before_dealine(self, past_date_10_days, future_date_10_days):
        homework = task_classes.Homework(
            "Lorem", future_date_10_days, past_date_10_days
        )
        assert homework.is_active() == True
