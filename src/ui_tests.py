import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class PageObjects:
    def __init__(self, driver):
        self.driver = driver

    def search_input(self):
        return self.driver.find_element(by=By.NAME, value='search')

    def add_to_cart_button(self):
        return self.driver.find_element(by=By.XPATH, value='//*[@id="content"]/div[3]/div/div/div[2]/div[2]/button[1]')

    def shopping_cart(self):
        return self.driver.find_element(by=By.CLASS_NAME, value='fa-shopping-cart')

    def remove_button(self):
        return self.driver.find_element(by=By.XPATH,
                                        value='//*[@id="content"]/form/div/table/tbody/tr/td[4]/div/span/button[2]')

    def continue_button(self):
        return self.driver.find_element(by=By.LINK_TEXT, value='Continue')

    def update_button(self):
        return self.driver.find_element(by=By.CLASS_NAME, value='fa-refresh')

    def coupon_button(self):
        return self.driver.find_element(by=By.LINK_TEXT, value='Use Coupon Code')

    def coupon_input(self):
        return self.driver.find_element(by=By.ID, value='input-coupon')

    def apply_coupon_button(self):
        return self.driver.find_element(by=By.ID, value='button-coupon')

    def certificate_button(self):
        return self.driver.find_element(by=By.LINK_TEXT, value='Use Gift Certificate')

    def certificate_input(self):
        return self.driver.find_element(by=By.ID, value='input-voucher')

    def apply_certificate_button(self):
        return self.driver.find_element(by=By.ID, value='button-voucher')

    def continue_shopping_button(self):
        return self.driver.find_element(by=By.LINK_TEXT, value='Continue Shopping')

    def checkout_button(self):
        return self.driver.find_element(by=By.LINK_TEXT, value='Checkout')


class UITests:
    def __init__(self, driver, page_objects):
        self.driver = driver
        self.page_objects = page_objects
        self.test_search_results()

    def test_search_results(self):
        """Результаты поисковой выдачи"""
        search_input = self.page_objects.search_input()
        search_input.send_keys('macbook')
        search_input.send_keys(Keys.RETURN)

        time.sleep(5)

        assert 'Search - macbook' in self.driver.page_source

        search_input = self.page_objects.search_input()
        search_input.clear()

        search_input.send_keys('iphone')
        search_input.send_keys(Keys.RETURN)

        time.sleep(5)

        assert 'Search - iphone' in self.driver.page_source

        print('Search results test passed')
        self.test_add_to_cart()

    def test_add_to_cart(self):
        """Добавление в корзину"""
        add_to_cart_button = self.page_objects.add_to_cart_button()
        add_to_cart_button.click()

        time.sleep(5)

        shopping_cart = self.page_objects.shopping_cart()
        shopping_cart.click()

        time.sleep(5)

        assert 'Shopping Cart' in self.driver.page_source
        assert 'Image' in self.driver.page_source
        assert 'Product Name' in self.driver.page_source
        assert 'Model' in self.driver.page_source
        assert 'Quantity' in self.driver.page_source
        assert 'Unit Price' in self.driver.page_source
        assert 'Total' in self.driver.page_source

        print('Add to cart test passed')
        self.test_delete_from_cart()

    def test_delete_from_cart(self):
        """Удаление из корзины"""
        remove_button = self.page_objects.remove_button()
        remove_button.click()

        time.sleep(5)

        assert 'Shopping Cart' in self.driver.page_source
        assert 'Your shopping cart is empty!' in self.driver.page_source

        print('Deletion from cart test passed')
        self.test_return_after_deletion()

    def test_return_after_deletion(self):
        """Возвращение в магазин из пустой корзины"""
        continue_button = self.page_objects.continue_button()
        continue_button.click()

        time.sleep(5)

        assert 'Your Store' in self.driver.page_source
        assert 'Featured' in self.driver.page_source
        assert 'Search' in self.driver.page_source

        print('Return after deletion test passed')
        self.test_update()

    def test_update(self):
        """Обновление товара по кнопке update"""
        search_input = self.page_objects.search_input()
        search_input.send_keys('macbook')
        search_input.send_keys(Keys.RETURN)

        time.sleep(5)

        add_to_cart_button = self.page_objects.add_to_cart_button()
        add_to_cart_button.click()

        time.sleep(5)

        shopping_cart = self.page_objects.shopping_cart()
        shopping_cart.click()

        time.sleep(5)

        update_button = self.page_objects.update_button()
        update_button.click()

        time.sleep(5)

        assert 'Success: You have modified your shopping cart!' in self.driver.page_source

        print('Update test passed')
        self.test_coupon()

    def test_coupon(self):
        """Ввод номера купона"""
        coupon_button = self.page_objects.coupon_button()
        coupon_button.click()

        time.sleep(5)

        coupon_input = self.page_objects.coupon_input()
        coupon_input.send_keys('88888')
        apply_button = self.page_objects.apply_coupon_button()
        apply_button.click()

        time.sleep(5)

        assert 'Coupon is either invalid, expired or reached its usage limit!' in self.driver.page_source

        print('Coupon test passed')
        self.test_certificate()

    def test_certificate(self):
        """Ввод номера подарочного сертификата"""
        certificate_button = self.page_objects.certificate_button()
        certificate_button.click()

        time.sleep(5)

        certificate_input = self.page_objects.certificate_input()
        certificate_input.send_keys('12345')
        apply_button = self.page_objects.apply_certificate_button()
        apply_button.click()

        time.sleep(5)

        assert 'Gift Certificate is either invalid or the balance has been used up!' in self.driver.page_source

        print('Certificate test passed')
        self.test_continue_shopping()

    def test_continue_shopping(self):
        """Продолжение покупок после добавления товара в корзину"""
        continue_shopping_button = self.page_objects.continue_shopping_button()
        continue_shopping_button.click()

        time.sleep(5)

        assert 'Your Store' in self.driver.page_source
        assert 'Featured' in self.driver.page_source
        assert 'Search' in self.driver.page_source

        print('Continue shopping test passed')
        self.test_checkout()

    def test_checkout(self):
        """Оплата товара"""
        shopping_cart = self.page_objects.shopping_cart()
        shopping_cart.click()

        time.sleep(5)

        checkout_button = self.page_objects.checkout_button()
        checkout_button.click()

        time.sleep(5)

        if '***' in self.driver.page_source:
            assert 'Products marked with *** are not available' in self.driver.page_source
        else:
            assert 'Checkout Options' in self.driver.page_source
            assert 'Billing Details' in self.driver.page_source
            assert 'Payment Method' in self.driver.page_source
            assert 'Confirm Order' in self.driver.page_source

        print('Checkout test passed')
        self.final_success()

    def final_success(self):
        print()
        print('=============')
        print('All tests passed')


if __name__ == '__main__':
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('http://tutorialsninja.com/demo/')
    page_objects = PageObjects(driver)
    tests = UITests(driver, page_objects)
    driver.close()
