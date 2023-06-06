"""
Example file illustrating call of sites walker.
"""
from Vac_search import outside_crutch, get_list_of_companies
from time import sleep


def main():
    luxoft_flag = False
    count = 5
    for key, val in outside_crutch(get_list_of_companies()).items():
        print(key, end=': ', sep='')
        print(len(val) if val else '\033[31mObtained empty list\033[0m')
        luxoft_flag = (key == 'luxoft_grb' and val and len(val) < 100)
    while luxoft_flag and count:
        print(f'Luxoft will be re-grabbed in 30 seconds. Attemps left: {count}')
        sleep(30)
        count -= 1
        key, val = outside_crutch(['luxoft_grb']).items()
        print(key, end=': ', sep='')
        print(len(val) if val else '\033[31mObtained empty list\033[0m')
        luxoft_flag = (key == 'luxoft_grb' and val and len(val) < 100)


if __name__ == '__main__':
    main()
