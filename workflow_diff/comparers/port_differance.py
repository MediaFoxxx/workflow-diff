from diffs import DiffEditPort, DiffEditPortName, DiffEditPortFlagP, DiffEditPortFlagB, DiffEditPortFlagR
from workflow import Workflow
from comparers.block_difference import find_edited_objects
import logging

logger = logging.getLogger(f'log.{__name__}')


def compare(old_workflow: Workflow, new_workflow: Workflow) -> list[DiffEditPort]:
    """Compares two Block lists and returns a Diffs list of those compares. Finds differences between same Ports."""

    wl1, wl2 = find_edited_objects(old_workflow.blocks, new_workflow.blocks)

    for blocks in zip(wl1, wl2):
        block1 = blocks[0]
        block2 = blocks[1]

        pl1, pl2 = find_edited_objects(list(block1.ports), list(block2.ports))

        for ports in zip(pl1, pl2):
            port1 = ports[0]
            port2 = ports[1]

            if port1.name != port2.name:
                yield DiffEditPortName(block2.get_path(new_workflow.blocks), port1.get_title(), port2.name)
            if port1.flag_p != port2.flag_p:
                yield DiffEditPortFlagP(block2.get_path(new_workflow.blocks), port1.get_title(), port2.flag_p)
            if port1.flag_b != port2.flag_b:
                yield DiffEditPortFlagB(block2.get_path(new_workflow.blocks), port1.get_title(), port2.flag_b)
            if port1.flag_r != port2.flag_r:
                yield DiffEditPortFlagR(block2.get_path(new_workflow.blocks), port1.get_title(), port2.flag_r)

