from dataclasses import dataclass


@dataclass
class Storage:
    open_agencies: set
    winners: int
