from context import Context
from diffs import print_diffs
from workflow import Workflow

import importlib
import pkgutil
import logging


def set_logger():
    """"""

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(levelname)-8s: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('log').addHandler(console)


set_logger()
logger = logging.getLogger(f'log.{__name__}')


def get_comparers() -> list:
    """Returning a list of comparers from 'comparers' package."""

    folder_name = "comparers"
    return [
        importlib.import_module(f"{folder_name}.{name.name}")
        for name in pkgutil.iter_modules([folder_name])
    ]


def controller():

    context = Context()
    context.load_protoblocks()

    old_workflow = Workflow(path_to_workflow=context.first_path_to_workflow)
    new_workflow = Workflow(path_to_workflow=context.second_path_to_workflow)

    logger.debug('First workflow includes:\n')
    for block in old_workflow.blocks:
        logger.debug(block)

    logger.debug('Second workflow includes:\n')
    for block in new_workflow.blocks:
        logger.debug(block)

    comparers = get_comparers()
    diffs = []

    for comparer in comparers:
        diffs += comparer.compare(old_workflow, new_workflow)

    print_diffs(diffs)


if __name__ == '__main__':
    controller()
