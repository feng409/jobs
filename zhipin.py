# -*- coding: utf-8 -*-
# =============================================================================
#          Desc:
#        Author: chemf
#         Email: eoyohe@gmail.com
#      HomePage: eoyohe.cn
#       Version: 0.0.1
#    LastChange: 2020/2/28 8:44 PM
#       History:
# =============================================================================
import json
import time
import logging
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver, WebElement
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass

import coloredlogs
import yaml

with open('config.yaml') as f:
    config = yaml.load(f, yaml.FullLoader)

logger = logging.getLogger()
coloredlogs.install('INFO', logger=logger)

HOMEPAGE = 'https://zhipin.com'
LOGIN_URL = 'https://login.zhipin.com/?ka=header-login'


@dataclass
class JobItem:
    title: str
    wage: str
    company: str
    url: str


def init_selenium(load_cookies=False) -> RemoteWebDriver:
    options = ChromeOptions()
    script = '''
    Object.defineProperty(navigator, 'webdriver', {
        get: () => undefined
    })
    '''
    options.add_argument('--auto-open-devtools-for-tabs')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument("enable-features=NetworkServiceInProcess")
    browser = webdriver.Chrome(options=options)
    browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})
    browser.get(HOMEPAGE)
    browser.set_page_load_timeout(30)
    if load_cookies:
        logger.debug('load cookie')
        with open('cookie.json') as f:
            cookies = json.load(f)
        for cookie in cookies:
            try:
                browser.add_cookie(cookie)
            except Exception as e:
                print(cookie)
                raise e
    return browser


def login(browser: RemoteWebDriver):
    browser.get(LOGIN_URL)
    time.sleep(5)
    ele_tel = browser.find_element_by_css_selector('input[type="tel"]')
    ele_tel.send_keys(config['zhipin']['PHONE'])
    ele_passwd = browser.find_element_by_css_selector('input[type="password"]')
    ele_passwd.send_keys(config['zhipin']['PASSWORD'])
    ele_verify = browser.find_element_by_css_selector('div[id*="verrify"] > div > div > span')
    # todo auto press scroll bar
    with open('cookie.json', 'w') as f:
        f.write(json.dumps(browser.get_cookies()))


def say_hello(driver: RemoteWebDriver, url: str) -> None:
    """say hello to HR"""
    js_code = 'window.open("%s")' % url
    driver.execute_script(js_code)
    logger.info(driver.current_window_handle)
    time.sleep(30)
    driver.close()


def find_job(driver: RemoteWebDriver, job_url: str, page_count: int) -> List[JobItem]:
    items = []
    for page in range(1, page_count + 1):
        url = f'{job_url}&page={page}'
        _current_page_jobs = _find_job(driver, url)
        items.extend(_current_page_jobs)
    return items


def _find_job(driver: RemoteWebDriver, job_url: str) -> List[JobItem]:
    items = []
    try:
        wait = WebDriverWait(driver, 5)

        driver.get(job_url)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.job-list')))

        ele_jobs = driver.find_elements_by_css_selector('div.job-list ul > li')
        for ele_job in ele_jobs:
            ele_job = ele_job  # type: WebElement
            title = ele_job.find_element_by_css_selector('div.job-title').text
            wage = ele_job.find_element_by_css_selector('div.job-limit span.red').text
            company = ele_job.find_element_by_css_selector('div.company-text').text
            button = ele_job.find_element_by_css_selector('button.btn-startchat')
            say_hello_url = HOMEPAGE + button.get_attribute('data-url')

            company = company.replace('\n', ' ')
            logger.info('[click] [%s] {%s} (%s)', title, company, wage)
            item = JobItem(title, wage, company, say_hello_url)
            items.append(item)
    except NoSuchElementException as e:
        logger.exception(e)
    except TimeoutException as e:
        logger.exception(e)
        logger.error(job_url)
    return items


def handle_jobs(driver: RemoteWebDriver, jobs: List[JobItem]) -> None:
    for job in jobs:
        driver.get(job.url)


def main():
    driver = init_selenium(load_cookies=True)
    try:
        # login(driver)
        # 100-499
        jobs_url = config['zhipin']['job_url']
        jobs = []
        for job_url in jobs_url:
            _jobs = find_job(driver, job_url, 6)
            jobs.extend(_jobs)
        handle_jobs(driver, jobs)
    finally:
        pass
        # driver.quit()


if __name__ == '__main__':
    main()
