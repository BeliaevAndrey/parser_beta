from bs4 import BeautifulSoup
import json
import os
import re


class EpamDescriptionParser:
    _PATH: str = 'Epam_out_files'
    _JSON_FILE: str = 'epam_vacancies.json'
    mad_tag_dct: dict[str, str] = {'&amp;': '&', '&lt;': '<', '&gt;': '>'}

    def __init__(self, json_path: str = _PATH, json_file: str = _JSON_FILE):
        self._json_full_path = os.path.join(json_path, json_file)

    def read_dict(self) -> dict[str, dict[str, str]]:
        with open(self._json_full_path, 'r', encoding='utf-8') as f_in:
            out_dict = json.load(f_in)
        return out_dict

    def clean_phrase(self, in_str: str) -> str:
        for key, val in self.mad_tag_dct.items():
            in_str = in_str.replace(key, val)
        return in_str

    def walk_over_text(self):
        desc_dict = self.read_dict()
        count = 0
        for url, context in desc_dict.items():
            count += 1
            if count == 40:
                text = self.clean_phrase(context["description"])
                for item in BeautifulSoup(text, 'lxml').find_all('li'):
                    print(item)
                    print(70 * '=+=')
                # for line in text.split('</li><li>'):
                #     print(line)
                break


if __name__ == '__main__':
    clean = EpamDescriptionParser()
    clean.walk_over_text()
