from models.data import *
# from .data import *
import re
from unicodedata import normalize

def tokenize(text: str, want_to_print = False) -> "list[str]":
    text = normalize("NFC", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"(.)\?", r"\1 ?", text)
    text = text.lower()

    for token in TOKENIZE_DICT:
        text = re.sub(token, TOKENIZE_DICT[token], text)

    tokens = text.split(" ")

    for token in tokens:
        if token not in POS:
            tokens = list(filter(lambda x: x != token, tokens))
    
    if want_to_print:
        print(tokens)
        for token in tokens:
            print(POS[token], end=" ")
        print('\n')
    return tokens

ROOT = "ROOT"

RIGHT_ARC = {
    N: {Q: "noun_query", NAME: "nmod"},
    V: {PUNC: "punc", NAME: "nmod", PP: "pp", YN: "yesno", 
        N: "dobj", ADV: "adv", V: "vmod", Q: "query"},
    Q: [],
    PP: {N: "pobj", NAME: "pobj", PP: "pmod"},
    NAME: [],
    ROOT: {V: "root"},
    YN: [],
    ADV: [],
    P: [],
    DET: [],
    AUX: [],
}

LEFT_ARC = {
    N: {V: "subj", NAME: "nmod"},
    V: [],
    Q: {N: "noun_query"},
    PP: [],
    NAME: [],
    ROOT: [],
    YN: [],
    ADV: {V: "adv"},
    P: {N: "det"},
    DET: {N: "det"},
    AUX: [],
}

class Dependency:
    
    def __init__(self, relation: str, head: str, tail: str):
        self.relation = relation 
        self.head = head 
        self.tail = tail 
    
    def __str__(self) -> str:
        return f"\"{self.head}\" --{self.relation} -> \"{self.tail}\""

def malt_parse_helper(tokens: "list[str]") -> "list[Dependency]":
    buffer = tokens.copy()
    stack = [ROOT]
    dependencies: "list[Dependency]" = []
    root_verb = None

    while True:
        # print(buffer)
        # print(stack)
        # print('\n\n')

        if not buffer:
            break
        
        stack_item = stack[-1]
        buffer_item = buffer[0]

        stack_item_type = POS[stack_item] if stack_item is not ROOT else stack_item
        buffer_item_type = POS[buffer_item]

        
        if buffer_item_type == V and root_verb is None:
            root_verb = buffer_item
        
        if isinstance(buffer_item_type, tuple):
            if root_verb is None:
                root_verb = buffer_item
                buffer_item_type = buffer_item_type[0]
            elif root_verb != buffer_item:
                buffer_item_type = buffer_item_type[1]
            else:
                buffer_item_type = buffer_item_type[0]

        if isinstance(stack_item_type, tuple):
            stack_item_type = stack_item_type[0] if root_verb == stack_item else stack_item_type[1]

        dependency = None

        # RIGHT_ARC
        if buffer_item_type in RIGHT_ARC[stack_item_type]:
            dependency = Dependency(RIGHT_ARC[stack_item_type][buffer_item_type], stack_item, buffer_item)
            stack.append(buffer.pop(0))

        # LEFT_ARC
        elif buffer_item_type in LEFT_ARC[stack_item_type]:
            dependency = Dependency(LEFT_ARC[stack_item_type][buffer_item_type], buffer_item, stack_item)
            stack.pop()

        # SHIFT
        elif stack_item_type in [V, ROOT, PP, NAME, N, P]:
            if stack_item_type == PP and buffer_item_type in [YN, PUNC, V]:
                stack.pop()
            elif stack_item_type == NAME and buffer_item_type in [PP, V]:
                stack.pop()
            else:
                stack.append(buffer.pop(0))

        # REDUCE
        else:
            stack.pop()

        if dependency:
            dependencies.append(dependency)

    return dependencies

def malt_parse(sentence: str) -> "list[Dependency]":
    tokens = tokenize(sentence, False)
    return malt_parse_helper(tokens)


