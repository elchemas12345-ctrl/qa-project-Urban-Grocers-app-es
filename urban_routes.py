# pages/urban_routes_page.py

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 20)

    # Localizadores
    address_input = (By.ID, "address-input")
    comfort_tariff = (By.ID, "tariff-comfort")
    phone_input = (By.ID, "phone-input")
    add_card_button = (By.ID, "add-card")
    card_number_input = (By.ID, "card-number")
    card_expiry_input = (By.ID, "card-expiry")
    card_cvv_input = (By.ID, "code")  # CVV
    card_link_button = (By.ID, "link-card")
    message_input = (By.ID, "message-input")
    blanket_checkbox = (By.ID, "extra-blanket")
    tissues_checkbox = (By.ID, "extra-tissues")
    ice_cream_quantity_input = (By.ID, "ice-cream-quantity")
    request_taxi_button = (By.ID, "request-taxi")
    driver_info_modal = (By.ID, "driver-info-modal")
    phone_code_input = (By.ID, "phone-code")

    # Métodos
    def set_address(self, address):
        addr_field = self.wait.until(EC.visibility_of_element_located(self.address_input))
        addr_field.clear()
        addr_field.send_keys(address)
        addr_field.send_keys(Keys.RETURN)

    def select_comfort_tariff(self):
        self.wait.until(EC.element_to_be_clickable(self.comfort_tariff)).click()

    def enter_phone_number(self, phone):
        phone_field = self.wait.until(EC.visibility_of_element_located(self.phone_input))
        phone_field.clear()
        phone_field.send_keys(phone)

    def add_credit_card(self, number, expiry, cvv):
        self.wait.until(EC.element_to_be_clickable(self.add_card_button)).click()
        self.wait.until(EC.visibility_of_element_located(self.card_number_input)).send_keys(number)
        self.driver.find_element(*self.card_expiry_input).send_keys(expiry)
        cvv_field = self.driver.find_element(*self.card_cvv_input)
        cvv_field.send_keys(cvv)
        cvv_field.send_keys(Keys.TAB)  # Desenfocar para habilitar botón
        self.wait.until(EC.element_to_be_clickable(self.card_link_button)).click()

    def confirm_phone_code(self, code):
        code_field = self.wait.until(EC.visibility_of_element_located(self.phone_code_input))
        code_field.send_keys(code)
        code_field.send_keys(Keys.RETURN)

    def write_message(self, message):
        msg_field = self.wait.until(EC.visibility_of_element_located(self.message_input))
        msg_field.send_keys(message)

    def request_extras(self, blanket=True, tissues=True, ice_cream_qty=0):
        if blanket:
            self.driver.find_element(*self.blanket_checkbox).click()
        if tissues:
            self.driver.find_element(*self.tissues_checkbox).click()
        if ice_cream_qty > 0:
            ice_input = self.driver.find_element(*self.ice_cream_quantity_input)
            ice_input.clear()
            ice_input.send_keys(str(ice_cream_qty))

    def request_taxi(self):
        self.driver.find_element(*self.request_taxi_button).click()

    def wait_for_driver_info(self):
        self.wait.until(EC.visibility_of_element_located(self.driver_info_modal))
        time.sleep(2)
