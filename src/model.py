from dataclasses import dataclass

@dataclass
class Aspect:
    name: str

@dataclass
class Game:
    name: str
    description: str
    age: tuple[int, int]
    players: tuple[int, int]
    duration: int
    aspects: list[Aspect]

@dataclass
class Condition:
    todo: str

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
class KB:
    questions: list[Question]
    games: list[Game]

@dataclass
class Fact:
    aspects: list[Aspect]
    age: tuple[int, int]
    players: tuple[int, int]
    duration: int
