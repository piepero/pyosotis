"""Dummy functions used by sample_tasks.py"""

import logging
import random
import time

logger = logging.getLogger(__name__)

# key constants for the shared dictionary
PROJECT_NAME = "project_name"


def clone_main(SharedDict: dict):
    """Simulates cloning the main repositories."""
    logger.info(
        f"clone_main({SharedDict[PROJECT_NAME]}): Emulate cloning of main project repositories."
    )
    for i in range(2):
        logger.info(f"clone_main: clone main {i + 1}")
        time.sleep(3)
    logger.info("clone_main: done.")


def clone_auxillary(SharedDict: dict):
    """Simulates cloning several auxillary repositories."""
    logger.info(
        f"clone_auxillary({SharedDict[PROJECT_NAME]}): Emulate cloning of auxillary repositories."
    )
    for i in range(5):
        logger.info(f"clone_remaining: clone helper {i + 1}")
        time.sleep(i + 1)
    logger.info("clone_remaining: done.")


def create_project_name(SharedDict: dict):
    """Creates a custom name for the project and stores it in SharedDict."""
    colors = ("Red", "Green", "Blue", "Violet", "Black", "White")
    shapes = ("Circle", "Square", "Triangle", "Rectangle")
    SharedDict["project_name"] = random.choice(colors) + random.choice(shapes)
    logger.info(
        f"create_project_name: The project is called {SharedDict[PROJECT_NAME]}"
    )
