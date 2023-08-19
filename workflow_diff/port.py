from dataclasses import dataclass, field


@dataclass(slots=True, unsafe_hash=True)
class Port:
    """Class of port for Block."""

    type: str = field(compare=False)
    guid: str = field(compare=True)
    name: str = field(compare=False)
    flag_p: bool = field(compare=False)
    flag_b: bool = field(compare=False)
    flag_r: bool = field(compare=False)

    @classmethod
    def from_dict(cls, dictionary: dict):
        """Creating an object of Port from the dictionary."""

        return cls(
            type=dictionary['type'],
            guid=dictionary['guid'],
            name=dictionary['name'],
            flag_p=dictionary.get('parameter'),
            flag_b=dictionary.get('batch'),
            flag_r=dictionary.get('history', {}).get('enabled')
        )

    def get_title(self) -> str:
        """Returns briefly block description."""

        return f"{self.name} ({self.type})"
