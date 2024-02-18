from fastapi.encoders import jsonable_encoder

from src.users.models import User
from tests.conftest import client, TestingSessionLocal


def test_create_user(clear_db, user_data1, user_data2, user_data3, position_data1):
    # Очистили БД в фикстуре clear_db
    response = client.post('/positions/', json={**position_data1})
    position_id = response.json().get('id')

    # Case 1: Создание пользователя с полными данными, проверка кода ответа
    response = client.post('/users/', json={**user_data1})
    assert response.status_code == 200, 'Неверный код ответа'
    user_id = response.json().get('id')

    # Case 2: Создание пользователя с полными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
        db_user_data = jsonable_encoder(db_user)
    del db_user_data['password']
    assert response.json() == db_user_data, 'Тело ответа не совпадает с записью в БД'

    # Case 3: Создание пользователя с полными данными, проверка тела ответа
    user_data1['id'] = user_id
    user_data1['position_id'] = position_id
    user_data1.pop('position')
    user_data1.pop('password')
    assert response.json() == user_data1, 'Тело ответа не совпадает c вводимыми данными'

    # Case 4: Создание пользователя с неполными данными, проверка кода ответа
    response = client.post('/users/', json={**user_data2})
    assert response.status_code == 200, 'Неверный код ответа'
    user_id = response.json().get('id')

    # Case 5: Создание пользователя с неполными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
        db_user_data = jsonable_encoder(db_user)
    del db_user_data['password']
    assert response.json() == db_user_data, 'Тело ответа не совпадает с записью в БД'

    # Case 6: Создание пользователя с неполными данными, проверка тела ответа
    user_data2['id'] = user_id
    user_data2['position_id'] = None
    user_data2['firstname'] = None
    user_data2['lastname'] = None
    user_data2.pop('password')
    assert response.json() == user_data2, 'Тело ответа не совпадает c вводимыми данными'

    # Case 7: Создание пользователя с несуществующей position, проверка совпадения тела ответа и данных в БД
    response = client.post('/users/', json={**user_data3})
    user_id = response.json().get('id')
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
        db_user_data = jsonable_encoder(db_user)
    del db_user_data['password']
    assert response.json() == db_user_data, 'Тело ответа не совпадает с записью в БД'

    # Case 8: Создание пользователя с несуществующей position, проверка тела ответа
    user_data3['id'] = user_id
    user_data3['position_id'] = None
    user_data3['firstname'] = None
    user_data3['lastname'] = None
    user_data3.pop('password')
    user_data3.pop('position')
    assert response.json() == user_data3, 'Тело ответа не совпадает c вводимыми данными'

    # Case 9: Создание пользователя с дублем email, проверка кода ответа
    user_data3['password'] = 'pass'
    response = client.post('/users/', json={**user_data3})
    assert response.status_code == 400, 'Неверный код ответа'


def test_get_all_users(user_data2):
    # Case 1: Запрос всех пользователей, проверка кода ответа
    response = client.get('/users/')
    assert response.status_code == 200, 'Неверный код ответа'

    # Case 2: Запрос всех пользователей, проверка количества записей
    assert len(response.json()) == 3, 'Неверное количество данных'

    # Case 3: Запрос всех пользователей, проверка limit и offset
    response = client.get('/users/?skip=1&limit=1')
    assert len(response.json()) == 1, 'Неверное количество данных при наличии limit'
    assert response.json()[0]['email'] == user_data2['email'], 'Неверная запись в ответе'


def test_get_user_by_id():
    # Case 1: Запрос несуществующего пользователя, проверка кода ответа
    response = client.get(f'/users/{10000}')
    assert response.status_code == 404, 'Неверный код ответа, несуществующий пользователь'

    # Case 2: Запрос существующего пользователя, проверка кода ответа
    response = client.get(f'/users/{1}')
    assert response.status_code == 200, 'Неверный код ответа, существующий пользователь'

    # Case 3: Запрос существующего пользователя, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_user = db.get(User, response.json().get('id'))
    db_user_data = jsonable_encoder(db_user)
    db_user_data.pop('password')
    assert db_user_data == response.json(), 'Тело ответа не совпадает с записью в БД'


