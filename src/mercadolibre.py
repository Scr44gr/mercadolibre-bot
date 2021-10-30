

from typing import List, Union
import requests
from bs4 import BeautifulSoup


requests.adapters.DEFAULT_RETRIES = 5

class MercadoLibre:

    ORIGIN_URL = 'https://api.mercadolibre.com'
    ENDPOINT = '/items?ids={}'
    SITE_ID = 'MLC'
    MAX_IDS_SIZE = 20  # Max ids size per request

    def __init__(self, ids: Union[str, List[str]]) -> None:
        if isinstance(ids, list):
            ids = ','.join(ids)
        self.url = self.ORIGIN_URL + self.ENDPOINT.format(ids)

    def get_items_info(self):
        """Make a request to the mercadolibre api and get the info of the items by their ids

        response example:

        {
               "code": 200,
               "body": {
                   "id": "MLA594239600",
                   "site_id": "MLA",
                   "title": "Item De Test - Por Favor No Ofertar",
                   "subtitle": null,
                   "seller_id": 303888594,
                   "category_id": "MLA401685",
                   "official_store_id": null,
                   "price": 120,
                   "base_price": 120,
                   "original_price": null,
                   "currency_id": "",
                   "initial_quantity": 1,
                   "available_quantity": 1,
                   "sold_quantity": 0,
                   "sale_terms": [],
                   [...
                   ] "automatic_relist": false,
                   "date_created": "2018-02-26T18:15:05.000Z",
                   "last_updated": "2018-03-29T04:14:39.000Z",
                   "health": null
               }
           }
        ]

        """

        response = requests.get(self.url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})

        if response.status_code == 200:
            return response.json()

        raise BadStatusCode()

class MercadoLibreWebCorrector:


    def get_sales(self, url: str) -> List[str]:
        """Get the sales of an item by its url

        Args:
            url (str): The url of the item

        Returns:
            List[str]: The sales of the item
        """

        response = requests.get(url,  headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'})

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # get numbers
            # <span class="ui-pdp-subtitle">Nuevo  |  1254 vendidos</span>
            # quick fix, need to improve.
            try:
                text = soup.find('div', {'class': 'ui-pdp-header__subtitle'}).find('span').text
                numbers =[int(n) for n in text.split() if n.isdigit()][0]
                return numbers or 0
            except:
                return 0
class BadStatusCode(Exception):
    """The response has a bad status code response.

    """
    


if __name__ == '__main__':
    url = "https://articulo.mercadolibre.cl/MLC-482168573-pack-2-lampara-de-sal-del-himalaya-piedra-de-2-a-3-kg-_JM"
    test = MercadoLibreWebCorrector()
    print(test.get_sales(url))