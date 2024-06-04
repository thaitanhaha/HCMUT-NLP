from models.data import *
from models.maltparser import Dependency
# from .data import *
# from .maltparser import Dependency

class Relation:
    def __init__(self, type: str, left: str, right: str):
        self.type = type    # e.g. AGENT
        self.left = left    # e.g. s1
        self.right = right  # e.g. đến
    
    def __str__(self) -> str:
        return f"({self.left} {self.type} {self.right})"

class SEM:
    def __init__(self, predicate: str, variable, relations=None):
        self.predicate = predicate
        self.variable = variable
        self.relations = relations if relations else []
    
    def __str__(self) -> str:
        return f"({self.predicate} {self.variable}" \
                + f"{' ' + ' '.join(map(str, self.relations)) if self.relations else ''})"


def create_sem(word, existing_variables):
    var = create_variable(word, existing_variables)
    if POS[word] not in [NAME]:
        return word, None
    sem = SEM(POS[word], var, [word])
    return sem, var


def create_variable(name: str, existing_variables: "list[str]") -> str:
    letter = name[0]
    i = 0
    while True:
        i += 1
        var = f"{letter}{i}"
        if var not in existing_variables:
            return var


def relationalize(dependencies: "list[Dependency]") -> "list[Relation]":
    relations = []
    variables = []

    for dependency in dependencies:
        if dependency.relation == "query":
            relations.append(Relation("QUERY", "s1", dependency.tail))

        elif dependency.relation == "noun_query":
            flag = False
            for relation in relations:
                if relation.type == "QUERY":
                    flag = True
                    break
            if flag:
                relations.append(Relation("CO_QUERY", "s1", dependency.head))
            else:
                relations.append(Relation("QUERY", "s1", dependency.head))

        elif dependency.relation == "root":
            variables.append("s1")
            relations.append(Relation("PRED", "s1", dependency.tail))

        elif dependency.relation == "subj":
            if dependency.tail in PRONOUN:
                relations.append(Relation("AGENT", "s1", dependency.tail))

        elif dependency.relation == "nmod":
            if POS[dependency.tail] == NAME:
                dependent_sem, dependent_var = create_sem(dependency.tail, variables)
                if dependent_var is not None:
                    variables.append(dependent_var)
                relations.append(Relation("DES", "s1", dependent_sem))
            else:
                dependent_sem, dependent_var = create_sem(dependency.tail, variables)
                if dependent_var is not None:
                    variables.append(dependent_var)
                relations.append(Relation("THEME", "s1", dependent_sem))


        elif dependency.relation == "pobj" and dependency.head == "từ":
            dependent_sem, dependent_var = create_sem(dependency.tail, variables)
            if dependent_var is not None:
                variables.append(dependent_var)
            relations.append(Relation("SRC", "s1", dependent_sem))

        elif dependency.relation == "pobj" and dependency.head == "tới":
            dependent_sem, dependent_var = create_sem(dependency.tail, variables)
            if dependent_var is not None:
                variables.append(dependent_var)
            relations.append(Relation("DES", "s1", dependent_sem))


    return relations
