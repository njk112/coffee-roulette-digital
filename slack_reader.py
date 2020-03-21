import json
from datetime import date
import re

def read_txt(path_to_txt):
    txt_file = open(path_to_txt, "r")
    return txt_file.read()

def convert_to_array(slack_array): 
    return list(iter(slack_array.splitlines()))

def fix_names_list(names_list):
    fixed_list = []                                                                                                                                                                                                                                                                                                    
    for name in names_list:
        fixed_name = re.sub('@', "", name)
        fixed_list.append(fixed_name.strip())
    return fixed_list

def find_questions(slack_sorted_array):
    questions_dict, question_aswers = {}, {}
    expression_emoji = ':[A-Za-z0-9_.-]+:'
    expression_people = '@[A-Za-z0-9_.-]*\s+[A-Za-z0-9_.-]*'

    for row in slack_sorted_array:
        row_position = slack_sorted_array.index(row)
        if re.search(r'\bvotes\b', row):
            specific_question = questions_dict.get(str(row_position-1))
            people_list = re.findall(expression_people, row + " ")
            updated_people_list = fix_names_list(people_list)
            question_aswers['{}'.format(specific_question.strip())] = updated_people_list
        else: 
            question = re.sub(expression_emoji, "", row)
            questions_dict['{}'.format(row_position)] = question

    return question_aswers

slack_string = read_txt('slack.txt')
print(find_questions(convert_to_array(slack_string)))