import json
import os

from Vac_search.cus_utility import datestamp, dump_to_json
from Vac_search.async_gr_custom import AsyncGrab

BASIC_LINK = 'https://www.jetbrains.com/careers/jobs/'


class GrabJetBrainsVacancies:
    _vac_count: int = 0
    _lost_items: list = []

    def __init__(self, out_path: str, file_name: str):
        self._out_file = os.path.join(out_path, file_name)
        self._final_dict_lst = []

    def _form_final_dict(self, data_in: list[dict[str, str]]) -> list[dict[str, str]]:
        """Getting interesting positions from dictionary"""
        for item in data_in:
            try:
                tmp_dict = {
                    "company": "JetBrains",
                    'parse_time': datestamp(),
                    'name': item.get('title', None),
                    'url': f'{BASIC_LINK + item.get("slug")}',
                    'role': ','.join(item.get('role', [' -empty- ', ])),
                    'technologies': ', '.join(item.get('technologies', [' -empty- ', ])),
                }
                self._final_dict_lst.append(tmp_dict)
                self._vac_count += 1
            except Exception as exc:
                print(f'\033[31m{exc.__class__}: {exc}\0330m')      # TODO: add logger instruction here
                self._lost_items.append(item)
        return self._final_dict_lst

    @staticmethod
    async def _first_fun(an_url: str) -> list[dict]:
        """Initial (or final) grabbing method"""
        start_line = 'var VACANCIES = [{'
        end_line = '}]'
        AsyncGrab.set_pages_list([an_url])
        results: list[tuple[str, str]] = await AsyncGrab.start()
        out_string: str = results[0][1]
        try:
            start_index = out_string.index(start_line) + len(start_line) - 2
            end_index = out_string.index(end_line, start_index + 1) + 3
            tmp = out_string[start_index:end_index]
            vacancies_str: list[dict] = json.loads(tmp)
            return vacancies_str
        except ValueError:  # TODO: add logger instruction here
            return []

    async def start_grabbing(self) -> [list[dict[str, str]], None]:
        """Kickstart"""
        tmp = await self._first_fun(BASIC_LINK)
        if tmp:
            dump_to_json(self._out_file, self._form_final_dict(tmp))
            return self._final_dict_lst
        else:
            print('Error')  # TODO: add logger instruction here


if __name__ == '__main__':
    print("module")
