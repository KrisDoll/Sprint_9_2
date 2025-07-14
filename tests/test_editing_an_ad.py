import allure
import pytest
from data.Handlers import Handlers
from data.conftest import api_client, registration_data, create_user, ad_data, image_files, create_test_listing, auth_token, another_auth_token

@allure.suite("Редактирование объявления")
class TestEditingAnAd:


    @allure.description("Редактирование любого поля объявления")
    @allure.title("200 ОК при редактировании названия")
    def test_update_ad_success(self, create_user, api_client, auth_token, ad_data, image_files, create_test_listing):
        headers = {
            "Authorization": f"Bearer {auth_token}",
            "Accept": "application/json"
        }
        ad_id = create_test_listing
        ad_field = "name"
        new_value = "Кристиночка молодец"
        ad_data[ad_field] = new_value
        response = api_client.patch(
            endpoint=f"{Handlers.UPDATE_LISTING}/{ad_id}",
            headers=headers,
            data=ad_data,
            files=image_files
        )
        assert response.status_code == 200, f"ОР: 200, ФР: {response.status_code}"

    @allure.description("Редактирование объявления, созданного не тем пользователем, под токеном которого производится редактирование")
    @allure.title("200 ОК при редактировании названия")
    def test_edit_ad_by_different_user(self, create_user, api_client, auth_token, another_auth_token, ad_data, create_test_listing):
        ad_id = create_test_listing
        headers = {
            "Authorization": f"Bearer {another_auth_token}",
            "Accept": "application/json"
        }
        ad_data['name'] = "Попытка редактирования другим пользователем"

        response = api_client.patch(
            endpoint=f"{Handlers.UPDATE_LISTING}/{ad_id}",
            headers=headers,
            data=ad_data,
            files=None
        )
        assert response.status_code == 401, f"ОР: 401, ФР: {response.status_code}"