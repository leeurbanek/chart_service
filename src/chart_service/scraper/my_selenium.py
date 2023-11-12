import io
import logging
import os

import requests
from bs4 import BeautifulSoup
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from src import debug
from src.utils import SpinnerManager, WebDriverManager


logging.getLogger('PIL').setLevel(logging.WARNING)
logging.getLogger('selenium').setLevel(logging.WARNING)
logging.getLogger('urllib3').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


class WebScraper:
    """"""
    def __init__(self, ctx, period, symbol):
        self.chart_dir = f"{ctx.obj['default']['temp_dir']}/chart"
        self.ctx = ctx
        self.debug = debug
        self.period = period
        self.symbol = symbol
        self.url = ctx.obj['chart_service']['base_url']

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ctx={self.ctx.obj}, period={self.period}, symbol={self.symbol})"

    def webscraper(self):
        """"""
        if self.debug: logger.debug(f'webscraper({self.period}, {self.symbol})\n')
        with WebDriverManager(debug=self.debug) as driver:
            if self.debug: logger.debug(f"WebDriverManager()={WebDriverManager}")
            if not self.debug: print(f'  fetching chart: {self.symbol}_{self.period.lower()}.png... ', end=' ')
            with SpinnerManager():
                if self.debug: logger.debug(f"SpinnerManager()={SpinnerManager}")
                self._set_chart_page(driver)
                content = self._get_page_content(driver)
                src = self._get_img_src(content)
                self._save_img_to_file(src)
            if not self.debug: print('\b done')

    def _get_img_src(self, soup=None):
        """"""
        if self.debug: logger.debug(f'_get_img_src(soup={type(soup)})')
        attr = soup.find(attrs={'class': "chartnotes-container"})
        img = attr.find("img")
        return img.get("src")

    def _get_page_content(self, driver):
        """"""
        if self.debug: logger.debug('_get_page_content(driver={driver})')
        driver.implicitly_wait(3)
        content = driver.page_source
        return BeautifulSoup(content, features='html.parser')

    def _save_img_to_file(self, src=None):
        """"""
        if self.debug: logger.debug(f'_save_img_to_file(src={type(src)})')

        src_content = requests.get(f'https:{src}', headers={'User-agent': 'Mozilla/5.0'}).content

        image_file = io.BytesIO(src_content)
        image = Image.open(image_file).convert('RGB')
        # image.save(os.path.join(CHART_DIR, f'{self.symbol}_{self.period.lower()}.png'), 'PNG', quality=80)
        image.save(os.path.join(self.chart_dir, f'{self.symbol}_{self.period.lower()}.png'), 'PNG', quality=80)

    def _set_chart_page(self, driver):
        """"""
        if self.debug: logger.debug(f'scraper_obj._set_chart_page(driver={driver})')
        year = 1  # for setting dataRange predef field
        if self.period == 'Weekly': year = 5

        # driver.get(f'{BASE_URL}{self.symbol}')
        driver.get(f'{self.url}{self.symbol}')
        driver.implicitly_wait(3)

        period2 = Select(driver.find_element(By.ID, 'period2'))
        period2.select_by_visible_text(f'{self.period}')

        dataRange = Select(driver.find_element(By.ID, 'dataRange'))
        dataRange.select_by_value(f'predef:{year}|0|0')

        chartSize = Select(driver.find_element(By.ID, 'chartSize'))
        chartSize.select_by_visible_text('Landscape')

        # chartSkin = Select(driver.find_element(By.ID, 'chartSkin'))
        # chartSkin.select_by_visible_text('night')

        driver.find_element(By.XPATH, '//input[@type="button"][@value="Update"]').click()


# WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, 'Element's XPath')))
