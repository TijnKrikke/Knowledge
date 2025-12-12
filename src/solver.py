from model import Question, Option, Condition, Facts, Aspect

class Solver:
    def __init__(self):
        self.facts = Facts(aspects_pos=set(), aspects_neg=set(), aspects_idc=set(), age=(0, 100), players=(0, 100), duration=0)
        self.questions_asked = set()
        
    
    def get_question(self, questions: list[Question]) -> Question | None:
        for question in questions:
            if question.text not in self.questions_asked:
                if self._is_condition_satisfied(question.condition):
                    self.questions_asked.add(question.text)
                    return question
        return None
    
    def process_answer(self, option: Option) -> bool:
        self._fire_rules(option)

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

            elif option_type == "set_age_range":
                new = self._split_range(option_value)
                self.facts.age = new
                modified = True

            elif option_type == "set_players_range":
                new = self._split_range(option_value)
                self.facts.players = new
                modified = True

            elif option_type == "set_duration":
                new = int(option_value)
                self.facts.duration = new
                modified = True

        return modified  
    
    def _split_range(self, range_str: str) -> tuple[int, int]:
        part = range_str.split("-")
        return (int(part[0]), int(part[1]))

    def _is_condition_satisfied(self, condition : Condition) -> bool:
        if condition is None:
            return True

        # Check for aspect
        if condition.todo[-1] == "?":
            aspect_name = condition.todo[:-1]
            if aspect_name in [a.name for a in self.facts.aspects_pos]:
                return False
            if aspect_name in [a.name for a in self.facts.aspects_neg]:
                return False
            if aspect_name in [a.name for a in self.facts.aspects_idc]:
                return False
            return True
              
        # Check for age

        # Check for player

        # Check for duration

        return True
