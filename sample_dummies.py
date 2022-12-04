"""Dummy functions used by sample_tasks.py"""

import logging
import time

logger = logging.getLogger(__name__)


def clone_main():
    logger.info("clone_main: Emulating the cloning of the main project repositories.")
    for i in range(2):
        logger.info(f"clone_main: clone main {i + 1}")
        time.sleep(3)
    logger.info("clone_main: done.")


def clone_remaining():
    logger.info(
        "clone_remaining: Emulating the cloning of additional main project repositories."
    )
    for i in range(5):
        logger.info(f"clone_remaining: clone helper {i + 1}")
        time.sleep(i + 1)
    logger.info("clone_remaining: done.")
