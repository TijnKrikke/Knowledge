class Aspect:
    name: str

class Game:
    name: str
    description: str
    age: tuple[int, int]
    players: tuple[int, int]
    duration: int
    aspects: list[Aspect]

class Condition:
    todo: str

class Result:
    type: str # add_aspect, "set_age", "set_players"
    value: str

class Option:
    text: str
    results: list[Result]

class Question:
    text: str
    options: list[Option]
    condition: Condition
