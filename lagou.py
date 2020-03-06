# -*- coding: utf-8 -*-
# =============================================================================
#          Desc: 
#        Author: chemf
#         Email: eoyohe@gmail.com
#      HomePage: eoyohe.cn
#       Version: 0.0.1
#    LastChange: 2020/3/2 4:29 PM
#       History: 
# =============================================================================
import json
import time
from dataclasses import dataclass

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver, WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from common import logger, config


class LagouSpider:
    def __init__(self, load_cookie=True):
        self.homepage = 'https://www.lagou.com'
        self.config_key = 'lagou'
        self.jobs = []
        self.driver = self.init_selenium(load_cookie)

    def init_selenium(self, load_cookies=False) -> RemoteWebDriver:
        options = ChromeOptions()
        # 自动打开 F12 控制台，方便抓包检查网络请求问题
        options.add_argument('--auto-open-devtools-for-tabs')
        # 同避免 webdriver=True, 在 chrome 低于 79 版本生效
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # stackoverflow 上表示避免 TimeoutException 的方法，但似乎没用
        options.add_argument("enable-features=NetworkServiceInProcess")
        browser = webdriver.Chrome(options=options)

        # 禁止 window.navigator.webdriver = True 被检测到是 webdriver 的爬虫行为
        script = '''
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        })
        '''
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": script})

        # 设置 cookie 前需要先跳转到对应的 domain
        browser.get(self.homepage)
        browser.set_page_load_timeout(30)
        if load_cookies:
            logger.debug('load cookies')
            with open(config[self.config_key]['cookie_file']) as f:
                cookies = json.load(f)
            for cookie in cookies:
                try:
                    browser.add_cookie(cookie)
                except Exception as e:
                    print(cookie)
                    raise e
        return browser

    def find_jobs(self, jobs_url: str, page: int):
        items = []
        for page in range(1, page_count + 1):
            url = f'{jobs_url}&page={page}'
            _current_page_jobs = self._find_job(url)
            items.extend(_current_page_jobs)
        return items

    def _find_jobs(self, job_url):
        self.driver.get(job_url)
        time.sleep(5)
        html = self.driver
        pass

    def run(self):
        pass


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
