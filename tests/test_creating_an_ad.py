import allure
import pytest
from data.Handlers import Handlers
from data.conftest import api_client, registration_data, create_user, ad_data, image_files, create_test_listing, auth_token


@allure.suite('Создание объявлений')
class TestAdCreation:
    @allure.description("Успешное создание объявления")
    @allure.title("200 ОК при создании нового объявления")
    @pytest.mark.usefixtures("create_test_listing")
    def test_create_ad_success(self, api_client, auth_token, ad_data, image_files):
        headers = {
        "Authorization": f"Bearer {auth_token}",
        "Accept": "application/json"
        }
        response = api_client.post(
            endpoint=Handlers.CREATE_LISTING,
            headers=headers,
            data=ad_data,
            files=image_files
        )
        assert response.status_code == 201, f"ОР: 201, ФР: {response.status_code}"
