from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import data
import helpers


class UrbanRoutesPage:
    CAMPO_DE = (By.ID, "from")
    CAMPO_PARA = (By.ID, "to")

    TAXI_BUTTON = (
        By.XPATH,
        '//button[contains(text(), "Chamar um táxi")]'
    )

    CARD_COMFORT_PLAN = (
        By.XPATH,
        '//div[contains(@class, "tcard")]'
        '//div[contains(text(), "Comfort")]'
    )

    SELECTED_COMFORT_PLAN = (
        By.XPATH,
        '//div[contains(@class, "tcard") and '
        'contains(@class, "active")]'
        '//div[contains(@class, "tcard-title")]'
    )

    PHONE_NUMBER_CONTROL = (By.CLASS_NAME, "np-text")
    PHONE_NUMBER_INPUT = (By.ID, "phone")
    PHONE_NUMBER_CODE_INPUT = (By.ID, "code")
    PHONE_NUMBER_NEXT_BUTTON = (By.CSS_SELECTOR, ".full")
    PHONE_NUMBER_CONFIRM_BUTTON = (
        By.XPATH,
        '//button[contains(text(), "Confirm")]'
    )

    PAYMENT_METHOD_SELECT = (By.CLASS_NAME, "pp-text")
    ADD_CARD_CONTROL = (By.CLASS_NAME, "pp-plus")
    CARD_NUMBER_INPUT = (By.ID, "number")
    CARD_CODE_INPUT = (By.ID, "code")
    CARD_CREDENTIALS_CONFIRM_BUTTON = (
        By.XPATH,
        '//button[text()="Adicionar"]'
    )
    CLOSE_BUTTON_PAYMENT_METHOD = (
        By.XPATH,
        '//button[contains(@class, "close")]'
    )
    CURRENT_PAYMENT_METHOD = (By.CLASS_NAME, "pp-text")

    MESSAGE_FOR_DRIVER = (
        By.XPATH,
        '//input[@placeholder="Enviar mensagem ao motorista..."]'
    )

    OPTION_SWITCHES = (By.CLASS_NAME, "switch")
    OPTION_SWITCHES_INPUTS = (By.CLASS_NAME, "switch-input")

    ADD_ENUMERABLE_OPTION = (By.CLASS_NAME, "counter-plus")
    AMOUNT_OF_ENUMERABLE_OPTION = (By.CLASS_NAME, "counter-value")

    ORDER_CAR_BUTTON = (
        By.XPATH,
        '//button[contains(text(), "Pedir um táxi")]'
    )
    ORDER_POPUP = (By.CLASS_NAME, "order-header-title")
    DRIVER_WAIT_TIME = (By.CLASS_NAME, "order-header-time")
    ORDER_DRIVER_RATING = (By.CLASS_NAME, "driver-rating")
    ORDER_DRIVER_IMAGE = (By.CLASS_NAME, "driver-photo")
    ORDER_DRIVER_NAME = (By.CLASS_NAME, "driver-name")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def _wait_for(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        )

    def _click(self, locator):
        element = self.wait.until(
            EC.element_to_be_clickable(locator)
        )
        element.click()
        return element

    def set_from_field(self, from_field):
        field = self._wait_for(self.CAMPO_DE)
        field.clear()
        field.send_keys(from_field)

    def set_to_field(self, to_field):
        field = self._wait_for(self.CAMPO_PARA)
        field.clear()
        field.send_keys(to_field)

    def set_route(self, from_field, to_field):
        self.driver.get(data.URBAN_ROUTES_URL)
        self.set_from_field(from_field)
        self.set_to_field(to_field)

    def get_from(self):
        return self._wait_for(self.CAMPO_DE).get_attribute("value")

    def get_to(self):
        return self._wait_for(self.CAMPO_PARA).get_attribute("value")

    def assert_route(self, from_field, to_field):
        assert self.get_from() == from_field
        assert self.get_to() == to_field

    def click_taxi_button(self):
        self._click(self.TAXI_BUTTON)

    def click_comfort_plan_card(self):
        self._click(self.CARD_COMFORT_PLAN)

    def select_comfort_plan(self):
        self.click_taxi_button()
        self.click_comfort_plan_card()

    def assert_comfort_plan_selected(self):
        selected = self._wait_for(self.SELECTED_COMFORT_PLAN)
        assert "Comfort" in selected.text

    def set_phone_number(self, phone_number):
        self._click(self.PHONE_NUMBER_CONTROL)

        phone_field = self._wait_for(self.PHONE_NUMBER_INPUT)
        phone_field.clear()
        phone_field.send_keys(phone_number)

        self._click(self.PHONE_NUMBER_NEXT_BUTTON)

        code = helpers.retrieve_phone_code(self.driver)
        code_field = self._wait_for(self.PHONE_NUMBER_CODE_INPUT)
        code_field.send_keys(code)

        self._click(self.PHONE_NUMBER_CONFIRM_BUTTON)

    def assert_phone_number(self, phone_number):
        assert phone_number in self._wait_for(
            self.PHONE_NUMBER_CONTROL
        ).text

    def set_card_info(self, card_number, card_code):
        self._click(self.PAYMENT_METHOD_SELECT)
        self._click(self.ADD_CARD_CONTROL)

        number_field = self._wait_for(self.CARD_NUMBER_INPUT)
        number_field.clear()
        number_field.send_keys(card_number)

        code_field = self._wait_for(self.CARD_CODE_INPUT)
        code_field.clear()
        code_field.send_keys(card_code)
        code_field.send_keys(Keys.TAB)

        self._click(self.CARD_CREDENTIALS_CONFIRM_BUTTON)
        self._click(self.CLOSE_BUTTON_PAYMENT_METHOD)

    def get_current_payment_method(self):
        return self._wait_for(
            self.CURRENT_PAYMENT_METHOD
        ).text

    def set_message_for_driver(self, message):
        field = self._wait_for(self.MESSAGE_FOR_DRIVER)
        field.clear()
        field.send_keys(message)

    def get_message_for_driver(self):
        return self._wait_for(
            self.MESSAGE_FOR_DRIVER
        ).get_attribute("value")

    def click_blanket_and_handkerchiefs_option(self):
        switches = self.wait.until(
            EC.presence_of_all_elements_located(self.OPTION_SWITCHES)
        )
        switches[0].click()

    def get_blanket_and_handkerchiefs_option_checked(self):
        inputs = self.driver.find_elements(
            *self.OPTION_SWITCHES_INPUTS
        )
        return inputs[0].is_selected()

    def add_ice_cream(self, amount):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(
                self.ADD_ENUMERABLE_OPTION
            )
        )
        for _ in range(amount):
            buttons[0].click()

    def get_amount_of_ice_cream(self):
        values = self.wait.until(
            EC.presence_of_all_elements_located(
                self.AMOUNT_OF_ENUMERABLE_OPTION
            )
        )
        return int(values[0].text)

    def click_order_taxi_button(self):
        self._click(self.ORDER_CAR_BUTTON)

    def wait_order_taxi_popup(self):
        return self._wait_for(self.ORDER_POPUP)

    def wait_driver_info(self):
        self._wait_for(self.ORDER_DRIVER_NAME)
        self._wait_for(self.ORDER_DRIVER_RATING)
        self._wait_for(self.ORDER_DRIVER_IMAGE)

    def get_driver_info(self):
        name = self._wait_for(self.ORDER_DRIVER_NAME).text
        rating = self._wait_for(self.ORDER_DRIVER_RATING).text
        image = self._wait_for(self.ORDER_DRIVER_IMAGE).get_attribute("src")
        return name, rating, image
