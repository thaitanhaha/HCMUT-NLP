from models.maltparser import *
from models.grammar_relation import relationalize
from models.logical_form import logicalize
from models.semantic_procedure import proceduralize
from models.answer import answer
# from .models.maltparser import malt_parse
# from .models.grammar_relation import relationalize
# from .models.logical_form import logicalize
# from .models.semantic_procedure import proceduralize
# from .models.answer import answer

def get_questions(path):
    questions = []
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            line = line.replace("\n", "")
            questions.append(line)
    return questions

def write_to_file(string, path):
    with open(path, "a", encoding="utf-8") as file:
        file.write(string)

def main():
    queries = get_questions("hcmut/iaslab/nlp/input/questions.txt")

    for i in range(1,6):
        file_path = f"hcmut/iaslab/nlp/output/p2-q-{i}.txt"
        with open(file_path, "w", encoding="utf-8"):
            pass

    output1 = "Đầu tiên ta định nghĩa RIGHT_ARC và LEFT_ARC như sau:\n\n"
    output1 += "RIGHT_ARC: \nCó dạng A R B, nghĩa là, từ bên trái là A, từ bên phải là B, mối quan hệ RIGHT_ARC của chúng là R\n"
    for i in RIGHT_ARC:
        if len(RIGHT_ARC[i]) > 0:
            for j in RIGHT_ARC[i]:
                output1 += ''.join([f"{i:{18}}", f"{RIGHT_ARC[i][j]:{18}}", f"{j:{18}}"]) + "\n"
    output1 += "\n\nLEFT_ARC: \nCó dạng A R B, nghĩa là, từ bên trái là A, từ bên phải là B, mối quan hệ LEFT_ARC của chúng là R\n"
    for i in LEFT_ARC:
        if len(LEFT_ARC[i]) > 0:
            for j in LEFT_ARC[i]:
                output1 += ''.join([f"{i:{18}}", f"{LEFT_ARC[i][j]:{18}}", f"{j:{18}}"]) + "\n"
    output1 += "\nSau khi đã định nghĩa, sử dụng giải thuật MaltParser như đã học để phân tích câu."
    write_to_file(output1, f"hcmut/iaslab/nlp/output/p2-q-1.txt")

    for query in queries:
        output = "Câu hỏi: " + query + "\n"

        context_deps = malt_parse(query)
        output2 = ""
        for x in context_deps:
            output2 += str(x) + "\n"
        output2 += "\n\n"
        write_to_file(output + output2, f"hcmut/iaslab/nlp/output/p2-q-2.txt")

        output3 = ""
        relations = relationalize(context_deps)
        for x in relations:
            output3 += str(x) + "\n"
        output3 += "\n\n"
        write_to_file(output + output3, f"hcmut/iaslab/nlp/output/p2-q-3.txt")

        sem = logicalize(relations)
        output4 = str(sem) + "\n"
        procedure = proceduralize(sem)
        output4 += str(procedure) + "\n\n\n"
        write_to_file(output + output4, f"hcmut/iaslab/nlp/output/p2-q-4.txt")

        output5 = "Trả lời: " + answer(procedure) + "\n\n\n"
        write_to_file(output + output5, f"hcmut/iaslab/nlp/output/p2-q-5.txt")


if __name__ == "__main__":
    main()