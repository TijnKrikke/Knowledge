from dataclasses import dataclass
from enum import Enum

class Truth(Enum):
    NO = 0
    YES = 1
    IDC = 2
    UNKNOWN = 3

@dataclass(eq=True, frozen=True)
class Fact:
    name:str

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
class Option:
    text: str
    results: list[Fact|Aspect]

@dataclass
class Question:
    text: str
    options: list[Option]

@dataclass
class Rule:
    description: str
    condition: dict
    results: list[Fact|Aspect]

@dataclass
class KB:
    rules: list[Rule]
    questions: list[Question]
    games: list[Game]

@dataclass
class Facts:
    fact_pos: set[Fact|Aspect]
    fact_neg: set[Fact|Aspect]
    fact_idc: set[Fact|Aspect]
    fact_known: set[Fact|Aspect]
    remaining_rules: list[Rule]
    remaining_questions: list[Question]
    remaining_games: list[Game]

    def add_fact(self, fact: Fact|Aspect):
        name = fact.name

        if type(fact) is Fact:
            fact = Fact(name=name[:-1])
        elif type(fact) is Aspect:
            fact = Aspect(name=name[:-1])
        else:
            raise Exception(f"Unknown fact type: {type(fact)}")

        if name[-1] == "+":
            self.fact_pos.add(fact)
        if name[-1] == "-":
            self.fact_neg.add(fact)
        if name[-1] == "~":
            self.fact_idc.add(fact)

        self.fact_known.add(fact)