import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
import time
import requests

# Configure a basic logger so each step is visible in console output.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Base URL template for fetching Harry Potter books by language.
BOOKS_URL = "https://potterapi-fedeperin.vercel.app/{}/books"


def fetch_data(language):
    """
    Fetch Harry Potter book data for a given language.

    This is a blocking I/O call, so it is suitable for running in a thread
    or a process pool when used inside asyncio.
    """
    logger.info("Starting book fetch for language=%s", language)

    try:
        # requests.get is blocking; it is often run in a worker thread.
        response = requests.get(BOOKS_URL.format(language), timeout=10)
        response.raise_for_status()
        books = response.json()

        logger.info(
            "Fetched %s books successfully for language=%s",
            len(books) if isinstance(books, list) else "data",
            language,
        )
        return books

    except requests.RequestException as exc:
        logger.exception("Failed to fetch books for language=%s: %s", language, exc)
        raise


async def main():
    # This first section uses asyncio.to_thread for blocking IO operations.
    # The event loop keeps running while each thread handles the HTTP request.
    # logger.info("Starting async thread-based fetches")

    # task1 = asyncio.create_task(asyncio.to_thread(fetch_data, "en"))
    # task2 = asyncio.create_task(asyncio.to_thread(fetch_data, "it"))

    # result1 = await task1
    # result2 = await task2

    # logger.info(
    #     "Thread-based results received: en=%s, it=%s",
    #     len(result1) if isinstance(result1, list) else "n/a",
    #     len(result2) if isinstance(result2, list) else "n/a",
    # )


    languages = ["en", "it", "fr", "es", "pt", "ru"]


    # This second section uses a ProcessPoolExecutor to demonstrate parallel
    # execution for tasks that may be CPU-bound or need isolation.
    loop = asyncio.get_running_loop()

    logger.info("Starting process-pool fetches")

    resultMap = {}
    with ProcessPoolExecutor(max_workers=3) as executor:

        tasksMap = {}

        for language in languages:
            logger.info("Submitting fetch task for language=%s", language)
            tasksMap[language] = loop.run_in_executor(executor, fetch_data, language)

        # Await the results of the fetches
        for language, task in tasksMap.items():
            try:
                result = await task
                logger.info(
                    "Process-pool fetch completed for language=%s with %s books",
                    language,
                    len(result) if isinstance(result, list) else "data",
                )

                resultMap[language] = result
            except Exception as exc:
                logger.error(
                    "Process-pool fetch failed for language=%s: %s", language, exc
                )

    return resultMap

if __name__ == "__main__":
    t1 = time.perf_counter()
    resultmap = asyncio.run(main())

    t2 = time.perf_counter()

    logger.info("Total execution time: %.2f seconds", t2 - t1)
    # print("Final results:", resultmap)