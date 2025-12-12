import yaml
import os
from typing import Optional

from model import KB, Question, Option, Result, Condition, Game, Aspect


def load_kb(path: Optional[str] = None) -> KB:
    if path is None:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "resources", "kb.yml"))

    with open(path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    questions = []
    for question in data.get("questions", []):
        options = []
        for o in question.get("options", []):
            results = []
            for r in o.get("results", []):
                results.append(Result(type=r.get("type"), value=r.get("value")))
            options.append(Option(text=o.get("text"), results=results))

        condition = None
        if question.get("condition") is not None:
            condition_obj = question.get("condition")
            condition = Condition(todo=str(condition_obj))

        questions.append(Question(text=question.get("text"), options=options, condition=condition))

    games = []
    for game in data.get("games", []):
        aspects = {Aspect(name=a) for a in game.get("aspects", [])}
        age = tuple(game.get("age", [0, 0]))
        players = tuple(game.get("players", [0, 0]))
        games.append(
            Game(
                name=game.get("name"),
                description=game.get("description"),
                age=age,
                players=players,
                duration=game.get("duration", 0),
                aspects=aspects,
            )
        )

    return KB(questions=questions, games=games)
