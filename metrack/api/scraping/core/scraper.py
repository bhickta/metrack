from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import frappe

class Selenium:
    def __init__(self, **kwargs) -> None:
        self.selenium_grid_url = kwargs.get("selenium_grid_url", 'http://selenium-chrome:4444/wd/hub')
        self.post_init()
    
    def post_init(self):
        self.set_chrome_options()

    def set_chrome_options(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self._get_chrome_driver()
        self._get_driver_wait()

    def _get_chrome_driver(self):
        self.driver = RemoteWebDriver(
            command_executor=self.selenium_grid_url,
            options=self.chrome_options
        )
    
    def _get_driver_wait(self):
        self.wait = WebDriverWait(self.driver, 10)
    
    def get_driver_and_wait(self) -> tuple[RemoteWebDriver, WebDriverWait]:
        return self.driver, self.wait
    
    def find_element(self, by, value):
        return self.driver.find_element(by, value)
    
    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)
    
    def get(self, url):
        return self.driver.get(url)
    
# Instantiate the Selenium class
selenium = Selenium()
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as clickable
from selenium.common.exceptions import TimeoutException