import pytest
import allure
import os
from api.api import ApiClient
from data.URLs import Urls
from data.generator import TestGenerator
from data.Handlers import Handlers


@pytest.fixture
def api_client():
    """Фикстура для создания клиента API с базовым URL"""
    with allure.step("Создание API клиента с базовым URL"):
        return ApiClient(Urls.BASE_URL)


@pytest.fixture
def registration_data():
    with allure.step("Генерация тестовых данных для регистрации пользователя"):
        fake_user = TestGenerator.generate_user()
        data = {
            "email": fake_user.get("email"),
            "password": fake_user.get("password"),
            "submitPassword": fake_user.get("password")
        }
        allure.attach(str(data), name="Регистрационные данные", attachment_type=allure.attachment_type.TEXT)
        return data


@pytest.fixture
def create_user(api_client, registration_data):
    with allure.step("Создание нового пользователя"):
        response = api_client.post(
            endpoint=Handlers.SIGNUP,
            json=registration_data
        )

        allure.attach(
            f"Request: POST {Urls.BASE_URL}{Handlers.SIGNUP}\n"
            f"Request Body: {registration_data}\n"
            f"Response Status: {response.status_code}\n"
            f"Response Body: {response.text}",
            name="Детали запроса/ответа",
            attachment_type=allure.attachment_type.TEXT
        )

        assert response.status_code == 201
        user = {
            "email": registration_data.get("email"),
            "password": registration_data.get("password")
        }
        return user



def get_image_files_paths():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # папка conftest.py
    project_root = os.path.dirname(base_dir)  # корень проекта
    data_folder = os.path.join(project_root, 'data')
    image_filenames = ['image1.jpg', 'image2.jpg', 'image3.jpg']
    image_paths = [os.path.join(data_folder, filename) for filename in image_filenames]
    return image_paths


@pytest.fixture
def image_files():
    image_paths = get_image_files_paths()
    files = []
    for path in image_paths:
        with open(path, 'rb') as f:
            image_data = f.read()
        filename = os.path.basename(path)
        files.append(('images', (filename, image_data, 'image/jpeg')))
    return files


@pytest.fixture
def ad_data():
    return TestGenerator.create_listing_data()


@pytest.fixture
def auth_token(api_client, create_user):
    with allure.step("Получение токена аутентификации"):
        payload = create_user

        response = api_client.post(
            endpoint=Handlers.AUTHORIZATION,
            json=payload
        )

        allure.attach(
            f"Request: POST {Urls.BASE_URL}{Handlers.AUTHORIZATION}\n"
            f"Request Body: {payload}\n"
            f"Response Status: {response.status_code}\n"
            f"Response Body: {response.text}",
            name="Детали запроса/ответа аутентификации",
            attachment_type=allure.attachment_type.TEXT
        )
        response_data = response.json()
        token_data = response_data["token"]
        token = token_data["access_token"]
        return token


@pytest.fixture
def another_auth_token(api_client):
    with allure.step("Создание и аутентификация другого пользователя"):
        another_user = {
            "email": "another_user@example.com",
            "password": "another_password123",
            "submitPassword": "another_password123"
        }
        reg_response = api_client.post(
            endpoint=Handlers.SIGNUP,
            json=another_user
        )
        login_response = api_client.post(
            endpoint=Handlers.AUTHORIZATION,
            json=another_user
        )
        return login_response.json()["token"]["access_token"]



@pytest.fixture
def create_test_listing(api_client, auth_token, ad_data, image_files):
    data = ad_data
    test_files = image_files
    headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json"
    }
    response = api_client.post(
        endpoint=Handlers.CREATE_LISTING,
        headers=headers,
        data=data,
        files=test_files
    )
    response_json = response.json()
    return response_json['id']

