import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class UITests:
    def __init__(self, driver):
        self.driver = driver
        self.test_search_results()

    def test_search_results(self):
        """Результаты поисковой выдачи"""
        search_input = self.driver.find_element(by=By.NAME, value='search')
        search_input.send_keys('macbook')
        search_input.send_keys(Keys.RETURN)

        time.sleep(10)

        assert 'Search - macbook' in self.driver.page_source

        search_input = self.driver.find_element(by=By.NAME, value='search')
        search_input.clear()

        search_input.send_keys('iphone')
        search_input.send_keys(Keys.RETURN)

        time.sleep(10)

        assert 'Search - iphone' in self.driver.page_source

        print('Search results test passed')
        self.test_add_to_cart()

    def test_add_to_cart(self):
        """Добавление в корзину"""
        add_to_cart_button = self.driver.find_element(by=By.XPATH,
                                                      value='//*[@id="content"]/div[3]/div/div/div[2]/div[2]/button[1]')
        add_to_cart_button.click()

        time.sleep(10)

        shopping_cart = self.driver.find_element(by=By.CLASS_NAME, value='fa-shopping-cart')
        shopping_cart.click()

        time.sleep(10)

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
        remove_button = self.driver.find_element(by=By.XPATH,
                                                 value='//*[@id="content"]/form/div/table/tbody/tr/td[4]/div/span/button[2]')
        remove_button.click()

        time.sleep(10)

        assert 'Shopping Cart' in self.driver.page_source
        assert 'Your shopping cart is empty!' in self.driver.page_source

        print('Deletion from cart test passed')
        self.test_return_after_deletion()

    def test_return_after_deletion(self):
        """Возвращение в магазин из пустой корзины"""
        continue_button = self.driver.find_element(by=By.LINK_TEXT, value='Continue')
        continue_button.click()

        time.sleep(10)

        assert 'Your Store' in self.driver.page_source
        assert 'Featured' in self.driver.page_source
        assert 'Search' in self.driver.page_source

        print('Return after deletion test passed')
        self.test_update()

    def test_update(self):
        """Обновление товара по кнопке update"""
        search_input = self.driver.find_element(by=By.NAME, value='search')
        search_input.send_keys('macbook')
        search_input.send_keys(Keys.RETURN)

        time.sleep(10)

        add_to_cart_button = self.driver.find_element(by=By.XPATH,
                                                      value='//*[@id="content"]/div[3]/div/div/div[2]/div[2]/button[1]')
        add_to_cart_button.click()

        time.sleep(10)

        shopping_cart = self.driver.find_element(by=By.CLASS_NAME, value='fa-shopping-cart')
        shopping_cart.click()

        time.sleep(10)

        update_button = self.driver.find_element(by=By.CLASS_NAME, value='fa-refresh')
        update_button.click()

        time.sleep(10)

        assert 'Success: You have modified your shopping cart!' in self.driver.page_source

        print('Update test passed')
        self.test_coupon()

    def test_coupon(self):
        """Ввод номера купона"""
        coupon_button = self.driver.find_element(by=By.LINK_TEXT, value='Use Coupon Code')
        coupon_button.click()

        time.sleep(10)

        coupon_input = self.driver.find_element(by=By.ID, value='input-coupon')
        coupon_input.send_keys('88888')
        apply_button = self.driver.find_element(by=By.ID, value='button-coupon')
        apply_button.click()

        time.sleep(10)

        assert 'Coupon is either invalid, expired or reached its usage limit!' in self.driver.page_source

        print('Coupon test passed')
        self.test_certificate()

    def test_certificate(self):
        """Ввод номера подарочного сертификата"""
        certificate_button = self.driver.find_element(by=By.LINK_TEXT, value='Use Gift Certificate')
        certificate_button.click()

        time.sleep(10)

        certificate_input = self.driver.find_element(by=By.ID, value='input-voucher')
        certificate_input.send_keys('12345')
        apply_button = self.driver.find_element(by=By.ID, value='button-voucher')
        apply_button.click()

        time.sleep(10)

        assert 'Gift Certificate is either invalid or the balance has been used up!' in self.driver.page_source

        print('Certificate test passed')
        self.test_continue_shopping()

    def test_continue_shopping(self):
        """Продолжение покупок после добавления товара в корзину"""
        continue_shopping_button = self.driver.find_element(by=By.LINK_TEXT, value='Continue Shopping')
        continue_shopping_button.click()

        time.sleep(10)

        assert 'Your Store' in self.driver.page_source
        assert 'Featured' in self.driver.page_source
        assert 'Search' in self.driver.page_source

        print('Continue shopping test passed')
        self.test_checkout()

    def test_checkout(self):
        """Оплата товара"""
        shopping_cart = self.driver.find_element(by=By.CLASS_NAME, value='fa-shopping-cart')
        shopping_cart.click()

        time.sleep(10)

        checkout_button = self.driver.find_element(by=By.LINK_TEXT, value='Checkout')
        checkout_button.click()

        time.sleep(10)

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
    tests = UITests(driver)
    driver.close()
