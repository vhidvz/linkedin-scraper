import json

from .Types import Types
from .States import States

from .Utils import scroll_to
from .Utils import is_signed_in
from .Utils import linkedin_url_type
from .Utils import is_linkedin_driver
from .Utils import wait_until_loading

from .Actions import top_down_scroll

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class People(object):
    def __init__(self):
        self.img: str = ''
        self.name: str = ''
        self.link: str = ''
        self.headline: str = ''


class Intro(People):
    def __init__(self):
        self.region: str = ''
        self.connections: int = 0


class About(object):
    def __init__(self):
        self.text: str = ''
        self.links: list = []


class Person(object):

    def __init__(self, linkedin_url: str, driver: WebDriver):
        self.linkedin_url = linkedin_url
        self.driver = driver
        self.data = {}

    def scrape(self):
        if is_signed_in(self.driver) and linkedin_url_type(self.linkedin_url) == Types.PERSON:
            self.driver.get(self.linkedin_url)
            wait_until_loading(self.driver)
            top_down_scroll(self.driver)

            self.data.update({'intro': self.__get_intro__()})
            self.data.update(
                {'people_also_viewed': self.__get_people_also_viewed__()})
            self.data.update({'about': self.__get_about__()})

        else:
            raise Exception(
                'Please sign in before any type of scrapping or give a true type of linkedin url.')
        return self

    def __get_intro__(self) -> dict:
        intro = Intro()

        intro.link = self.linkedin_url
        intro.img = self.driver.find_element_by_xpath(
            '/html/body/div/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[1]/div[1]/div/div//img').get_attribute('src')
        intro.name = self.driver.find_element_by_xpath(
            '/html/body/div/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[1]/li[1]').text
        intro.region = self.driver.find_element_by_xpath(
            '/html/body/div/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[2]/li[1]').text
        intro.headline = self.driver.find_element_by_xpath(
            '/html/body/div/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/h2').text
        try:
            intro.connections = int(self.driver.find_element_by_xpath(
                '/html/body/div/div[6]/div[3]/div/div/div/div/div[2]/div[1]/div[1]/div/section/div[2]/div[2]/div[1]/ul[2]/li[2]//span').text.split()[0])
        except:
            pass

        return intro.__dict__

    def __get_people_also_viewed__(self) -> list:
        peoples = []

        for item in self.driver.find_elements_by_xpath('/html/body/div/div[6]/div[3]/div/div/div/div/div[2]/div[2]/div/div/section/ul/li'):
            people = People()
            people.img = item.find_element_by_xpath(
                './/img').get_attribute('src')
            people.name = item.find_element_by_xpath(
                './/h3').text.split('\n')[0]
            people.link = item.find_element_by_xpath(
                './/a').get_attribute('href')
            people.headline = item.find_element_by_xpath('.//p').text
            peoples.append(people.__dict__)

        return peoples

    def __get_about__(self) -> dict:
        about = About()

        aboutElement = self.driver.find_element_by_class_name(
            'pv-about-section')
        if EC._element_if_visible(aboutElement):
            try:
                scroll_to(self.driver, **aboutElement.location)
                anchorSeeMore = aboutElement.find_element_by_xpath(
                    './/span/a[text()="see more"]')
                anchorSeeMore.click()
            except:
                pass
            about.text = aboutElement.find_element_by_xpath(
                './/p[contains(@class, "pv-about__summary-text")]').text

            for item_link in aboutElement.find_elements_by_class_name('pv-treasury-list-preview__treasury-item-link'):
                about.links.append(item_link.get_attribute('href'))

        return about.__dict__

    def json(self, indent=None):
        return json.dumps(self.data, indent=indent)
