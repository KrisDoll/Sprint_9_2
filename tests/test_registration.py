import allure
from data.Handlers import Handlers
from data.conftest import api_client, registration_data


@allure.suite("Регистрация пользователя")
class TestRegistration:

    @allure.description("Регистрация нового пользователя")
    @allure.title("200 ОК при регистрации нового пользователя с уникальным email")
    def test_registration(self, api_client, registration_data):
        response = api_client.post(
            endpoint=Handlers.SIGNUP,
            json=registration_data
        )
        assert response.status_code == 201, f"ОР: 201, ФР: {response.status_code}"

    @allure.description("Повторная регистрация пользователя")
    @allure.title("400 при регистрации пользователя с не уникальным email")
    def test_registration_false(self, api_client, registration_data):
        response = api_client.post(
            endpoint=Handlers.SIGNUP,
            json=registration_data
        )
        response_duplicate = api_client.post(
            endpoint=Handlers.SIGNUP,
            json=registration_data
        )
        assert response_duplicate.status_code == 400, f"ОР: 400, ФР: {response_duplicate.status_code}"

