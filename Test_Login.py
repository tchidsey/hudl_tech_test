import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.email_field = (By.ID, 'email')
        self.password_field = (By.ID, 'password')
        self.login_button = (By.ID, 'logIn')
        

    def enter_email(self, email):
        self.driver.find_element(*self.email_field).send_keys(email)

    def clear_email(self):
         self.driver.find_element(*self.email_field).clear

    def enter_password(self, password):
        self.driver.find_element(*self.password_field).send_keys(password)

    def clear_password(self):
        self.driver.find_element(*self.password_field).clear    

    def click_login_button(self):
        self.driver.find_element(By.ID, 'logIn').click()


class HelpPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.help_link = (By.XPATH, "//a[@data-qa-id='need-help-link']")

    def click_help_link(self):
        self.driver.find_element(*self.help_link).click()


class BackButton(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def click_back_button(self):
        self.driver.back()
        self.element = self.driver.find_element(By.XPATH, '//*[@id="app"]/section/a/svg/path')
        button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.element))
        button.click

class OrgLogIn(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def click_org_login(self):
        self.org_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/section/div[2]/div/form/div/a/button')
        self.org_button.click

class SignUp(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def click_signup_button(self):
       self.link = self.driver.find_element(By.XPATH,  '//a[contains(@href,"/register/signup")]') 
       self.element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.link))
       self.element.click 

class HudlTests(unittest.TestCase):
    def setUp(self):
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(service=Service(executable_path=ChromeDriverManager().install()), options=options)
        self.driver.get('https://www.hudl.com/login')


    def test_login(self):
        login_page = LoginPage(self.driver)
        login_page.enter_email('username')
        login_page.enter_password('password')
        login_page.click_login_button()
        self.assertIn('/home', (By.LINK_TEXT, '/home'))   
       
    def test_help_link(self):
        help_page = HelpPage(self.driver)
        help_page.click_help_link()
        self.element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//h2[@data-qa-id='login-help-headline']")))
        self.assertEqual('Login Help', self.element.text)

    def test_sign_up_link(self):
        sign_up = SignUp(self.driver)
        sign_up.click_signup_button()
    
    def test_org_login(self):
        org_button = OrgLogIn(self.driver)
        org_button.click_org_login()
    
  
    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()