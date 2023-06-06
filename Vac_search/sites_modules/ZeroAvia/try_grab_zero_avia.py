import re
import os
from bs4 import BeautifulSoup
from typing import TypeAlias
import json

from Vac_search.async_gr_custom import AsyncGrab
from Vac_search.cus_utility import datestamp, dump_to_json

LIST_OF_DICTS_SRC: TypeAlias = list[dict[str, [str, list]]]
LIST_OF_DICTS_OUT: TypeAlias = list[dict[str, str]]


class GrabZeroAviaVacancies:
    # Attention!!! Not sure if links below will not expire ever...
    _URL_OF_INTEREST = 'https://jobs.workable.com/search?query=zeroavia&remote=false'
    _PRE_LINK = 'https://jobs.workable.com/api/v1/companies/r6jxFNjY8f9DVffcV8kB3T?pageToken='
    _PATTERN = re.compile(r'"nextPageToken":"[\w\d=]+"')

    def __init__(self, out_path: str, file_name: str):
        self._out_file = os.path.join(out_path, file_name)
        self._vac_count = 0

    def _form_final_dct(self, dct_in: LIST_OF_DICTS_SRC) -> LIST_OF_DICTS_OUT:
        """
        Extraction of interested parameters from dictionary, obtained from site
        :param dct_in: list[dict[str, [str, list]]]     -- json-decoded dictionary
        :return: list[dict[str, str]]                   -- list of filtered dict
        """
        final_list = []
        for item in dct_in:
            tmp_dict = {
                "company": "ZeroAvia",
                'parse_time': datestamp(),
                'name': item.get("title", None),
                'url': item.get("url", None),
                'department': item.get("department", None),
                'employmentType': item.get("employmentType", None),
                'language': item.get("language", None),
                'locations': '; '.join(loc) if (loc := item.get("locations", None)) else None
            }
            final_list.append(tmp_dict)
            self._vac_count += 1
        print(f'{self._vac_count=}')
        return final_list

    @staticmethod
    def first_fun(an_url: [str, list]) -> [str, list[tuple[str, str]]]:
        """Initial (or final) grabbing method"""
        if isinstance(an_url, str):
            AsyncGrab.set_pages_list([an_url])
            tmp_stub = AsyncGrab.start()
            try:
                out_string: str = tmp_stub[0][1]
                return out_string
            except Exception as exc:
                print('\033[31m', f'{exc.__class__.__name__}: {exc}', '\033[0m')
                print(tmp_stub)         # TODO: change to log-dump
                # raise SystemExit      # TODO: Check strictly
        elif isinstance(an_url, list):
            AsyncGrab.set_pages_list(an_url)
            out_list: list[tuple[str, str]] = AsyncGrab.start()
            return out_list
        else:
            raise TypeError("Unsupported type of incoming data")

    def _walk_over_zeroavia(self):      # TODO: Refactor! Decomposition needed.
        """
        Main grabbing method for ZeroAvia site.
        Yet another spaghetti-code for now.
        """
        response: str = self.first_fun(self._URL_OF_INTEREST)
        token: str = self._PATTERN.findall(response)[0]
        # print(token)                  # TODO: move to logger (maybe useful to control scrapping)
        new_link = self._PRE_LINK + token.split(':')[1].replace('"', '')
        responses = []
        for _ in range(5):
            responses.append(self.first_fun(new_link))
            token: list = self._PATTERN.findall(responses[-1])
            if token:
                token: str = token[0]
                new_link = self._PRE_LINK + token.split(':')[1].replace('"', '')
            else:
                break
        soup = BeautifulSoup(response, 'html5lib')
        out_text = soup.find(name='script').contents
        l_idx = out_text[0].find('"jobs":', 1) + len('"jobs":')
        r_idx = out_text[0].rfind(']', 1) + 1
        za_job_dct: list[dict[str, str]] = []
        if l_idx > 0 and r_idx > 0:
            out_text = out_text[0][l_idx:r_idx]
        try:
            za_job_dct = json.loads(out_text)
        except Exception as exc:
            print(f'\033[031m{exc.__class__.__name__}: {exc}\033[0m')       # TODO: reorient to logger
        for rsp in responses:
            try:
                temp_dct = json.loads(str(rsp))
                za_job_dct.extend(temp_dct.get("jobs"))
            except Exception as exc:
                print(f'\033[031m{exc.__class__.__name__}: {exc}\033[0m')   # TODO: reorient to logger
        dump_to_json(self._out_file, self._form_final_dct(za_job_dct))

    def start_grabbing(self):
        """Kickstart"""
        self._walk_over_zeroavia()


if __name__ == '__main__':
    print('A module. Not for separate use')
    GrabZeroAviaVacancies('za_outfiles', 'ZeroAvia_vacancies.json').start_grabbing()
