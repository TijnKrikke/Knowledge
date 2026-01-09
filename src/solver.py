from model import Question, Option, Condition, Facts, Rule, Aspect, Game

class Solver:
    def __init__(self, games: list[Game] = [], rules: list[Rule] = []):
        self.facts = Facts(aspects_pos=set(), aspects_neg=set(), aspects_idc=set(), age=(0, 100), players=(0, 100), duration=0)
        self.questions_asked = set()
        self.games_left = games
        self.rules_left = rules
        self.known_facts = []

    def get_question(self, questions: list[Question]) -> Question | None:
        self.games_left = self.get_games_left()
        if len(self.games_left) <= 1:
            return None

        all_aspects_left = []
        for game in self.games_left:
            for aspect in game.aspects:
                if aspect.name not in all_aspects_left:
                    all_aspects_left.append(aspect.name)
            all_aspects_left.append(game.aspects)
        for question in questions:
            if question.text not in self.questions_asked:
                if self._is_condition_satisfied(question.condition, all_aspects_left): 
                    self.questions_asked.add(question.text)
                    return question
        return None
    
    def process_answer(self, option: Option) -> bool:
        return self._fire_rules(option)

    def _fire_rules(self, option: Option) -> bool:
        modified = False
        for o in option.results:
            option_type = o.type
            option_value = o.value
            if option_type == "add_aspect":
                if option_value[-1] == "+":
                    self.facts.aspects_pos.add(Aspect(option_value[:-1]))
                elif option_value[-1] == "-":
                    self.facts.aspects_neg.add(Aspect(option_value[:-1]))
                elif option_value[-1] == "~":
                    self.facts.aspects_idc.add(Aspect(option_value[:-1]))
                modified = True

        if modified:
            self.loop_rules()

        return modified  

    def loop_rules(self):
        modified = True

        while modified:
            modified = False
            for rule in self.rules_left:
                if self.evaluate_rule(rule):
                    self.rules_left.remove(rule)
                    modified = True
                    for o in rule.results:
                        option_type = o.type
                        option_value = o.value
                        if option_type == "add_aspect":
                            if option_value[-1] == "+":
                                self.facts.aspects_pos.add(Aspect(option_value[:-1]))
                            elif option_value[-1] == "-":
                                self.facts.aspects_neg.add(Aspect(option_value[:-1]))
                            elif option_value[-1] == "~":
                                self.facts.aspects_idc.add(Aspect(option_value[:-1]))

    def _split_range(self, range_str: str) -> tuple[int, int]:
        part = range_str.split("-")
        return (int(part[0]), int(part[1]))

    def _is_condition_satisfied(self, condition : Condition, all_aspects_left) -> bool:
        if condition is None:
            return True

        # Check for aspect
        if condition.todo[-1] == "?":
            aspect_name = condition.todo[:-1]
            if aspect_name not in all_aspects_left:
                return False

            if aspect_name in [a.name for a in self.facts.aspects_pos]:
                return False
            if aspect_name in [a.name for a in self.facts.aspects_neg]:
                return False
            if aspect_name in [a.name for a in self.facts.aspects_idc]:
                return False
            return True

        return True

    def get_games_left(self) -> list[Game]:
        out = {a.name for a in self.facts.aspects_neg}
        required  = {a.name for a in self.facts.aspects_pos}
        matches: list[Game] = []
        for game in self.games_left:
            append = True
            for req in required:
                if req not in [a.name for a in game.aspects]:
                    append = False
            for a in game.aspects:
                if a.name in out:
                    append = False
                    break
            if append:
                matches.append(game)
        self.games_left = matches
        return matches

    def evaluate_rule(self, rule: Rule) -> bool:
        return self.evaluate_expr(rule.condition)

    def evaluate_expr(self, expr: dict) -> bool:
        (operand, value), = expr.items()

        if operand == "and":
            return all(self.evaluate_expr(sub_expr) for sub_expr in value)

        if operand == "or":
            return any(self.evaluate_expr(sub_expr) for sub_expr in value)

        if operand == "fact":
            return value in self.known_facts

        if operand == "aspect":
            return Aspect(str(value)) in self.facts.aspects_pos

        raise Exception(f"Unknown operand {operand}")