from . import LINKEDIN_WEBSITE

from .Types import Types

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


def wait_until_loading(driver: WebDriver, timeout: int = 10,
                       conditions=[EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'footer')),
                                   EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="nav-typeahead-wormhole"]'))]):
    try:
        for condition in conditions:
            WebDriverWait(driver, timeout).until(condition)

    except Exception as error:
        raise error


def is_linkedin_driver(driver: WebDriver) -> bool:
    return hasattr(driver, 'state')


def is_signed_in(driver: WebDriver) -> bool:
    try:
        driver.find_element_by_xpath('//*[@id="profile-nav-item"]')
        return True
    except:
        return False


def linkedin_url_type(linkedin_url: str) -> str or None:
    valid_linkedin_urls = ['in/', 'groups/', 'school/', 'company/']
    valid_linkedin_urls.extend(
        [LINKEDIN_WEBSITE+string for string in valid_linkedin_urls])
    if any([linkedin_url.startswith(string) for string in valid_linkedin_urls]):
        if linkedin_url.startswith(LINKEDIN_WEBSITE+'in/') or linkedin_url.startswith('in/'):
            return Types.PERSON
        if linkedin_url.startswith(LINKEDIN_WEBSITE+'groups/') or linkedin_url.startswith('groups/'):
            return Types.GROUPS
        if linkedin_url.startswith(LINKEDIN_WEBSITE+'school/') or linkedin_url.startswith('school/'):
            return Types.SCHOOL
        if linkedin_url.startswith(LINKEDIN_WEBSITE+'company/') or linkedin_url.startswith('company/'):
            return Types.COMPANY
    elif linkedin_url == LINKEDIN_WEBSITE or linkedin_url == LINKEDIN_WEBSITE+'feed':
        return None
    else:
        raise Exception('It\'s not a valid linkedin url.')


def scroll_to(driver: WebDriver, x, y, top_margin=120, left=0):
    driver.execute_script('scroll({x}, {y})'.format(
        x=left if isinstance(left, int) else x, y=y if y-top_margin < 0 else y-top_margin))
