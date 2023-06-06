import os

from Vac_search.sites_modules import *

__all__ = ['outside_crutch', 'get_list_of_companies']

if not os.path.exists('out_files'):
    # crutchely crutch
    os.mkdir('out_files')
    print("Creating dir")
    BAS_OUT_PATH = os.path.abspath('out_files')
    print(f"Created dir {BAS_OUT_PATH}")
else:
    BAS_OUT_PATH = os.path.abspath('out_files')
    print(f"Found dir {BAS_OUT_PATH}")

firms_files = {'JetBrains': 'vacancies_JetBrains.json',
               'Epam': 'vacancies_Epam.json',
               'Luxoft': 'vacancies_Luxoft.json',
               'Miro': 'vacancies_Miro.json',
               'Veeam': 'vacancies_Veeam.json',
               'ZeroAvia': 'vacancies_ZeroAvia.json',
               }

# define grabbers
__grabbers_dict = {
    'jetbrains_grb': GrabJetBrainsVacancies(BAS_OUT_PATH, firms_files['JetBrains']),
    'zeroavia_grb': GrabZeroAviaVacancies(BAS_OUT_PATH, firms_files['ZeroAvia']),
    'epam_grb': GrabEpamVacancies(BAS_OUT_PATH, firms_files['Epam']),
    'miro_grb': GrabMiroVacancies(BAS_OUT_PATH, firms_files['Miro']),
    'luxoft_grb': GrabLuxoftVacancies(BAS_OUT_PATH, firms_files['Luxoft']),
}


def __total_walk() -> dict[str, list[dict[str, str]]]:
    companies_resulting_dict = {}
    for company, grabber in __grabbers_dict.items():
        print(f'\033[32m\nGrabbing: {company} \033[0m')
        companies_resulting_dict[company] = grabber.start_grabbing()
    # start grab vacancies links (now not needed, left just for clearness)
    # jetbrains_grb.start_grab()
    # epam_grb.start_grabbing()
    # miro_grb.start_grabbing()
    # luxoft_grb.start_grabbing()
    # zeroavia_grb.start_grabbing()
    return companies_resulting_dict


def outside_crutch(company_name: list = None) -> dict[str, list[dict[str, str]]]:
    companies_resulting_dict = {}
    if company_name is None:
        return __total_walk()
    for company in company_name:
        current = __grabbers_dict.get(company, None)
        if current:
            companies_resulting_dict[company] = current.start_grabbing()
    return companies_resulting_dict


def get_list_of_companies():
    return list(__grabbers_dict.keys())


if __name__ == '__main__':
    __total_walk()
