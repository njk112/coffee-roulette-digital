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
    row_position = 0
    for row in slack_sorted_array:
        if re.search(r'\bvotes\b', row):
            specific_question = questions_dict.get(str(row_position-1))
            people_list = re.findall(expression_people, row + " ")
            updated_people_list = fix_names_list(people_list)
            question_aswers['{}'.format(specific_question.strip())] = updated_people_list
        else: 
            question = re.sub(expression_emoji, "", row)
            questions_dict['{}'.format(row_position)] = question

        row_position +=1 

    return question_aswers

def check_for_duplicates(slack_dict):
    slack_keys = [*slack_dict]
    duplicate_people = []
    duplicate_dict = {}
    for key in slack_keys:
        group_people = slack_dict.get(key)
        for person in group_people:
            if duplicate_dict.get(person) is not None:
                current_groups = duplicate_dict.get(person)
                duplicate_people.append(person)
                duplicate_dict["{}".format(person)] = current_groups + [key]
            else:
                duplicate_dict["{}".format(person)] = [key]

    return duplicate_people, duplicate_dict

def remove_duplicates(duplicate_people, people_dict, slack_dict):
    for person in duplicate_people:
        person_keys = people_dict.get(person)
        len_dict = {}
        remove_from_us = []
        for key in person_keys:
            len_dict[key] = len(slack_dict.get(key)) - 1
                
        print(len_dict)

def get_nice_slack_array(path_to_slack_file):
    slack_file = read_txt(path_to_slack_file)
    nice_slack_file = find_questions(convert_to_array(slack_file))
    duplicate_people, duplicate_dict = check_for_duplicates(nice_slack_file)
    remove_duplicates(duplicate_people, duplicate_dict, nice_slack_file)


    return nice_slack_file

get_nice_slack_array('slack.txt')