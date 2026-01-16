from model import Question, Option, Facts, Rule, Aspect, Game, Fact, KB, Truth
import random

class Solver:
    def __init__(self, kb: KB, debug=False):
        self.kb = kb
        self.facts = Facts(
            fact_pos=set(),
            fact_neg=set(),
            fact_idc=set(),
            fact_known=set(),
            remaining_rules=kb.rules.copy(),
            remaining_games=kb.games.copy()
        )

        self.reason_unknown = None
        self.cur_goal_aspect = None
        self.cur_sub_goal = None
        self.debug = debug

    def get_question(self) -> Question | None:
        if len(self.facts.remaining_games) <= 1:
            # Bypass looking for a question if a game has been determined
            return None

        if self.cur_goal_aspect is None or self.cur_goal_aspect in self.facts.fact_known:
            # Set new goal by inspecting remaining unknown aspects from the list of possible games
            aspects = set()
            for game in self.facts.remaining_games:
                aspects.update(game.aspects)

            # Remove aspects that are already known
            aspects = aspects - self.facts.fact_known

            if aspects:
                self.cur_goal_aspect = random.choice(list(aspects))
                if self.debug:
                    print(f"New goal: {self.cur_goal_aspect}")
            else:
                if self.debug:
                    print(f"Exhausted all aspects")
                return None

        return self.find_next_question(self.cur_goal_aspect, set(), set())

 
    def get_aspects(self):
        aspects_pos = [fact for fact in self.facts.fact_pos if type(fact) is Aspect]
        aspects_neg = [fact for fact in self.facts.fact_neg if type(fact) is Aspect]
        return aspects_pos, aspects_neg


    def find_next_question(self, target_fact: Fact|Aspect, inspected_rules: set[Rule], inspected_questions: set[Question]) -> Question | None:
        self.cur_sub_goal = target_fact

        # Check for a question that can directly answer the goal
        for question in self.kb.questions:
            for option in question.options:
                for result in option.results:
                    if result.name[:-1] == target_fact.name:
                        return question

        # Recursively check rules to find new target goal that can answer original goal
        for rule in self.kb.rules:
            for result in rule.results:
                if result.name[:-1] == target_fact.name:
                    # Infer new target by inspecting unknown rule conditions
                    new_goal = self.find_goal_from_condition(rule.condition)
                    if new_goal is None:
                        break

                    if self.debug:
                        print(f"New subgoal: {new_goal}")

                    return self.find_next_question(new_goal, inspected_rules, inspected_questions)

        # Exhausted all options
        if self.debug:
            print(f"Exhausted all questions")
        return None

    def find_goal_from_condition(self, condition: dict) -> Fact | None:
        _ = self.evaluate_expr(condition)

        return self.reason_unknown

    def get_games_left(self) -> list[Game]:
        out = {a.name for a in self.facts.fact_neg if type(a) is Aspect}
        required = {a.name for a in self.facts.fact_pos if type(a) is Aspect}

        matches: list[Game] = []
        for game in self.facts.remaining_games:
            append = True
            for req in required:
                if req not in [a.name for a in game.aspects]:
                    if self.debug:
                        print(f"> Game {game.name} Missing required aspect: {req}")
                    append = False
            for a in game.aspects:
                if a.name in out:
                    if self.debug:
                        print(f"> Game {game.name} Has forbidden aspect: {a}")
                    append = False
                    break
            if append:
                matches.append(game)
        self.facts.remaining_games = matches
        return matches

    def process_answer(self, option: Option):
        for result in option.results:
            if self.debug:
                print(f"Learned new fact: {result}")
            self.facts.add_fact(result)

            if result.name[-1] == "~":
                self.cur_goal_aspect = None

        self.loop_rules()

    def loop_rules(self):
        modified = True

        while modified:
            modified = False
            for rule in self.facts.remaining_rules[:]:
                truth = self.evaluate_expr(rule.condition)


                if truth is not Truth.UNKNOWN:
                    operand = "~"
                    if truth is Truth.YES:
                        operand = "+"
                    elif truth is Truth.NO:
                        operand = "-"

                    for result in rule.results:
                        if type(result) is Fact:
                            result = Fact(result.name[:-1]+operand)
                        else:
                            result = Aspect(result.name[:-1]+operand)

                        self.facts.add_fact(result)
                        self.facts.remaining_rules.remove(rule)
                        if self.debug:
                            print(f"Inferred new fact: {result}")
                        modified = True
                        break

    def evaluate_expr(self, expr: dict) -> Truth:
        self.reason_unknown = None
        return self.rec_evaluate_expr(expr)

    def rec_evaluate_expr(self, expr: dict) -> Truth:
        (operand, value), = expr.items()

        generator = (self.rec_evaluate_expr(sub_expr) for sub_expr in value)
        if operand == "and":
            temp = self.reason_unknown
            self.reason_unknown = None
            truth = self.evaluate_all(generator)
            if truth is not Truth.UNKNOWN:
                self.reason_unknown = temp

            return truth

        if operand == "or":
            temp = self.reason_unknown
            self.reason_unknown = None
            truth = self.evaluate_any(generator)
            if truth is not Truth.UNKNOWN:
                self.reason_unknown = temp

            return truth

        fact = None

        if operand == "fact":
            fact = Fact(str(value[:-1]))
        if operand == "aspect":
            fact = Aspect(str(value[:-1]))

        if fact is None:
            raise Exception(f"Unknown operand {operand}")

        inverted = True if str(value[-1]) == "-" else False
        if fact in self.facts.fact_pos:
            return Truth.NO if inverted else Truth.YES
        elif fact in self.facts.fact_neg:
            return Truth.YES if inverted else Truth.NO
        elif fact in self.facts.fact_idc:
            return Truth.IDC
        else:
            if self.reason_unknown is None:
                self.reason_unknown = fact
            return Truth.UNKNOWN

    def evaluate_all(self, iterable) -> Truth:
        # It behaves in this order:
        # Any NO results in NO           [_ _ -] => -
        # Any UNKNOWN results in UNKNOWN [_ _ ?] => ?
        # IDC leans towards YES          [+ ~ ~] => +
        # Unless all are IDC             [~ ~ ~] => ~

        any_unknown = False
        any_pos = False
        for x in iterable:
            if x is Truth.NO:
                return Truth.NO
            elif x is Truth.UNKNOWN:
                any_unknown = True
            elif x is Truth.YES:
                any_pos = True

        return Truth.UNKNOWN if any_unknown\
            else Truth.YES if any_pos else Truth.IDC

    def evaluate_any(self, iterable) -> Truth:
        # It behaves in this order:
        # Any YES results in YES         [_ _ +] => +
        # Any UNKNOWN results in UNKNOWN [_ _ ?] => ?
        # IDC leans towards NO           [- ~ ~] => -
        # Unless all are IDC             [~ ~ ~] => ~

        any_unknown = False
        any_neg = False
        for x in iterable:
            if x is Truth.YES:
                return Truth.YES
            elif x is Truth.UNKNOWN:
                any_unknown = True
            elif x is Truth.NO:
                any_neg = True

        return Truth.UNKNOWN if any_unknown \
            else Truth.NO if any_neg else Truth.IDC
