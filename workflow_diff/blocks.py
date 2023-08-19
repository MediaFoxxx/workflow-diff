from abc import ABC
from dataclasses import dataclass, field
from port import Port
from context import protoblocks


@dataclass(slots=True, frozen=True)
class BlockSettings:
    """Class of settings for Block."""

    memory: int
    cpu: int
    timeout: int

    def get_title(self) -> str:
        params = []
        if self.memory:
            params.append(f"Memory: {self.memory}")

        if self.cpu:
            params.append(f"CPU: {self.cpu}")

        if self.timeout:
            params.append(f"Timeout: {self.timeout}")

        return f'({", ".join(params)})'


@dataclass(slots=True, frozen=True)
class Block(ABC):
    """Class of block from a workflow."""

    guid: str = field(compare=True)
    type: str = field(compare=False)
    name: str = field(compare=False)
    parent: str = field(compare=False)
    position: tuple[int] = field(compare=False)
    description: str = field(compare=False)
    settings: BlockSettings = field(compare=False)
    ports: tuple[Port] = field(compare=False)

    @classmethod
    def from_dict(cls, dictionary: dict):
        """Creating an object of Block from the dictionary."""

        ports = cls._get_ports(dictionary['ports'])
        description = cls._get_description(dictionary['description'], dictionary['description_default'])
        settings = cls._get_settings(dictionary)

        return cls(
            guid=dictionary['guid'],
            type=dictionary['type'],
            name=dictionary['name'],
            parent=dictionary['parent'],
            position=tuple(dictionary['ui']['position'].values()),
            description=description,
            settings=settings,
            ports=ports
        )

    @staticmethod
    def _get_settings(dictionary: dict) -> BlockSettings:
        """"""

        if dictionary.get('resources_customized') is not None:
            memory = dictionary['resources_customized']['run']['requests']['memory']
            cpu = dictionary['resources_customized']['run']['requests']['cpu']
        else:
            memory, cpu = None, None

        timeout = dictionary.get('idle_timeout_user')

        return BlockSettings(memory, cpu, timeout)

    @staticmethod
    def _get_description(description: dict, description_default: dict) -> str | None:
        """Returns a tuple of Ports which are included in the Block."""

        if description is not None:
            return description['']
        elif description_default is not None:
            return description_default['']

        return description

    @staticmethod
    def _get_ports(ports: list[dict]) -> tuple[Port]:
        """Returns a tuple of Ports which are included in the Block."""

        return tuple(Port.from_dict(port) for port in ports)

    def get_title(self) -> str:
        """Returns briefly block description."""

        return self.name

    def get_path(self, workflow: list) -> str:
        """Returns a path of Blocks parents."""

        parent_guid = self.parent
        list_of_parents = [self.get_title()]

        while parent_guid is not None:
            for block in workflow:
                if block.guid == parent_guid:
                    list_of_parents.append(block.get_title())
                    parent_guid = block.parent

                    break

        block_path = ''
        for parent in list(reversed(list_of_parents))[:-1]:
            block_path += parent + ' / '
        block_path += list_of_parents[0]

        return block_path


@dataclass(slots=True, frozen=True)
class Composite(Block):
    """Class of composite block from workflow."""

    pass


@dataclass(slots=True, frozen=True)
class Protoblock(Block):
    """Class of protoblock block from workflow."""

    protoblock_id: str = field(compare=False)
    protoblock_version: int = field(compare=False)
    protoblock_name: str = field(compare=False)

    @classmethod
    def from_dict(cls, dictionary: dict):
        ports = cls._get_ports(dictionary['ports'])
        description = cls._get_description(dictionary['description'], dictionary['description_default'])
        settings = cls._get_settings(dictionary)
        protoblock_id = dictionary['protoblock']['id']
        protoblock_version = dictionary['protoblock']['version']

        if protoblocks:
            protoblock_name = cls._get_protoblock_name(protoblock_id, protoblock_version)
        else:
            protoblock_name = None

        return cls(
            guid=dictionary['guid'],
            type=dictionary['type'],
            name=dictionary['name'],
            parent=dictionary['parent'],
            position=tuple(dictionary['ui']['position'].values()),
            description=description,
            settings=settings,
            ports=ports,
            protoblock_id=protoblock_id,
            protoblock_version=protoblock_version,
            protoblock_name=protoblock_name
        )

    @staticmethod
    def _get_protoblock_name(pb_id: str, pb_version: str) -> str:
        """Returns a name of protoblock."""

        id_version = f'{pb_id}-{pb_version}'

        if id_version in protoblocks[0].keys():
            name = protoblocks[0][id_version]
        elif id_version in protoblocks[1].keys():
            name = protoblocks[1][id_version]
        else:
            name = None

        return name

    def get_title(self) -> str:

        if self.protoblock_name is not None and self.protoblock_name != self.name:
            return f"{self.name} ({self.protoblock_name})"
        else:
            return f"{self.name}"


def create_block(dictionary: dict) -> Block:
    """A block factory which returns Composite of Protoblock object."""

    factory_dict = {
        'COMPOSITE': Composite,
        'BLOCK': Protoblock
    }
    return factory_dict[dictionary['type']].from_dict(dictionary)
