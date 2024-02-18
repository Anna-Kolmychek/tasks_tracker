from fastapi.encoders import jsonable_encoder

from src.tasks.models import Task
from src.tasks.schemas import TaskStatus
from tests.conftest import client, TestingSessionLocal


def test_create_task(clear_db, position_data1, user_data1, task_data1, task_data2):
    # Очистили БД в фикстуре clear_db

    # Case 1: Создание задачи с неполными данными, проверка кода ответа
    response = client.post('/tasks/', json={**task_data1})
    task1_id = response.json().get('id')
    assert response.status_code == 200, 'Неверный код ответа'

    # Case 2: Создание задачи с неполными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_task = db.get(Task, task1_id)
    assert response.json() == jsonable_encoder(db_task), 'Тело ответа не совпадает с записью в БД'

    # Case 3: Создание задачи с неполными данными, проверка тела ответа
    task_data1['description'] = task_data1['parent_task_id'] = None
    task_data1['maker_id'] = task_data1['maker_position_id'] = task_data1['deadline'] = None
    task_data1['status'] = TaskStatus.new.value
    task_data1['id'] = task1_id
    assert response.json() == task_data1, 'Тело ответа не совпадает c вводимыми данными'

    # Case 4: Создание задачи с полными данными, проверка кода ответа
    client.post('/positions/', json={**position_data1})
    client.post('/users/', json={**user_data1})
    response = client.post('/tasks/', json={**task_data2})
    task2_id = response.json().get('id')
    assert response.status_code == 200, 'Неверный код ответа'

    # Case 5: Создание задачи с полными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_task = db.get(Task, task2_id)
    assert response.json() == jsonable_encoder(db_task), 'Тело ответа не совпадает с записью в БД'

    # Case 6: Создание задачи с полными данными, проверка тела ответа
    task_data2['id'] = task2_id
    assert response.json() == task_data2, 'Тело ответа не совпадает c вводимыми данными'

    # Case 7: Создание задачи с несуществующим parent_task_id, проверка кода ответа
    task_data2.pop('id')
    task_data2['parent_task_id'] = 10000
    response = client.post('/tasks/', json={**task_data2})
    assert response.status_code == 400, 'Неверный код ответа'

    # Case 8: Создание задачи с несуществующим maker_id, проверка кода ответа
    task_data2.pop('parent_task_id')
    task_data2['maker_id'] = 10000
    response = client.post('/tasks/', json={**task_data2})
    assert response.status_code == 400, 'Неверный код ответа'

    # Case 9: Создание задачи с несуществующим maker_position_id, проверка кода ответа
    task_data2.pop('maker_id')
    task_data2['maker_position_id'] = 10000
    response = client.post('/tasks/', json={**task_data2})
    assert response.status_code == 400, 'Неверный код ответа'

    # Case 10: Создание задачи с несуществующим status
    task_data2.pop('maker_position_id')
    task_data2['status'] = 'fake status'
    response = client.post('/tasks/', json={**task_data2})
    assert response.status_code == 422, 'Неверный код ответа'


def test_get_all_tasks():
    # Case 1: Запрос всех задач, проверка кода ответа
    response = client.get('/tasks/')
    assert response.status_code == 200, 'Неверный код ответа'

    # Case 2: Запрос всех задач, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_tasks = db.query(Task).all()
        db_tasks_data = jsonable_encoder(db_tasks)
    assert response.json() == db_tasks_data, 'Тело ответа не совпадает с записью в БД'

    # Case 3: Запрос всех задач, проверка limit и offset
    response = client.get('/tasks/?skip=1&limit=1')
    with TestingSessionLocal() as db:
        db_tasks = db.query(Task).offset(1).limit(1).all()
        db_tasks_data = jsonable_encoder(db_tasks)
    assert response.json() == db_tasks_data, 'Тело ответа не совпадает с записью в БД, проверка limit и offset'


def test_get_task_by_id(task_data1):
    # Case 1: Запрос несуществующей задачи, проверка кода ответа
    response = client.get(f'/tasks/{10000}')
    assert response.status_code == 404, 'Неверный код ответа'

    # Case 2: Запрос существующей задачи, проверка кода ответа
    response = client.post('/tasks/', json={**task_data1})
    task_id = response.json().get('id')
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200, 'Неверный код ответа'

    # Case 3: Запрос существующей задачи, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_tasks = db.get(Task, task_id)
    assert response.json() == jsonable_encoder(db_tasks), 'Тело ответа не совпадает с записью в БД'


