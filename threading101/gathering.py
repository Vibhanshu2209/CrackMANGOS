
import asyncio

from helper import setup_logger, logging, APIService

setup_logger()
logger = logging.getLogger(__name__)


api_service = APIService()

languages = ["en", "it","ru", "fr", "es", "pt" ]
coroutines = [api_service.fetch_data(language) for language in languages]


async def main():
    # results = await asyncio.gather(
    #     *coroutines, 
    #     return_exceptions=True ## if fetch_data raises an exception, it will be captured and returned in the results list
    #     )
    # print(f"Coroutine results: {results}")

    # tasks = [asyncio.create_task(api_service.fetch_data(lang)) for lang in languages]
    # results = await asyncio.gather(
    #     *tasks, 
    #     return_exceptions=True ## if fetch_data raises an exception, it will be captured and returned in the results list
    #     )
    # print(f"Task results: {results}")

    async with asyncio.TaskGroup() as tg:
        results = [tg.create_task(api_service.fetch_data(lang)) for lang in languages]

    print(f"Taskgroup results {[len(result.result()) for result in results]}")
    """
    since "ru" language doesnt have any valid data 
    AND fetch_data also calls response.raise_for_status,
    so the above task group will throw an error while trying to call for "ru" language
    """


asyncio.run(main())
