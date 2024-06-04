from models.grammar_relation import SEM
# from .grammar_relation import SEM

class Procedure:
    def __init__(self, name:str,  args: "list[str]"):
        self.name = name
        self.args = args
    
    def __str__(self):
        return f"({self.name} " \
            + f"{' '.join(map(str, self.args)) if isinstance(self.args, list) else self.args})"

MAP_WORD_TO_DATA_VAR = {
    "tour": "TOUR",
    "tới": "ATIME",
    "từ": "DTIME",
    "đà_nẵng": "DN",
    "hồ_chí_minh": "HCM",
    "nha_trang": "NT",
    "phú_quốc": "PQ",
    "phương_tiện": "BY",
    "bao_lâu": "RUN-TIME",
    "bao_nhiêu": "COUNT",
    "ngày": "DATE",
    "có": "LIST",
    "nhắc": "LIST",
    "đi": "LIST",
}

def proceduralize(sem: SEM) -> "list[Procedure]":
    subj = find_subj(sem)
    theme = find_theme(sem)
    
    src = find_src(sem)
    des = find_des(sem)

    procedures: "list[Procedure]" = []

    if subj == "TOUR":
        # if subj:
        #     if theme:
        #         procedures.append(Procedure(subj + " " + theme, ["?x"]))
        #     else:
        #         procedures.append(Procedure(subj, ["?x"]))
        if des:
            procedures.append(Procedure(subj + " " + des, ["?x"]))
        else:
            procedures.append(Procedure(subj, ["?x"]))
        return Procedure("PRINT-ALL", ["?x"] + procedures)
    
    if subj == "RUN-TIME":
        procedures.append(Procedure(subj, ["?x"]))
        if src:
            procedures.append(Procedure("DTIME", ["?x", src, "?t"]))
        if des:
            procedures.append(Procedure("ATIME", ["?x", des, "?t"]))

        return Procedure("PRINT-ALL", ["?x"] + procedures)

    if subj == "BY" or subj == "DATE":
        if subj:
            if des:
                procedures.append(Procedure(subj + " " + des, ["?x"]))
            # if theme:
            #     procedures.append(Procedure(subj + " " + theme, ["?x"]))
            else:
                procedures.append(Procedure(subj, ["?x"]))
        return Procedure("PRINT-ALL", ["?x"] + procedures)


def find_subj(sem):
    which_subj = find_sem_given_predicate(sem, "WHICH")
    if which_subj and which_subj.relations:
        if isinstance(which_subj.relations[0], SEM):
            return MAP_WORD_TO_DATA_VAR[which_subj.relations[0].relations[0]]
        return MAP_WORD_TO_DATA_VAR[which_subj.relations[0]]

def find_theme(sem):
    theme = find_sem_given_predicate(sem, "THEME")
    if theme and theme.relations:
        if theme.relations[0] in MAP_WORD_TO_DATA_VAR:
            return MAP_WORD_TO_DATA_VAR[theme.relations[0]]
        elif theme.relations[0].relations[0] in MAP_WORD_TO_DATA_VAR:
            return MAP_WORD_TO_DATA_VAR[theme.relations[0].relations[0]]
        return ""

def find_verb_type(sem):
    wh = find_sem_given_predicate(sem, "WH-QUERY")
    if wh and wh.relations:
        return MAP_WORD_TO_DATA_VAR[wh.relations[0].predicate]

def find_src(sem):
    src = find_sem_given_predicate(sem, "FROM-LOC")
    if src and src.relations:
        return MAP_WORD_TO_DATA_VAR[src.relations[0].relations[0]]

def find_des(sem):
    src = find_sem_given_predicate(sem, "TO-LOC")
    if src and src.relations:
        return MAP_WORD_TO_DATA_VAR[src.relations[0].relations[0]]

def find_sem_given_predicate(sem: SEM, predicate: str) -> SEM:
    if sem.predicate == predicate:
        return sem
    else:
        found = None
        for relation in sem.relations:
            if not isinstance(relation, str):
                found = find_sem_given_predicate(relation, predicate)
            if found:
                return found