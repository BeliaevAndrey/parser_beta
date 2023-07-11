import re

from Vac_search.async_gr_custom import AsyncGrab
from .luxoft_page_parser import LuxoftPageParser
from Vac_search.cus_utility import logger
import asyncio


class GrabLuxoftVacancies:
    LINK: str = "https://career.luxoft.com/job-opportunities/"
    BASE_LINK: str = 'https://career.luxoft.com/job-opportunities/?keyword=&set_filter=Y&PAGEN_1='
    OUT_PATH: str = 'Luxoft_out_files'
    UPPER_LIMIT: int = 94
    VACANCY_LINK_PATTERN: re.Pattern = re.compile(r"/job/[\w-]+/\d+/")
    _pages_storage = []

    def __init__(self, out_path: str, file_name: str = 'Luxoft_vacancies.json'):
        self.luxoft_parser = LuxoftPageParser(out_path, file_name)

    async def start_grabbing(self) -> list[dict[str, str]]:
        """Start walking over luxoft"""
        base_link = "https://career.luxoft.com"
        luxoft_links = self._generate_pack()
        luxoft_vacancy_links = []
        result1 = await self._grab_vacancies(luxoft_links)
        for item in result1:
            luxoft_vacancy_links.extend(self._find_links_lines(item[1]))
        luxoft_vacancy_links = list(set(luxoft_vacancy_links))
        logger.info(f'Amount of unique links {len(luxoft_vacancy_links)}')
        for i in range(len(luxoft_vacancy_links)):
            luxoft_vacancy_links[i] = f'{base_link}{luxoft_vacancy_links[i]}'
        step = 30
        for i in range(0, len(luxoft_vacancy_links), step):
            self._pages_storage.extend(await self._grab_vacancies(luxoft_vacancy_links[i:i + step]))
        print(f'{len(self._pages_storage)=}')
        logger.info(f'{len(self._pages_storage)=}')
        self.luxoft_parser.parse_out(self._pages_storage)
        return self.luxoft_parser.final_dict_list

    @staticmethod
    async def _grab_vacancies(an_url: [str, list]) -> [str, list[tuple[str, str]]]:
        if isinstance(an_url, list):
            AsyncGrab.set_pages_list(an_url)
            out_list: list[tuple[str, str]] = await AsyncGrab.start()
            return out_list
        else:
            raise TypeError("Unsupported type of incoming data")

    def _generate_pack(self) -> list[str]:
        links_bunch = ['https://career.luxoft.com/job-opportunities/?keyword=&set_filter=Y', ]
        for i in range(2, self.UPPER_LIMIT):                # Upper limit to be enlarged if needed
            links_bunch.append(self.BASE_LINK + str(i))
        logger.info(msg=f'Amount of links {len(links_bunch)}')
        return links_bunch

    def _find_links_lines(self, page_in: str) -> list:
        result = self.VACANCY_LINK_PATTERN.findall(page_in)
        return result


if __name__ == '__main__':
    asyncio.run(GrabLuxoftVacancies('Luxoft_out_files', 'Luxoft_vacancies.json').start_grabbing())
