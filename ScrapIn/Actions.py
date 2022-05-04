from . import LINKEDIN_WEBSITE

from .States import States

from .Utils import is_signed_in
from .Utils import wait_until_loading
from .Utils import is_linkedin_driver

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


def login(driver: WebDriver, username: str, password: str,
          linkedin_url=LINKEDIN_WEBSITE) -> WebDriver:
    if is_linkedin_driver(driver):
        assert driver.state == States.MAIN,\
            'To login to the LinkedIn website your state must be in the State.MAIN.'
    else:
        url = driver.execute_script('return window.location.href')
        if not url == linkedin_url and not is_signed_in(driver):
            driver.get(LINKEDIN_WEBSITE)

    try:
        inputUsername = driver.find_element_by_xpath(
            '/html/body/nav/section[2]/form/div[1]/div[1]/input')
        inputUsername.send_keys(username)

        inputPassword = driver.find_element_by_xpath(
            '/html/body/nav/section[2]/form/div[1]/div[2]/input')
        inputPassword.send_keys(password)

        buttonSignIn = driver.find_element_by_xpath(
            '/html/body/nav/section[2]/form/div[2]/button')
        buttonSignIn.click()

        if is_linkedin_driver(driver):
            driver.state = States.HOME

    except Exception as error:
        raise error

    return driver


def logout(driver: WebDriver) -> WebDriver:
    if is_linkedin_driver(driver):
        assert not (driver.state == States.INIT or driver.state ==
                    States.MAIN), 'Can\'t logout before logged in'

    try:
        driver.get(LINKEDIN_WEBSITE+'m/logout/')
        wait_until_loading(driver, conditions=[EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#artdeco-modal-outlet'))])
        driver.get(LINKEDIN_WEBSITE)

        if is_linkedin_driver(driver):
            driver.state = States.MAIN

    except Exception as error:
        raise error

    return driver


def top_down_scroll(driver: WebDriver, callback=None, pix_step=5):
    recall = False
    start_scroll = 0
    while True:
        scrollHeight = driver.execute_script(
            'return document.body.scrollHeight;')
        for i in range(start_scroll, scrollHeight, pix_step):
            driver.execute_script('scroll(0, {})'.format(i))
            try:
                flag_recall, flag_break = callback(driver, recall)
                if flag_recall:
                    recall = True
                if flag_break:
                    return
            except:
                continue
        if scrollHeight == driver.execute_script(
                'return document.body.scrollHeight;'):
            break
        else:
            start_scroll = scrollHeight