def test_update_task_by_id(clear_db, task_data1, task_data2, position_data1, user_data1):
    # Case 1: Обновление несуществующей задачи, проверка кода ответа
    response = client.put(f'/tasks/{10000}', json={**task_data1})
    assert response.status_code == 404, 'Неверный код ответа, несуществующая задача'

    # Case 2: Обновление существующей задачи, проверка кода ответа
    client.post('/positions/', json={**position_data1})
    client.post('/users/', json={**user_data1})
    client.post('/tasks/', json={**task_data1})
    response = client.post('/tasks/', json={**task_data1})
    task_id = response.json().get('id')
    response = client.put(f'/tasks/{task_id}', json={**task_data2})
    assert response.status_code == 200, 'Неверный код ответа, существующая задача'

    # Case 3: Обновление существующей задачи полными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_tasks = db.get(Task, task_id)
    assert response.json() == jsonable_encoder(db_tasks), 'Тело ответа не совпадает с записью в БД'

    # Case 4: Обновление существующей задачи полными данными, проверка тела ответа
    task_data2['id'] = task_id
    assert response.json() == task_data2, 'Тело ответа не совпадает c вводимыми данными'

    # Case 5: Обновление существующей задачи неполными данными, проверка совпадения тела ответа и данных в БД
    response = client.put(f'/tasks/{task_id}', json={**task_data1})
    with TestingSessionLocal() as db:
        db_tasks = db.get(Task, task_id)
    assert response.json() == jsonable_encoder(db_tasks), 'Тело ответа не совпадает с записью в БД'

    # Case 6: Обновление существующей задачи неполными данными, проверка данных тела ответа
    task_data1['description'] = task_data1['parent_task_id'] = None
    task_data1['maker_id'] = task_data1['maker_position_id'] = task_data1['deadline'] = None
    task_data1['status'] = TaskStatus.new.value
    task_data1['id'] = task_id
    assert response.json() == task_data1, 'Тело ответа не совпадает c вводимыми данными'

    # Case 7: Обновление существующей задачи несуществующим status, проверка кода ответа
    task_data1.pop('id')
    task_data1['status'] = 'fake status'
    response = client.put(f'/tasks/{task_id}', json={**task_data1})
    assert response.status_code == 422, 'Неверный код ответа, несуществующий status'

    # Case 8: Обновление существующей задачи несуществующим parent_task_id, проверка кода ответа
    task_data1.pop('status')
    task_data1['parent_task_id'] = 10000
    response = client.put(f'/tasks/{task_id}', json={**task_data1})
    assert response.status_code == 400, 'Неверный код ответа, несуществующий parent_task_id'

    # Case 9: Обновление существующей задачи несуществующим maker_id, проверка кода ответа
    task_data1.pop('parent_task_id')
    task_data1['maker_id'] = 10000
    response = client.put(f'/tasks/{task_id}', json={**task_data1})
    assert response.status_code == 400, 'Неверный код ответа, несуществующий maker_id'

    # Case 10: Обновление существующей задачи несуществующим maker_position_id, проверка кода ответа
    task_data1.pop('maker_id')
    task_data1['maker_position_id'] = 10000
    response = client.put(f'/tasks/{task_id}', json={**task_data1})
    assert response.status_code == 400, 'Неверный код ответа, несуществующий maker_position_id'


def test_partial_update_task_by_id(clear_db, task_data1, task_data2, position_data1, user_data1):
    # Case 1: Обновление несуществующей задачи, проверка кода ответа
    response = client.patch(f'/tasks/{10000}', json={**task_data1})
    assert response.status_code == 404, 'Неверный код ответа, несуществующая задача'

    # Case 2: Обновление существующей задачи, проверка кода ответа
    client.post('/positions/', json={**position_data1})
    client.post('/users/', json={**user_data1})
    client.post('/tasks/', json={**task_data1})
    response = client.post('/tasks/', json={**task_data2})
    task_id = response.json().get('id')
    response = client.patch(f'/tasks/{task_id}', json={**task_data1})
    assert response.status_code == 200, 'Неверный код ответа, существующая задача'

    # Case 3: Обновление существующей задачи неполными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_tasks = db.get(Task, task_id)
    assert response.json() == jsonable_encoder(db_tasks), 'Тело ответа не совпадает с записью в БД'

    # Case 4: Обновление существующей задачи неполными данными, проверка тела ответа
    task_data2['id'] = task_id
    task_data2['title'] = task_data1['title']
    assert response.json() == task_data2, 'Тело ответа не совпадает c вводимыми данными'


def test_delete_task_by_id(task_data1):
    # Case 1: Удаление несуществующей задачи, проверка кода ответа
    response = client.delete(f'/tasks/{10000}')
    assert response.status_code == 404, 'Неверный код ответа, несуществующая задача'

    # Case 2: Удаление существующей задачи, проверка кода ответа
    response = client.post('/tasks/', json={**task_data1})
    task_id = response.json().get('id')
    with TestingSessionLocal() as db:
        db_tasks = db.get(Task, task_id)
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200, 'Неверный код ответа, существующая задача'

    # Case 3: Удаление существующей задачи, проверка тела ответа
    assert response.json() == jsonable_encoder(db_tasks), 'Тело ответа не совпадает с записью в БД'

    # Case 4: Удаление существующей задачи, проверка отсутствия данных в ДБ
    with (TestingSessionLocal() as db):
        is_exist = db.query(Task.id).where(Task.id == task_id).first() is not None
    assert not is_exist, 'Объект не удален из БД'
