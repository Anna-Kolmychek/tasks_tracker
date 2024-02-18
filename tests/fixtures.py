import pytest

from src.database import Base
from src.positions.models import Position
from src.tasks.models import Task
from src.users.models import User
from tests.conftest import engine, TestingSessionLocal


@pytest.fixture
def position_data1():
    return {'title': 'developer'}


@pytest.fixture
def position_data2():
    return {'title': 'manager'}


@pytest.fixture
def user_data1(position_data1):
    return {
        "email": "ivanov@email.com",
        "password": "qwerty",
        "firstname": "ivan",
        "lastname": "ivanov",
        "position": position_data1['title']
    }


@pytest.fixture
def user_data2():
    return {
        "email": "petrov@email.com",
        "password": "qwerty"
    }


@pytest.fixture
def user_data3():
    return {
        "email": "sidorov@email.com",
        "password": "qwerty",
        "position": "fake position"
    }


@pytest.fixture
def task_data1():
    return {
        "title": "Task 1"
    }

@pytest.fixture
def task_data2():
    return {
        "description": "Test description",
        "status": "in work",
        "parent_task_id": 1,
        "maker_id": 1,
        "maker_position_id": 1,
        "deadline": "2024-02-16",
        "title": "Task 2"
    }


@pytest.fixture()
def load_test_data_in_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as db:
        job_positions = [
            [1, 'Backend Developer'],
            [2, 'Frontend Developer'],
            [3, 'QA Engineer'],
            [4, 'Project Manager'],
        ]
        columns = ['id', 'title']
        for row in job_positions:
            position = dict(zip(columns, row))
            db.add(Position(**position))

        users = [
            [1, 'i_ivanov@email.com', 'Иван', 'Иванов', 'string', 1],
            [2, 'p_petrov@email.com', 'Петр', 'Петров', 'string', 1],
            [3, 's_sergeev@email.com', 'Сергей', 'Сергеев', 'string', 1],
            [4, 'a_andreev@email.com', 'Андрей', 'Андреев', 'string', 1],
            [5, 'a_smirnov@email.com', 'Антон', 'Смирнов', 'string', 2],
            [6, 'a_popov@email.com', 'Артем', 'Попов', 'string', 2],
            [7, 'b_sokolov@email.com', 'Борис', 'Соколов', 'string', 3],
            [8, 'v_morozov@email.com', 'Виктор', 'Морозов', 'string', 3],
            [9, 'v_volkov@email.com', 'Виталий', 'Волков', 'string', 4],
            [10, 'd_vasilev@email.com', 'Денис', 'Васильев', 'string', None],
            [11, 'd_pavlov@email.com', 'Дмитрий', 'Павлов', 'string', None],
        ]
        columns = ['id', 'email', 'firstname', 'lastname', 'password', 'position_id']
        for row in users:
            position = dict(zip(columns, row))
            db.add(User(**position))

        tasks = [
            [1, 'Backend задача 1', None, 'new', '2024-04-12', None, 1, 1],
            [2, 'Backend задача 2', None, 'in_work', '2024-03-10', 7, 1, 1],
            [3, 'Backend задача 3', None, 'new', '2024-05-30', None, 2, 1],
            [4, 'Backend задача 4', None, 'new', '2024-05-30', None, 2, 1],
            [5, 'Backend задача 5', None, 'new', '2024-05-30', None, 2, 1],
            [6, 'Backend задача 6', None, 'in_work', '2024-03-15', 1, 2, 1],
            [7, 'Backend задача 7', None, 'new', '2024-04-15', None, None, 1],
            [8, 'Backend задача 8', None, 'new', '2024-04-15', None, None, 1],
            [9, 'Backend задача 9', None, 'new', '2024-04-15', 8, None, 1],
            [10, 'QA задача 1', None, 'in_work', '2024-02-12', None, 8, 3],
            [11, 'Frontend задача 1', None, 'in_work', '2024-02-12', None, 5, 2],
            [12, 'Backend задача 10', None, 'closed', '2024-02-13', None, 4, 1],
            [13, 'Backend задача 11', None, 'closed', '2024-02-13', 15, 4, 1],
            [14, 'Backend задача 12', None, 'closed', '2024-02-13', 15, 4, 1],
            [15, 'Backend задача 13', None, 'closed', '2024-02-13', None, 4, 1],
            [16, 'Backend задача 14', None, 'closed', '2024-02-13', None, 4, 1],
            [17, 'QA задача 2', None, 'closed', '2024-02-14', None, 8, 3],
            [18, 'QA задача 3', None, 'new', '2024-02-14', None, 8, 3],
        ]
        columns = ['id', 'title', 'description', 'status', 'deadline', 'parent_task_id', 'maker_id', 'maker_position_id']
        for row in tasks:
            position = dict(zip(columns, row))
            db.add(Task(**position))

        db.commit()
