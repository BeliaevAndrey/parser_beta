import os
from requests_html import HTMLSession

# from Vac_search.async_gr_custom import AsyncGrab
from Vac_search.cus_utility import logger
from Vac_search.cus_utility import datestamp, dump_to_json


class GrabEpamVacancies:
    # Attention! Not sure if link below will not expire ever...
    _LINK: str = ("https://www.epam.com/services/vacancy/"
                  "search?locale=en&limit=3000&"
                  "recruitingUrl=%2Fcontent%2Fepam%2Fen%2Fcareers%2Fjob-listings%2Fjob&"
                  "query=&country=all&sort=relevance&offset=0&searchType=placeOfWorkFilter")
    _lost_items: list = []

    def __init__(self, out_path: str, final_file: str):
        self._final_file = os.path.join(out_path, final_file)
        self._final_file_lost = os.path.join(out_path, 'epam_lost_data.json')
        self._final_dicts_list = []

    def start_grabbing(self, start_link: str = _LINK) -> list[dict[str, str]]:
        session = HTMLSession()
        request = session.get(start_link)
        out_dct: dict = request.json()
        count = 'STUB! -> (something maybe wrong)'
        try:
            count = out_dct.get('total', None)
            count = int(count)
        except Exception as exc:
            print(f'\033[031mCount ERROR{exc.__class__.__name__} {exc}\033[0m')
        for item in out_dct['result']:
            try:
                tmp_dct = {
                    "company": "Epam",
                    'parse_time': datestamp(),
                    'name': item.get('name', None),
                    'url': item.get("url", None),
                }
                self._final_dicts_list.append(tmp_dct)
            except Exception as exc:
                print(f'\033[031mCount ERROR{exc.__class__.__name__} {exc}\033[0m')
                self._lost_items.append(item)
        logger.info(f'Links found: list length = {len(self._final_dicts_list)}, site response = {count}')
        dump_to_json(self._final_file, self._final_dicts_list)
        return self._final_dicts_list


if __name__ == '__main__':
    print('module')
