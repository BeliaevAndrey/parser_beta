"""
Example file illustrating call of sites walker.
"""
from Vac_search import outside_crutch, get_list_of_companies
from time import sleep
import asyncio


async def main():
    luxoft_flag = False
    count = 5
    for key, val in (await outside_crutch(get_list_of_companies())).items():
        print(key, end=': ', sep='')
        print(len(val) if val else '\033[31mObtained empty list\033[0m')
        luxoft_flag = (key == 'luxoft_grb' and val and len(val) < 600 or not val)
    while luxoft_flag and count:
        print(f'Luxoft will be re-grabbed in 30 seconds. Attemps left: {count}')
        sleep(30)
        count -= 1
        key, val = (await outside_crutch(['luxoft_grb'])).items()
        print(key, end=': ', sep='')
        print(len(val) if val else '\033[31mObtained empty list\033[0m')
        luxoft_flag = (key == 'luxoft_grb' and val and len(val) < 100 or not val)


if __name__ == '__main__':
    asyncio.run(main())
