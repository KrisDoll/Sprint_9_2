import allure
import pytest
from data.Handlers import Handlers
from data.conftest import api_client, registration_data

@allure.suite("Авторизация пользователя")
class TestAuthorization:
    @allure.description("Успешная авторизация пользователя")
    @allure.title("200 ОК при авторизации ранее зарегистрированного пользователя")
    def test_authorization(self, api_client, registration_data):
        response = api_client.post(
            endpoint=Handlers.SIGNUP,
            json=registration_data
        )
        login_payload = {
            "email": registration_data["email"],
            "password": registration_data["password"]
        }
        response_login = api_client.post(
            endpoint=Handlers.AUTHORIZATION,
            json=login_payload
        )
        assert response_login.status_code == 201, f"ОР: 201, ФР: {response_login.status_code}"
