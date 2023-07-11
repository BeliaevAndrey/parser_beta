import asyncio
import aiohttp
from Vac_search.cus_utility import logger


class AsyncGrab:
    """To grab a bunch of pages asynchronously"""
    _temp_storage: list[tuple[str, str]]
    _pages_list: list
    _incomplete_flag: bool = False
    _count_connection_errors: int = 0
    _lost_urls: list[str] = []

    @classmethod
    def set_pages_list(cls, pages_to_grab) -> None:
        cls._pages_list = pages_to_grab
        if cls._pages_list:
            print('PAGES LIST SUCCESSFULLY SET')
        else:
            print('PAGES LIST SET FAILED!!!')
            logger.warning(msg=f'PAGES LIST SET FAILED!!!')

    @classmethod
    async def _grab_site(cls, url_to_get: str) -> None:
        """Asynchronously grabbing site page"""
        user_agent = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0'}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url_to_get, headers=user_agent) as response:
                    html = await response.text()
                    cls._temp_storage.append((url_to_get, html))
        except Exception as exc:
            logger.error(msg=f'{exc.__class__.__name__}: {exc}')
            cls._count_connection_errors += 1
            cls._incomplete_flag = True
            cls._lost_urls.append(url_to_get)

    @classmethod
    async def _grab_wordlist(cls) -> None:
        """Create a queue of coroutines to grab info from site"""
        if cls._pages_list:
            captors = [asyncio.ensure_future(cls._grab_site(url_to_get=url))
                       for url in cls._pages_list]
            await asyncio.wait(captors)
        else:
            print('ERROR: pages list NOT set!')
            logger.warning(msg=f'ERROR: pages list NOT set!')
            return

    @classmethod
    async def start(cls) -> list[tuple[str, str]]:
        cls._temp_storage = []
        # eve_loop = asyncio.new_event_loop()
        await cls._grab_wordlist()
        # eve_loop.close()
        if cls._temp_storage:
            return cls._temp_storage
        else:
            print("ERROR: empty page storage")
            logger.warning(msg=f'ERROR: empty page storage')
            return []

    @classmethod
    def complete_flag(cls) -> bool:
        return cls._incomplete_flag

    @classmethod
    def err_count(cls) -> int:
        return cls._count_connection_errors

    @classmethod
    def get_lost_urls(cls) -> list[str]:
        return cls._lost_urls
