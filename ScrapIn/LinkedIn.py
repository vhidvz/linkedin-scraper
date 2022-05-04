
from . import LINKEDIN_WEBSITE

from .States import States

from .Actions import login, logout
from .Actions import top_down_scroll

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from selenium.webdriver.remote.webdriver import WebDriver


def LinkedIn(cls: Firefox or Chrome, **kwargs) -> WebDriver:
    class LinkedIn(cls):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.get(LINKEDIN_WEBSITE)
            self.state = States.MAIN

        def login(self, username, password):
            return login(self.driver, username, password)

        def logout(self):
            return logout(self.driver)

        def top_down_scroll(self, **kwargs):
            return top_down_scroll(self.driver, **kwargs)

    return LinkedIn(**kwargs)
