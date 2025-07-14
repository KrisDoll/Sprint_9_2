import allure
import pytest
from data.Handlers import Handlers
from data.conftest import api_client, registration_data, create_user, ad_data, image_files, create_test_listing, auth_token, another_auth_token


@allure.suite("Удаление объявления")
class TestRemovalOfAd:

    @allure.description("Удаление объявления")
    @allure.title("200 ОК при удалении объявления")
    def test_delete_ad(self, auth_token, create_test_listing, api_client):
        ad_id = create_test_listing
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        }
        response = api_client.delete(
            endpoint=f"{Handlers.DELETE_LISTING}/{ad_id}",
            headers=headers
         )
        assert response.status_code == 200, f"ОР: 200, ФР: {response.status_code}"