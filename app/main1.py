import openpyxl
import random
import os
import sys

def read_excel_data(file_path, output_file_path):
    data_dict = {}
    wb = openpyxl.load_workbook(file_path)
    ws = wb.active

    with open(output_file_path, 'w') as output_file:
        for row in ws.iter_rows(min_row=1, values_only=True):
            flag = False
            key = row[0]
            values = row[1:]
            processed_values = []
            for value in values:
                if value is not None and "," in value:
                    processed_values.extend(value.split(", "))
                elif value is not None:
                    flag = True
                    processed_values.append(value)
            if flag:
                unique_list = list(set(processed_values))
                output_file.write(f"{key} -> {' | '.join(unique_list)}\n")
            data_dict[key] = processed_values

    return data_dict

def generate_random_sentence(rules, current_rule):
    if current_rule not in rules:
        if current_rule == "None":
            return ""
        return current_rule
    else:
        selected_rule = random.choice(rules[current_rule])
        selected_rule = selected_rule.split(" ")
        sentence = ""
        for part_of_speech in selected_rule:
            sentence += generate_random_sentence(rules, part_of_speech) + " "
        return sentence.strip()
    
def parse_sentence(sentence, rules):
    tokens = sentence.split()
    parse_stack = [tokens]
    tracking = {}

    while len(parse_stack) > 0:
        flag = False
        first_len = len(parse_stack)
        for rule, expressions in rules.items():
            for exp in expressions:
                exp_parts = exp.split()
                for j in range(0, first_len):
                    exp_length = len(exp_parts)
                    if exp_length <= len(parse_stack[j]):
                        for i in range(len(parse_stack[j]) - exp_length + 1):
                            if parse_stack[j][i:i+exp_length] == exp_parts:
                                padding_rule = [rule]
                                temp = parse_stack[j][:i] + padding_rule + parse_stack[j][i+exp_length:]
                                if temp not in parse_stack:
                                    parse_stack.append(temp)
                                    temp_1 = temp
                                    if exp_length > 1:
                                        for k in range(exp_length-1):
                                            padding_rule.append("____")
                                        temp_1 = parse_stack[j][:i] + padding_rule + parse_stack[j][i+exp_length:]
                                    tracking[tuple(temp)] = (tuple(parse_stack[j]), temp_1)
                                flag = True

        if flag == True:
            parse_stack = parse_stack[first_len:]
        else:
            return None

        result = []

        if ['Cau'] in parse_stack:
            index = tuple(['Cau'])
        else:
            continue

        result = []
        while index in tracking:
            result.append(tracking[index][1])
            index = tracking[index][0]
        result.append(index)
        break

    return result

def format_parser(parser):
    output = ""
    for i in range(len(parser)-2, 0, -1):
        indices_of_blank = [i for i, x in enumerate(parser[i]) if x == "____"]
        for index in indices_of_blank:
            parser[i-1].insert(index, "____")
    for tpl in parser:
        output += ''.join([f"{item:{18}}" for item in tpl]) + "\n"
    return output


def part_1(rule_file_path):
    output_file_path = "hcmut/iaslab/nlp/output/grammar.txt"
    try:
        read_excel_data(rule_file_path, output_file_path)
        print("Done! Output in output/grammar.txt!")
    except:
        print("Something wrong!")


def part_2(rule_file_path, number_of_sentences):
    try: 
        output_file_path = "hcmut/iaslab/nlp/output/grammar.txt"
        rules = read_excel_data(rule_file_path, output_file_path)

        output_samples_file_path = "hcmut/iaslab/nlp/output/samples.txt"
        with open(output_samples_file_path, "w", encoding="utf-8") as file:
            for i in range(int(number_of_sentences)):
                generated_sentence = generate_random_sentence(rules, "Cau")
                file.write(generated_sentence + "\n")
        print("Done! Generated " + str(number_of_sentences) + " sentences in output/samples.txt!")
    except:
        print("Something wrong!")


def part_3(rule_file_path):
    try:
        input_file_path = "hcmut/iaslab/nlp/input/sentences.txt"
        output_file_path = "hcmut/iaslab/nlp/output/grammar.txt"
        rules = read_excel_data(rule_file_path, output_file_path)

        output_parse_file_path = "hcmut/iaslab/nlp/output/parse-results.txt"
        count = 0
        with open(output_parse_file_path, "w", encoding="utf-8"):
            pass
        with open(input_file_path, "r", encoding="utf-8") as sentences_file:
            for generated_sentence in sentences_file:
                parsed_rule = parse_sentence(generated_sentence, rules)
                
                with open(output_parse_file_path, "a", encoding="utf-8") as file:
                    if parsed_rule:
                        file.write('----------------------------------------------------------------------\n')
                        file.write("The sentence: " + generated_sentence + "\n")
                        file.write("Parsed rule:\n")
                        file.write(format_parser(parsed_rule))
                        count += 1
                    else:
                        file.write('----------------------------------------------------------------------\n')
                        file.write("The sentence: " + generated_sentence + "\n")
                        file.write("Không thể phân tích câu.\n")
        print("Done! Parse " + str(count) + " sentences completely in output/parse-results.txt!")
    except:
        print("Something wrong!")


if __name__ == "__main__":
    string = "How to run:\n- python main.py 1\n- python main.py 1 data_file_path\n- python main.py 2 number_of_sentences\n- python main.py 2 data_file_path number_of_sentences\n- python main.py 3\n- python main.py 3 data_file_path"
    try:
        if len(sys.argv) >= 2:
            if sys.argv[1] == "1":
                if len(sys.argv) == 3:
                    part_1(sys.argv[2])
                elif len(sys.argv) == 2:
                    part_1("hcmut/iaslab/nlp/data/rule.xlsx")

            elif sys.argv[1] == "2":
                if len(sys.argv) == 4:
                    part_2(sys.argv[2], sys.argv[3])
                elif len(sys.argv) == 3:
                    part_2("hcmut/iaslab/nlp/data/rule.xlsx", sys.argv[2])

            elif sys.argv[1] == "3":
                if len(sys.argv) == 3:
                    part_3(sys.argv[2])
                elif len(sys.argv) == 2:
                    part_3("hcmut/iaslab/nlp/data/rule.xlsx")
            else:
                print(string)
        else:
            print(string)
    except:
        print(string)


