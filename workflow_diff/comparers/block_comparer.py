from diffs import Diff, DiffAdd, DiffDel
from workflow import Workflow
import logging

logger = logging.getLogger(f'log.{__name__}')


def compare(old_workflow: Workflow, new_workflow: Workflow) -> list[Diff]:
    """Compares two Block lists and returns a Diffs list of those compares. Finds added and deleted Blocks."""

    logger.info(f'First workflow consists of {len(old_workflow.blocks)} blocks.')
    logger.info(f'Second workflow consists of {len(new_workflow.blocks)} blocks.\n')

    added = set(new_workflow.blocks) - set(old_workflow.blocks)
    deleted = set(old_workflow.blocks) - set(new_workflow.blocks)

    logger.debug(f'There are only {len(added) + len(deleted)} difference:')

    if len(deleted) != 0:
        logger.debug(f'First workflow consists of: {deleted}')
    if len(added) != 0:
        logger.debug(f'Second workflow consists of: {added}')

    for block in deleted:
        yield DiffDel(block.get_path(old_workflow.blocks))
    for block in added:
        yield DiffAdd(block.get_path(new_workflow.blocks))
