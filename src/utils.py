import logging
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from src import config_dict


logging.getLogger('selenium').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

adblock = config_dict['chart_service']['adblock']
debug = config_dict['default']['debug'] == 'True'
driver = config_dict['chart_service']['driver']


class SpinnerManager:
    """Manage a simple spinner object"""
    busy = False
    delay = 0.2

    @staticmethod
    def spinning_cursor():
        while 1:
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.debug = debug
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            if not self.debug: 
                sys.stdout.write(next(self.spinner_generator))
                sys.stdout.flush()
            time.sleep(self.delay)
            if not self.debug:
                sys.stdout.write('\b')
                sys.stdout.flush()

    def __enter__(self):
        self.busy = True
        if self.debug: logger.debug(f'SpinnerManager.__enter__({SpinnerManager.spinner_task})')
        threading.Thread(target=self.spinner_task).start()

    def __exit__(self, exception, value, tb):
        self.busy = False
        time.sleep(self.delay)
        if exception is not None:
            return False
        if self.debug: logger.debug('SpinnerManager.__exit__()')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__})"


class WebDriverManager:
    """Manage Selenium web driver"""
    def __init__(self, debug) -> None:
        self.debug = debug

    def __enter__(self):
        chrome_opts = webdriver.ChromeOptions()
        chrome_opts.headless = True  # don't display browser window
        # s = Service(driver)
        # self.driver = webdriver.Chrome(service=s, options=chrome_opts)
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

        # Install ad blocker if used
        if os.path.exists(adblock):
            self.driver.install_addon(adblock)
            # pyautogui.PAUSE = 2.5
            # pyautogui.click()  # position browser window
            # pyautogui.hotkey('ctrl', 'w')  # close ADBLOCK page

        if self.debug: logger.debug(f'WebDriverManager.__enter__(session={self.driver.session_id})')
        return self.driver

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.driver.quit()
        if self.debug: logger.debug('WebDriverManager.__exit__()')

    def __repr__(self) -> str:
        return f"{self.__class__.__name__})"


if __name__ == '__main__':
    with SpinnerManager():
        time.sleep(2)  # some long-running operation
