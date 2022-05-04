import sys

from time import time
from random import randint

from collections import deque

from ScrapIn import Types

from ScrapIn import Person
from ScrapIn import LinkedIn

from ScrapIn.Actions import login
from ScrapIn.Actions import logout

from selenium.webdriver import Chrome
from selenium.webdriver import Firefox

from ScrapIn.Utils import linkedin_url_type
from ScrapIn.Utils import wait_until_loading


if __name__ == "__main__":
    linkedin = LinkedIn(cls=Chrome)

    login(linkedin, '[your_email]', '[your_password]')
    wait_until_loading(linkedin)

    person = Person('https://www.linkedin.com/in/[start_point]/',
                    driver=linkedin).scrape()

    queue = deque(maxlen=1000)

    queue.extend(person.data['people_also_viewed'])

    while len(queue) > 0:
        try:
            sys.stdout.flush()
            queue.reverse()
            queue.rotate(randint(0, 1000))
            p_link = queue.pop()['link']
            print(p_link, end='')

            if linkedin_url_type(p_link) == Types.PERSON:
                start = time()
                person = Person(p_link, driver=linkedin).scrape()
                print(' - duration', time()-start)
                queue.extend(person.data['people_also_viewed'])
        except:
            pass
