from sites_modules import *

__all__ = ['outside_crutch']

BAS_OUT_PATH = 'out_files'
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
    'epam_grb': GrabEpamVacancies(BAS_OUT_PATH, firms_files['Epam']),
    'miro_grb': GrabMiroVacancies(BAS_OUT_PATH, firms_files['Miro']),
    'luxoft_grb': GrabLuxoftVacancies(BAS_OUT_PATH, firms_files['Luxoft']),
    'zeroavia_grb': GrabZeroAviaVacancies(BAS_OUT_PATH, firms_files['ZeroAvia'])
}


def __total_walk():
    for grabber in __grabbers_dict.values():
        grabber.start_grabbing()
    # start grab vacancies links
    # jetbrains_grb.start_grab_jb()
    # epam_grb.start_grabbing()
    # miro_grb.start_grabbing()
    # luxoft_grb.start_grabbing()
    # zeroavia_grb.start_grabbing()


def outside_crutch(company_name: list = None):
    if company_name is None:
        __total_walk()
        return
    for company in company_name:
        current = __grabbers_dict.get(company, None)
        if current:
            current.start_grabbing()


def get_list_of_companies():
    return list(__grabbers_dict.keys())


if __name__ == '__main__':
    __total_walk()
