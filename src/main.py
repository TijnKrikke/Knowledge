import yaml

from src.model import KB

with open("../resources/kb.yml") as stream:
    try:
        ymlstring = yaml.safe_load(stream)

        # Workaround for not having empty constructor
        kb = KB(None, None)

        kb.questions = ymlstring.get("questions")
        kb.games = ymlstring.get("games")

        print(kb)
    except yaml.YAMLError as exc:
        print(exc)