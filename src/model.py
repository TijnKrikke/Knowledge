from dataclasses import dataclass

@dataclass(eq=True, frozen=True)
class Aspect:
    name: str

@dataclass
class Game:
    name: str
    description: str
    age: tuple[int, int]
    players: tuple[int, int]
    duration: int
    aspects: set[Aspect]

@dataclass
class Condition:
    todo: str #TODO

@dataclass
class Result:
    type: str # add_aspect, "set_age", "set_players"
    value: str

@dataclass
class Option:
    text: str
    results: list[Result]

@dataclass
class Question:
    text: str
    options: list[Option]
    condition: Condition

@dataclass
class Rule:
    description: str
    condition: dict
    results: list[Result]

@dataclass
class KB:
    rules: list[Rule]
    questions: list[Question]
    games: list[Game]

@dataclass
class Facts:
    aspects_pos: set[Aspect]
    aspects_neg: set[Aspect]
    aspects_idc: set[Aspect]
    age: tuple[int, int]
    players: tuple[int, int]
    duration: int
