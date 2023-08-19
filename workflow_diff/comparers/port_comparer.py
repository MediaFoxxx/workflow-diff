from diffs import DiffEditPort, DiffEditPortAdd, DiffEditPortDel
from workflow import Workflow
from comparers.block_difference import find_edited_objects
import logging

logger = logging.getLogger(f'log.{__name__}')


def compare(old_workflow: Workflow, new_workflow: Workflow) -> list[DiffEditPort]:
    """Compares two Block lists and returns a Diffs list of those compares. Finds added and deleted Ports."""

    wl1, wl2 = find_edited_objects(old_workflow.blocks, new_workflow.blocks)

    for blocks in zip(wl1, wl2):
        block1 = blocks[0]
        block2 = blocks[1]

        added = set(block2.ports) - set(block1.ports)
        deleted = set(block1.ports) - set(block2.ports)

        for port in deleted:
            yield DiffEditPortDel(block2.get_path(new_workflow.blocks), port.get_title())
        for port in added:
            yield DiffEditPortAdd(block2.get_path(new_workflow.blocks), port.get_title())
