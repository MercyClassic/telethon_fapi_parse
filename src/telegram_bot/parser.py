import asyncio
import dataclasses
import re
from typing import List

from selenium import webdriver


@dataclasses.dataclass
class Product:
    title: str
    link: str


class WBParser:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(options=options)

    def build_query_string(self, product_name: str):
        return re.sub(' ', r'%20', product_name)

    def get_products(self) -> List[Product]:
        links = self.driver.find_elements('class name', 'product-card__link')
        result = []
        for i in range(10):
            result.append(
                Product(
                    title=links[i].get_attribute('aria-label'),
                    link=links[i].get_attribute('href'),
                ),
            )
        return result

    async def parse(self, product_name: str) -> List[Product]:
        query = self.build_query_string(product_name)
        self.driver.get(
            'https://www.wildberries.ru/'
            'catalog/0/search.aspx'
            '?page=1&sort=popular'
            f'&search={query}',
        )
        await asyncio.sleep(3)
        return self.get_products()
