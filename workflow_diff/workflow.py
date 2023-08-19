import logging
import json

from blocks import Block, create_block
from link import Link

logger = logging.getLogger(f'log.{__name__}')


def open_file(file_path: str) -> dict:
    """Open json file and return a dictionary."""

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            dict_ = json.load(f)
    except FileNotFoundError as ex:
        logger.error(ex)
        exit(-1)

    return dict_


def get_blocks(workflow: dict) -> list[Block]:
    """Returns a list of the Blocks from the workflow.json"""

    return [create_block(block) for block in workflow['blocks']]


def get_links(workflow: dict) -> list[Link]:
    """Returns a list of the Links from the workflow.json"""

    for link in workflow['links']:
        yield Link(guid=link['guid'], src=link['src']['port'], dst=link['dst']['port'])


class Workflow:
    blocks: list[Block]
    links: list[Link]

    def __init__(self, path_to_workflow: str):
        """Creating an object of Workflow from the dictionary."""

        workflow_dict = open_file(file_path=path_to_workflow)
        if 'blocks' not in workflow_dict:
            logger.error('Specified json file has wrong format.')
            exit(-1)

        self.blocks = get_blocks(workflow_dict)
        self.links = get_links(workflow_dict)
