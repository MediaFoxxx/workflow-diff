from diffs import DiffEdit, DiffEditName, DiffEditDiscr, DiffEditPos, DiffEditSettings
from blocks import Block
from workflow import Workflow
from port import Port
import logging

logger = logging.getLogger(f'log.{__name__}')


def find_edited_objects(old_blocks: list[Block | Port], new_blocks: list[Block | Port]) \
        -> tuple[list[Block | Port], list[Block | Port]]:
    """Finds same Blocks (or Ports), but edited."""

    ws1 = set(old_blocks)
    ws2 = set(new_blocks)
    diff = ws1.symmetric_difference(ws2)

    ws1 -= diff
    ws2 -= diff

    wl1 = sorted(list(ws1), key=lambda block: block.guid)
    wl2 = sorted(list(ws2), key=lambda block: block.guid)

    return wl1, wl2


def compare(old_workflow: Workflow, new_workflow: Workflow) -> list[DiffEdit]:
    """Compares two Block lists and returns a Diffs list of those compares. Finds differences between same Blocks."""

    wl1, wl2 = find_edited_objects(old_workflow.blocks, new_workflow.blocks)

    for blocks in zip(wl1, wl2):
        block1 = blocks[0]
        block2 = blocks[1]

        if block1.name != block2.name:
            yield DiffEditName(block1.get_path(old_workflow.blocks), block2.name)
        if block1.position != block2.position:
            yield DiffEditPos(block2.get_path(new_workflow.blocks), block2.position)
        if block1.description != block2.description:
            yield DiffEditDiscr(block2.get_path(new_workflow.blocks), block1.description, block2.description)
        if block1.settings != block2.settings:
            yield DiffEditSettings(block2.get_path(new_workflow.blocks), block2.settings)
