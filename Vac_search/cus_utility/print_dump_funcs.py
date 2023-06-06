import json
import re


def dump_to_json(file_name: str, instance: list[dict]) -> None:
    try:
        with open(file_name, 'w', encoding='utf-8') as f_out:
            json.dump(instance, f_out, indent=4, ensure_ascii=False)
        print(f'\033[32mDumped to file {file_name}\033[0m')
    except Exception as exc:
        print(f'\033[31m{exc.__class__.__name__}:{exc}\033[0m')


def prn_dct(in_list: list[dict]) -> None:
    for pos in in_list:
        for key, val in pos.items():
            if key != 'description':
                print(key, end=': ', sep='')
                if isinstance(val, list):
                    for item in val:
                        print('\t', item)
                elif isinstance(val, str):
                    print('\t', val.replace('\\n', '\n'), '\n')
                else:
                    print('\t', val)
            else:
                print(key, end=': ', sep='')
                print('\n', val.replace('\\n', ''))
        prn_otb()


def clean_html(in_str: str) -> list[str]:
    src = in_str
    in_str = in_str.replace('\\/', '/').replace('&#8216;', "'").replace('&amp;', '&').replace('&#160;', '')
    tags_to_eliminate = ('<p>', '<p', '</p>',
                         '<li>', '<li', '</li>',
                         '<ul>', '</ul>', '</a',
                         '</h3', '<h3', '</h1', '<h1', '</h2', '<h2', '</h4', '<h4',
                         '><span', '<span', '</span>', '</span',
                         '<strong>', '<strong', '</strong>',
                         '<div>', '</div>', 'lang="en-us"',
                         )
    span_search = re.compile(r'( style="[\w\\:;/#=_\-,.>%" ]*;")')
    spaces_much = re.compile(r'\s{2,}')
    for pattern in span_search.findall(in_str):
        in_str = in_str.replace(pattern, '<break flag>')
    for pattern in spaces_much.findall(in_str):
        in_str = in_str.replace(pattern, '')
    for tag in tags_to_eliminate:
        in_str = in_str.replace(tag, '')
    return [elem.replace('>', '').replace('<b', '').replace('</b', '').replace('<br', '')
            for elem in in_str.replace('&#8217;', "'").split('<break flag>')
            if elem.replace('>', '')]


def prn_dct_r(in_list: [list[dict], dict]) -> None:
    if isinstance(in_list, list):
        for pos in in_list:
            if isinstance(pos, dict):
                prn_dct_r(pos)
            elif isinstance(pos, list):
                prn_dct_r(pos)
            else:
                print('\n', pos.replace('\\n', ''))
    elif isinstance(in_list, dict):
        for key, val in in_list.items():
            if (key in ['logo', 'sameAs', 'url', '@context', ] or
                    (key, val) == ('@type', 'JobPosting')):
                continue
            if key != 'description':
                print(key, end='=>>', sep='')
                if isinstance(val, dict):
                    prn_dct_r(val)
                elif isinstance(val, str):
                    print('\t', val.replace('\\n', '\n'), '\n')
                else:
                    print('\t', val)
            else:
                cleaned_val = clean_html(val)
                print(key, end='->\n', sep='')
                print('\n\n_>'.join(cleaned_val))
                # print('\n', val.replace('\\n', ''))
    print()


def prn_otb() -> None:
    print('\n'.join(['=' * 200, '/' * 200, '=' * 200]))
