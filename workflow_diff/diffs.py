from dataclasses import dataclass
from abc import ABC
import logging
from blocks import BlockSettings

logger = logging.getLogger(f'log.{__name__}')


@dataclass(slots=True)
class Diff(ABC):
    """Class of difference between two objects."""

    block_path: str

    def __str__(self):
        return self.block_path


@dataclass(slots=True)
class DiffAdd(Diff):
    pass


@dataclass(slots=True)
class DiffDel(Diff):
    pass


@dataclass(slots=True)
class DiffLink(Diff):
    port: str
    block_path2: str
    port2: str

    def __str__(self):
        return f'{self.block_path}, {self.port}  ->  {self.block_path2}, {self.port2}'


@dataclass(slots=True)
class DiffLinkAdd(DiffLink):
    pass


@dataclass(slots=True)
class DiffLinkDel(DiffLink):
    pass


@dataclass(slots=True)
class DiffEdit(Diff):
    pass


@dataclass(slots=True)
class DiffEditName(DiffEdit):
    new_name: str

    def __str__(self):
        return f'{self.block_path}: The name has been changed to "{self.new_name}"'


@dataclass(slots=True)
class DiffEditDiscr(DiffEdit):
    old_discr: str
    new_discr: str

    def __str__(self):
        return f'{self.block_path}: The description has been changed from "{self.old_discr}" to "{self.new_discr}"'


@dataclass(slots=True)
class DiffEditPos(DiffEdit):
    new_pos: tuple[int]

    def __str__(self):
        return f'{self.block_path}: Has been moved to {self.new_pos}'


@dataclass(slots=True)
class DiffEditPort(DiffEdit):
    port: str


@dataclass(slots=True)
class DiffEditPortAdd(DiffEditPort):
    pass

    def __str__(self):
        return f'{self.block_path}: Port {self.port} has been added'


@dataclass(slots=True)
class DiffEditPortDel(DiffEditPort):
    pass

    def __str__(self):
        return f'{self.block_path}: Port {self.port} has been deleted'


@dataclass(slots=True)
class DiffEditPortName(DiffEditPort):
    new_name: str

    def __str__(self):
        return f'{self.block_path}: Port {self.port} has been renamed to "{self.new_name}"'


@dataclass(slots=True)
class DiffEditPortFlag(DiffEditPort):
    flag: bool


@dataclass(slots=True)
class DiffEditPortFlagP(DiffEditPortFlag):

    def __str__(self):
        return f'{self.block_path}: Port {self.port} - flag "P" has been changed to "{self.flag}"'


@dataclass(slots=True)
class DiffEditPortFlagB(DiffEditPortFlag):

    def __str__(self):
        return f'{self.block_path}: Port {self.port} - flag "B" has been changed to "{self.flag}"'


@dataclass(slots=True)
class DiffEditPortFlagR(DiffEditPortFlag):

    def __str__(self):
        return f'{self.block_path}: Port {self.port} - flag "R" has been changed to "{self.flag}"'


@dataclass(slots=True)
class DiffEditSettings(DiffEdit):
    settings: BlockSettings

    def __str__(self):
        return f'{self.block_path}: Settings have been changed to {self.settings.get_title()}'


def print_diffs(list_diffs: list[Diff]):
    """Prints a list of Diffs"""

    if len(list_diffs) == 0:
        print("No differences!")
    else:
        added = [diff for diff in list_diffs if isinstance(diff, DiffAdd)]
        deleted = [diff for diff in list_diffs if isinstance(diff, DiffDel)]
        edited = [diff for diff in list_diffs if isinstance(diff, DiffEdit)]
        link_added = [diff for diff in list_diffs if isinstance(diff, DiffLinkAdd)]
        link_deleted = [diff for diff in list_diffs if isinstance(diff, DiffLinkDel)]

        if deleted:
            print('\nBlocks have been deleted:')
            for diff in deleted:
                print(diff)

        if added:
            print('\nBlocks have been added:')
            for diff in added:
                print(diff)

        if edited:
            print('\nBlocks have been edited:')
            for diff in sorted(edited, key=lambda res: res.block_path):
                print(diff)

        if link_deleted:
            print('\nLinks have been deleted:')
            for diff in sorted(link_deleted, key=lambda res: res.block_path):
                print(diff)

        if link_added:
            print('\nLinks have been added:')
            for diff in sorted(link_added, key=lambda res: res.block_path):
                print(diff)
