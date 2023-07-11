import re
import os
import json

from Vac_search.cus_utility import logger, dump_to_json, datestamp


class LuxoftPageParser:
    """
    A separate class for parsing pages from Luxoft site.
    Stands apart due to size and possible refactoring.
    Not involved into pages grabbing from network.
    """
    PHRASE2: str = r'\{\s+"@context":[\w\d\'\s:!@#$%^\\/&*\(\)\{\}\[\]~".,;\-+?]+\}'
    DICT_PATTERN: re.Pattern = re.compile(PHRASE2)
    ERR_PAT: str = '\033[31m{excName}: {excMsg}\033[0m'
    
    def __init__(self, out_path: str, file_name: str = 'Luxoft_vacancies.json'):
        self._out_path = os.path.join(out_path, file_name)
        logger.info(f'File out path: {self._out_path}')
        self._final_dicts_lst = []

    @property
    def final_dict_list(self):
        return self._final_dicts_lst

    def parse_out(self, pages_list_in: list[str]):
        """Starts parsing process. Phase 0"""
        result = self._catcher(pages_list_in)
        result2 = self._obtain_dicts(result)
        if result2[1]:
            for url_line, item in result2[1].items():
                result2[0][url_line] = (self._parse_missed(item))
        self._form_out_dict(result2[0])
        dump_to_json(self._out_path, self._final_dicts_lst)
        logger.info(f'{len(result2[0])=}; {len(result2[1])=}')

    def _form_out_dict(self, dct_in: dict):
        """Assembly uniformed dictionary to save. Recursive search (?). Phase 3"""
        def decompose_sub_dct(tmp: dict) -> str:
            """Extracting certain keys from sub-dictionaries"""
            out_str = []
            if addr_dct := tmp.get("address", None):
                out_str.append(addr_dct.get("addressCountry", None) or ' -unknown- ')
                out_str.append(addr_dct.get("addressLocality", None) or ' -unknown- ')
            return ', '.join(out_str)

        for key, val in dct_in.items():
            tmp_dct = {
                "company": "Luxoft",
                'parse_time': datestamp(),
                'name': val.get("title", None),
                'url': key,
                "hiringOrganization": (k.get("name", None) or '-unknown-'
                                       if (k := val.get("hiringOrganization", None))
                                       else '-unknown-'),
                "experience": val.get("skills"),
                "experienceRequirements": val.get("experienceRequirements", None) or '-empty-',
                "description": val.get("description"),
                "jobLocation": (decompose_sub_dct(location)
                                if (location := val.get("jobLocation", None))
                                else '-unknown-'),
                # "responsibilities": val.get("responsibilities"),
                # "occupationalCategory": val.get("occupationalCategory"),
            }
            self._final_dicts_lst.append(tmp_dct)

    def _catcher(self, pages_list_in: list) -> dict[str, str]:
        """Grab basic dictionary-strings from pages by regex pattern. Phase 1"""
        intermedia_result_1 = {}
        for page in pages_list_in:
            try:
                intermedia_result_1[page[0]] = (self.DICT_PATTERN.findall(page[1])[0])
            except Exception as exc:
                print('\033[31m', f'{exc.__class__.__name__}: {exc}', '\033[0m')
        return intermedia_result_1

    def _obtain_dicts(self, in_list: dict[str, str]) -> tuple[dict[str, dict[str, str]], dict[str, [dict]]]:
        """Obtain json-type dictionaries from strings. Phase 2"""
        resulting_dct = {}
        missed = {}
        count = 0
        for url_line, item in in_list.items():
            count += 1
            try:
                resulting_dct[url_line] = (json.loads(item))
            except Exception as exc1:
                print(f'\033[31m{exc1.__class__.__name__}: {exc1}\033[0m')
                try:
                    resulting_dct[url_line] = self._parse_missed(item, 'json')
                except Exception as exc2:
                    missed[url_line] = item
                    print(f'\033[31m{exc2.__class__.__name__}: {exc2} -> Reserved!\033[0m')

        return resulting_dct, missed

    @staticmethod
    def _parse_missed(line_in: str, flag: str = 'eval'):
        """Parse missed dictionaries. Phase 2.1 (optional)"""
        null = None     # NECESSARY! for eval function to substitute 'null' value. DO NOT REMOVE UNLESS SURE!
        under_work_line = line_in
        under_work_line = re.sub(" {2,}", " ", under_work_line)
        under_work_line += '}'
        if flag == 'json':
            return json.loads(under_work_line)
        else:
            return eval(under_work_line)    # left just in case for now; actually to be removed later


if __name__ == '__main__':
    print('To be used as part of complex for "Luxoft" only')
