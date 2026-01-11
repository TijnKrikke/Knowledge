from model import Question, Option, Condition, Facts, Rule, Aspect, Game, Fact
import random

class Solver:
    def __init__(self, games: list[Game] = [], rules: list[Rule] = []):
        self.facts = Facts(aspects_pos=set(), aspects_neg=set(), aspects_idc=set(), fact_pos=set(), fact_neg=set(), fact_idc=set())
        self.questions_asked = set()
        self.games_left = games
        self.rules_left = rules
        self.known_facts = []

        self.question_queue = []
        self.cur_goal_aspect = ""

    def get_question(self, questions: list[Question]) -> Question | None:
        def identy_rules_and_questions(check_aspect):
            #check questions
            for question in questions:
                if question.text in self.questions_asked:
                    continue
                if question.condition.todo[:-1] == check_aspect.name:
                    self.question_queue.append(question)
            # print(self.question_queue, "question")

            rules = []
            for rule in self.rules_left:
                for result in rule.results:
                    if result.value[:-1] == check_aspect.name:
                        rules.append(rule) 
                        print("rule found: ", rule)       
            return rules
        
        def check_rules(c_rules):
            print("Checking rule")
            for c_rule in c_rules:
                check_atoms(c_rule.condition)
                
            return None
        
        def check_atoms(expr: dict) -> bool:
            (operand, value), = expr.items()

            if operand == "and":
                print("found and")
                for sub_expr in value:
                    check_atoms(sub_expr)
                return True

            if operand == "or":
                print("found or")
                for sub_expr in value:
                    check_atoms(sub_expr)
                return True

            if operand == "fact":
                print("Found fact: ", value)
                value = value[:-1]
                if value not in self.facts.fact_pos and value not in self.facts.fact_idc and value not in self.facts.fact_neg:
                    identy_rules_and_questions(Aspect(str(value)))
                return True

            if operand == "aspect":
                print("Found aspect: ", value)
                value = value[:-1]
                if value not in self.facts.aspects_pos and value not in self.facts.aspects_idc and value not in self.facts.aspects_neg:
                    identy_rules_and_questions(Aspect(str(value)))
                return True
                
        

        if len(self.question_queue) > 0:
            if self.cur_goal_aspect not in self.facts.aspects_pos and self.cur_goal_aspect not in self.facts.aspects_idc and self.cur_goal_aspect not in self.facts.aspects_neg:
                return self.question_queue.pop(0)
            else:
                self.question_queue = []
            
        self.games_left = self.get_games_left()
        if len(self.games_left) <= 1:
            return None

        #Note, this is not equal to unproven aspects, its a set of aspects that the games leftover have.
        all_aspects_left = []
        for game in self.games_left:
            for aspect in game.aspects:
                if aspect not in all_aspects_left:
                    all_aspects_left.append(aspect)

        # can be already proven, fix later
        # IMPORTANT: will not terminate until lpgic is fixed (dont ask questions already asked)
        goal_aspect = random.choice(all_aspects_left)
        self.cur_goal_aspect = goal_aspect
        
        rules = identy_rules_and_questions(self.cur_goal_aspect)
        check_rules(rules)

        # no question found, use random
        if len(self.question_queue) <= 0:
            print("check if weird behaviour")
            return random.choice(questions)
        return self.question_queue.pop(0)

    
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
            if option_type == "add_fact":
                if option_value[-1] == "+":
                    self.facts.fact_pos.add(Fact(option_value[:-1]))
                elif option_value[-1] == "-":
                    self.facts.fact_neg.add(Fact(option_value[:-1]))
                elif option_value[-1] == "~":
                    self.facts.fact_idc.add(Fact(option_value[:-1]))
                modified = True

        if modified:
            self.loop_rules()

        return modified  

    def loop_rules(self):
        modified = True

        while modified:
            modified = False
            for rule in self.rules_left:
                print("we are in loop func")
                if self.evaluate_rule(rule):
                    print("Yippiee")
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
                        if option_type == "add_fact":
                            if option_value[-1] == "+":
                                self.facts.fact_pos.add(Fact(option_value[:-1]))
                            elif option_value[-1] == "-":
                                self.facts.fact_neg.add(Fact(option_value[:-1]))
                            elif option_value[-1] == "~":
                                self.facts.fact_idc.add(Fact(option_value[:-1]))

    def _split_range(self, range_str: str) -> tuple[int, int]:
        part = range_str.split("-")
        return (int(part[0]), int(part[1]))

    # def _is_condition_satisfied(self, condition : Condition, all_aspects_left) -> bool:
    #     if condition is None:
    #         return True

    #     # Check for aspect
    #     if condition.todo[-1] == "?":
    #         aspect_name = condition.todo[:-1]

    #         if aspect_name not in all_aspects_left:
    #             return False

    #         if aspect_name in [a.name for a in self.facts.aspects_pos]:
    #             return False
    #         if aspect_name in [a.name for a in self.facts.aspects_neg]:
    #             return False
    #         if aspect_name in [a.name for a in self.facts.aspects_idc]:
    #             return False
    #         return True

    #     return True

    def get_games_left(self) -> list[Game]:
        print("NEG: ",  self.facts.aspects_neg)
        print("POS: ",  self.facts.aspects_pos)

        print("NEG: ",  self.facts.fact_neg)
        print("POS: ",  self.facts.fact_pos)

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

        print("operand", operand)
        print("value", value)

        if operand == "and":
            sum_bool = 0
            for sub_expr in value:
                sum_bool += self.evaluate_expr(sub_expr)
            print(sum_bool, len(value))
            return sum_bool == len(value)
            return all(self.evaluate_expr(sub_expr) for sub_expr in value)

        if operand == "or":
            sum_bool = 0
            for sub_expr in value:
                sum_bool += self.evaluate_expr(sub_expr)
            print(sum_bool)
            return sum_bool >= 1

        if operand == "fact":
            return Fact(str(value[:-1])) in self.facts.fact_pos

        if operand == "aspect":
            return Aspect(str(value[:-1])) in self.facts.aspects_pos # in idc too I think

        raise Exception(f"Unknown operand {operand}")