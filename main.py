
import pytest
import data
import helpers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from pages import UrbanRoutesPage


class TestUrbanRoutes:

    @classmethod
    def setup_class(cls):
        # Verifica se o servidor está acessível
        if not helpers.is_url_reachable(data.URBAN_ROUTES_URL):
            pytest.skip(
                "O servidor Urban Routes não está acessível."
            )

        # Habilita os logs de rede para recuperar o código SMS
        options = Options()
        options.set_capability(
            "goog:loggingPrefs",
            {"performance": "ALL"}
        )

        cls.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )

        cls.driver.implicitly_wait(5)

        # Dados dos testes
        cls.from_field = data.ADDRESS_FROM
        cls.to_field = data.ADDRESS_TO
        cls.phone_number = data.PHONE_NUMBER
        cls.card_number = data.CARD_NUMBER
        cls.card_code = data.CARD_CODE
        cls.message_for_driver = data.MESSAGE_FOR_DRIVER

    @classmethod
    def teardown_class(cls):
        # Fecha o navegador ao finalizar os testes
        if hasattr(cls, "driver"):
            cls.driver.quit()

    # TESTE 1: Definir o endereço
    def test_set_route(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.assert_route(
            self.from_field,
            self.to_field
        )

    # TESTE 2: Selecionar o plano Comfort
    def test_select_comfort_plan(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.select_comfort_plan()
        page.assert_comfort_plan_selected()

    # TESTE 3: Preencher e confirmar o telefone
    def test_fill_phone_number(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.select_comfort_plan()
        page.set_phone_number(self.phone_number)

        page.assert_phone_number(self.phone_number)

    # TESTE 4: Adicionar cartão de crédito
    def test_set_card_info(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.select_comfort_plan()
        page.set_phone_number(self.phone_number)

        page.set_card_info(
            self.card_number,
            self.card_code
        )

        assert page.get_current_payment_method() == "Cartão"

    # TESTE 5: Escrever comentário para o motorista
    def test_set_message_for_driver(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.select_comfort_plan()

        page.set_message_for_driver(
            self.message_for_driver
        )

        assert (
            page.get_message_for_driver()
            == self.message_for_driver
        )

    # TESTE 6: Pedir cobertor e lenços
    def test_blanket_and_handkerchiefs_option(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.select_comfort_plan()
        page.click_blanket_and_handkerchiefs_option()

        assert page.get_blanket_and_handkerchiefs_option_checked()

    # TESTE 7: Pedir dois sorvetes
    def test_add_ice_cream(self):
        page = UrbanRoutesPage(self.driver)

        page.set_route(
            self.from_field,
            self.to_field
        )

        page.select_comfort_plan()
        page.add_ice_cream(2)

        assert page.get_amount_of_ice_cream() == 2

    # TESTE 8: Solicitar táxi e verificar o modal de busca
    def test_car_search_model_appears(self):
        page = UrbanRoutesPage(self.driver)

        # Define a rota
        page.set_route(
            self.from_field,
            self.to_field
        )

        # Seleciona Comfort
        page.select_comfort_plan()
        page.assert_comfort_plan_selected()

        # Confirma o telefone
        page.set_phone_number(self.phone_number)
        page.assert_phone_number(self.phone_number)

        # Adiciona o cartão
        page.set_card_info(
            self.card_number,
            self.card_code
        )
        assert page.get_current_payment_method() == "Cartão"

        # Adiciona o comentário para o motorista
        page.set_message_for_driver(
            self.message_for_driver
        )
        assert (
            page.get_message_for_driver()
            == self.message_for_driver
        )

        # Ativa cobertor e lenços
        page.click_blanket_and_handkerchiefs_option()
        assert page.get_blanket_and_handkerchiefs_option_checked()

        # Adiciona dois sorvetes
        page.add_ice_cream(2)
        assert page.get_amount_of_ice_cream() == 2

        # Solicita o táxi
        page.click_order_taxi_button()

        # Verifica se o modal de busca aparece
        assert page.is_order_taxi_popup_displayed()
