# Configure a basic logger so each step is visible in console output.
import logging
import os

import requests

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
logger = logging.getLogger(__name__)

# Base URL template for fetching Harry Potter books by language.


class APIService:
    BOOKS_URL = "https://potterapi-fedeperin.vercel.app/{}/books"

    def __init__(self, max_workers: int = 1):
        self.max_workers = max_workers

    async def fetch_data(self, language):
        # 2. Get the unique Process ID of the worker currently running this function
        current_pid = os.getpid()

        logger.info(
            "Starting book fetch for language=%s on Worker PID=%s (max_workers=%s)", 
            language, 
            current_pid, 
            self.max_workers
        )

        try:
            response = requests.get(self.BOOKS_URL.format(language), timeout=10)
            response.raise_for_status()
            books = response.json()

            logger.info(
                "Fetched %s books successfully for language=%s on Worker PID=%s",
                len(books) if isinstance(books, list) else "data",
                language,
                current_pid,
            )
            return books

        except requests.RequestException as exc:
            logger.exception("Failed to fetch books for language=%s: %s", language, exc)
            raise