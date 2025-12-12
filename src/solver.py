from typing import Set, List
from src.model import Question, Option, Result, Condition, Fact, Aspect

def is_condition_satisfied(condition : Condition, facts: Fact) -> bool:
    if condition is None:
        return True

    condition_todo = condition.todo

    # Check for aspect
    if condition_todo == "":
        aspect_name = condition_todo.split(":")[1]
        for aspect in facts.aspects:
            if aspect.name == aspect_name:
                return True
        return False
                
    # Check for age

    # Check for player

    # Check for duration

    return True

def split_range(range_str: str) -> tuple[int, int]:
    part = range_str.split("-")
    return (int(part[0]), int(part[1]))

def fire_rules (option: Option, facts: Fact) -> bool:
    modified = False

    for o in option.results:
        option_type = o.type
        option_value = o.value

        if option_type == "add_aspect":
            facts.aspects.append(Aspect(option_value))
            modified = True

        elif option_type == "set_age_range":
            new = split_range(option_value)
            facts.age = new
            modified = True

        elif option_type == "set_players_range":
            new = split_range(option_value)
            facts.players = new
            modified = True

        elif option_type == "set_duration":
            new = int(option_value)
            facts.duration = new
            modified = True

    return modified  

def ask_user(question: Question) -> Option:
    return question.options[choice]

def choose_question(questions: list[Question], facts: Fact, question_asked: set[Question]) -> Question | None:
    for question in questions:
        if question not in question_asked:
            if is_condition_satisfied(question.condition, facts):
                return question
    return None

def forward_chaining(questions: Question, facts: Fact):
    # Perform forward chaining    
    question_asked = set[Question]

    while True:
        question = choose_question(questions, facts, question_asked)
        if question is None:   
            break
        option = ask_user(question)
        fire_rules(option, facts)
        question_asked.add(question)    
    return 