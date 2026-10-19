
import pytest
import data
import helpers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from page import UrbanRoutesPage


class TestUrbanRoutes:
    driver = None
    from_field = data.ADDRESS_FROM
    to_field = data.ADDRESS_TO
    phone_number = data.PHONE_NUMBER

    @classmethod
    def setup_class(cls):
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            pytest.skip("O servidor Urban Routes não está acessível.")

        options = Options()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        cls.driver.execute_cdp_cmd(
            "Network.enable", {}
        )

    def test_set_route(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.assert_route(self.from_field, self.to_field)

    def test_select_plan(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.select_comfort_plan()
        page.assert_comfort_plan_selected()

    def test_fill_phone_number(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.select_comfort_plan()
        page.set_phone_number(self.phone_number)
        page.assert_phone_number(self.phone_number)

    def test_fill_card(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.select_comfort_plan()
        page.set_card_info(data.CARD_NUMBER, data.CARD_CODE)
        assert page.get_current_payment_method()

    def test_comment_for_driver(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.select_comfort_plan()
        message = data.MESSAGE_FOR_DRIVER
        page.set_message_for_driver(message)
        assert page.get_message_for_driver() == message

    def test_order_blanket_and_handkerchiefs(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.select_comfort_plan()
        page.click_blanket_and_handkerchiefs_option()
        assert page.get_blanket_and_handkerchiefs_option_checked()

    def test_order_2_ice_creams(self):
        page = UrbanRoutesPage(self.driver)
        page.set_route(self.from_field, self.to_field)
        page.select_comfort_plan()
        page.add_ice_cream(2)
        assert page.get_amount_of_ice_cream() == 2

    @classmethod
    def teardown_class(cls):
        if cls.driver is not None:
            cls.driver.quit()
