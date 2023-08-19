from diffs import DiffLink, DiffLinkAdd, DiffLinkDel
from workflow import Workflow
from blocks import Block
from port import Port
import logging

logger = logging.getLogger(f'log.{__name__}')


def find_block_in_block_list(blocks_list: list[Block], port_guid: str) -> tuple[Block, Port]:
    """Finds a Blocks in the workflow by his Port (port_guid)."""

    for block in blocks_list:
        for port in block.ports:
            if port.guid == port_guid:
                return block, port


def compare(old_workflow: Workflow, new_workflow: Workflow) -> list[DiffLink]:
    """Compares two Workflows and returns a Diffs list of those compares. Finds added and deleted Links."""

    added = set(new_workflow.links) - set(old_workflow.links)
    deleted = set(old_workflow.links) - set(new_workflow.links)

    for link in deleted:
        block1, port1 = find_block_in_block_list(old_workflow.blocks, link.src)
        block2, port2 = find_block_in_block_list(old_workflow.blocks, link.dst)

        yield DiffLinkDel(block1.get_path(old_workflow.blocks), port1.get_title(),
                          block2.get_path(old_workflow.blocks), port2.get_title())
    for link in added:
        block1, port1 = find_block_in_block_list(new_workflow.blocks, link.src)
        block2, port2 = find_block_in_block_list(new_workflow.blocks, link.dst)

        yield DiffLinkAdd(block1.get_path(new_workflow.blocks), port1.get_title(),
                          block2.get_path(new_workflow.blocks), port2.get_title())
