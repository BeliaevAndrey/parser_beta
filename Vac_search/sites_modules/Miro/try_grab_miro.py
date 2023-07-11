from bs4 import BeautifulSoup
import json
import os
import asyncio


from Vac_search.async_gr_custom import AsyncGrab
from Vac_search.cus_utility import dump_to_json, datestamp

LINK = "https://miro.com/careers/open-positions/"
OUT_PATH = 'Miro_out_files'


class GrabMiroVacancies:

    def __init__(self, out_path: str = OUT_PATH, final_file: str = 'Miro_vacancies.json'):
        self._final_file = os.path.join(out_path, final_file)
        self._vacancies_dicts_lst: list[dict[str, str]] = []

    def _collect_vac_urls(self, in_dct: [dict, list, str], urls_lst: list[str], urls_dct: [str, str]) -> None:
        """Find vacancies links"""
        for item in in_dct.get("props").get("pageProps").get("data").get("jobs"):
            urls_dct[item.get('absolute_url')] = item.get('title')
            urls_lst.append(item.get('absolute_url'))
            self._vacancies_dicts_lst.append(
                {
                    "company": "Miro",
                    "parse_time": datestamp(),
                    "name": item.get("title"),
                    "url": item.get("absolute_url"),
                }
            )

    async def _grab_start_page(self, link: str) -> tuple[list[str], dict[str, str]]:
        """Init page scrapping (local entrypoint)"""
        AsyncGrab.set_pages_list([link])
        out_string: str = (await AsyncGrab.start())[0][1]
        miro_sp_soup = BeautifulSoup(out_string, 'lxml')

        tmp = miro_sp_soup.find(
            name='script', attrs={'id': "__NEXT_DATA__", 'type': "application/json"}
        ).contents
        out_dict = json.loads(tmp[0])
        urls_lst = []
        urls_dct: dict[str, str] = {}
        self._collect_vac_urls(out_dict, urls_lst, urls_dct)
        return urls_lst, urls_dct

    async def start_grabbing(self) -> list[dict[str, str]]:
        await self._grab_start_page(LINK)
        dump_to_json(self._final_file, self._vacancies_dicts_lst)
        return self._vacancies_dicts_lst


if __name__ == '__main__':
    print('A module. Not for separate use.')
    # asyncio.run(GrabMiroVacancies().start_grabbing())