def test_update_user_by_id(clear_db, position_data1, user_data1, user_data2, user_data3):
    # Очистили БД в фикстуре clear_db

    # Case 1: Обновление несуществующего пользователя, проверка кода ответа
    response = client.put(f'/users/{10000}', json={**user_data2})
    assert response.status_code == 404, 'Неверный код ответа, несуществующий пользователь'

    # Case 2: Обновление существующего пользователя, проверка кода ответа
    response = client.post('/positions/', json={**position_data1})
    position_id = response.json().get('id')
    response = client.post('/users/', json={**user_data1})
    user_id = response.json().get('id')
    response = client.put(f'/users/{user_id}', json={**user_data2})
    assert response.status_code == 200, 'Неверный код ответа, существующий пользователь'

    # Case 3: Обновление существующего пользователя неполными данными, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
    db_user_data = jsonable_encoder(db_user)
    db_user_data.pop('password')
    assert db_user_data == response.json(), 'Тело ответа не совпадает с записью в БД, обновление неполными данными'

    # Case 4: Обновление существующего пользователя неполными данными, проверка данных тела ответа
    user_data2['id'] = user_id
    user_data2['position_id'] = None
    user_data2['firstname'] = None
    user_data2['lastname'] = None
    user_data2.pop('password')
    assert response.json() == user_data2, 'Тело ответа не совпадает c вводимыми данными, обновление неполными данными'

    # Case 5: Обновление существующего пользователя полными данными, проверка совпадения тела ответа и данных в БД
    response = client.put(f'/users/{user_id}', json={**user_data1})
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
    db_user_data = jsonable_encoder(db_user)
    db_user_data.pop('password')
    assert db_user_data == response.json(), 'Тело ответа не совпадает с записью в БД, обновление полными данными'

    # Case 6: Обновление существующего пользователя полными данными, проверка тела ответа
    user_data1.pop('password')
    user_data1.pop('position')
    user_data1['id'] = user_id
    user_data1['position_id'] = position_id
    assert response.json() == user_data1, 'Тело ответа не совпадает c вводимыми данными, обновление полными данными'

    # Case 7: Обновление существующего пользователя несуществующей position, проверка тела ответа
    user_data1.pop('position_id')
    user_data1.pop('id')
    user_data1['position'] = 'fake position'
    user_data1['password'] = 'pass'
    response = client.put(f'/users/{user_id}', json={**user_data1})
    assert response.status_code == 200, 'Неверный код ответа, обновление несуществующий position'
    assert response.json()['position_id'] is None, 'Неверный position_id, обновление несуществующий position'

    # Case 8: Обновление существующего пользователя где email совпадает с обновляемым, проверка кода ответа
    response = client.put(f'/users/{user_id}', json={**user_data1})
    assert response.status_code == 200, 'Неверный код ответа, email совпадает с обновляемым'

    # Case 9: Обновление существующего пользователя дубликатом email, проверка кода ответа
    client.post(f'/users/', json={**user_data3})
    user_data1['email'] = user_data3['email']
    response = client.put(f'/users/{user_id}', json={**user_data1})
    assert response.status_code == 400, 'Неверный код ответа, дубликат email'


def test_partial_update_user_by_id(clear_db, user_data1, user_data3):
    # Очистили БД в фикстуре clear_db

    # Case 1: Обновление несуществующего пользователя, проверка кода ответа
    response = client.patch(f'/users/{10000}', json={**user_data1})
    assert response.status_code == 404, 'Неверный код ответа, несуществующий пользователь'

    # Case 2: Обновление существующего пользователя, проверка кода ответа
    response = client.post('/users/', json={**user_data1})
    user_id = response.json().get('id')
    response = client.patch(f'/users/{user_id}', json={**user_data3})
    assert response.status_code == 200, 'Неверный код ответа, существующий пользователь'

    # Case 3: Обновление существующего пользователя неполными данными
    # с несуществующей position, проверка совпадения тела ответа и данных в БД
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
    db_user_data = jsonable_encoder(db_user)
    db_user_data.pop('password')
    assert db_user_data == response.json(), 'Тело ответа не совпадает с записью в БД'

    # Case 4: Обновление существующего пользователя неполными данными
    # с несуществующей position, проверка тела ответа
    user_data1.pop('password')
    user_data1.pop('position')
    user_data1['id'] = user_id
    user_data1['position_id'] = None
    user_data1['email'] = user_data3['email']
    assert response.json() == user_data1, 'Тело ответа не совпадает c вводимыми данными'


def test_delete_user_by_id(user_data2):
    # Case 1: Удаление несуществующего пользователя, проверка кода ответа
    response = client.delete(f'/users/{10000}')
    assert response.status_code == 404, 'Неверный код ответа, существующий пользователь'

    # Case 2: Удаление существующего пользователя, проверка кода ответа
    response = client.post('/users/', json={**user_data2})
    user_id = response.json().get('id')
    with TestingSessionLocal() as db:
        db_user = db.get(User, user_id)
        db_user_data = jsonable_encoder(db_user)
    response = client.delete(f'/users/{user_id}')
    assert response.status_code == 200, 'Неверный код ответа, существующий пользователь'

    # Case 3: Удаление существующего пользователя, проверка тела ответа
    db_user_data.pop('password')
    assert response.json() == db_user_data, 'Тело ответа не совпадает c вводимыми данными'

    # Case 4: Удаление существующего пользователя, проверка отсутствия данных в ДБ
    with (TestingSessionLocal() as db):
        is_exist = db.query(User.id).where(User.id == user_id).first() is not None
    assert not is_exist, 'Объект не удален из БД'
