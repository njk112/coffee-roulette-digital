import json
from datetime import date
import re


def read_txt(path_to_txt):
    """Reads txt file

    Arguments:
        path_to_txt {string} -- path to txt

    Returns:
        file.read() -- file in reading format
    """
    txt_file = open(path_to_txt, "r")
    return txt_file.read()


def convert_to_array(slack_array):
    """Converts slack txt file into array

    Arguments:
        slack_array {txt file} -- txt file with all info from slack

    Returns:
        list -- list of rows from slack txt file
    """
    return list(iter(slack_array.splitlines()))


def fix_names_list(names_list):
    """Removes @ before names and whitespace around

    Arguments:
        names_list {list} -- list of names with irrelevant signs from slack file

    Returns:
        list -- list of names with removed signs
    """
    fixed_list = []
    for name in names_list:
        fixed_name = re.sub('@', "", name)
        fixed_list.append(fixed_name.strip())
    return fixed_list


def find_questions(slack_sorted_array):
    """Finds questions and people who answered to those questions in given slack txt file

    Arguments:
        slack_sorted_array {list} -- array made from slack txt file

    Returns:
        dict -- dictionary of question : list of people signed to that question
    """
    questions_dict, question_aswers = {}, {}
    expression_emoji = ':[A-Za-z0-9_.-]+:'  # Finds emojis
    # Finds people names
    expression_people = '@[A-Za-z0-9_.-]*\s+[A-Za-z0-9_.-]*'
    row_position = 0
    for row in slack_sorted_array:
        if re.search(r'\bvotes\b', row) or re.search(r'\bvote\b', row):
            specific_question = questions_dict.get(str(row_position-1))
            people_list = re.findall(expression_people, row + " ")
            updated_people_list = fix_names_list(people_list)
            question_aswers['{}'.format(
                specific_question.strip())] = updated_people_list
        else:
            question = re.sub(expression_emoji, "", row)
            questions_dict['{}'.format(row_position)] = question

        row_position += 1

    return question_aswers


def check_for_duplicates(slack_dict):
    """Checks if any people voted several times

    Arguments:
        slack_dict {dict} -- slack questions : list of people dictionary

    Returns:
        list, dict -- list of all duplicated people, dict of person : list of questions answered
    """
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


"TODO: Fix this beauty sometime later"


def remove_duplicates(duplicate_people, people_dict, slack_dict):
    """Removes people duplicate votes. Acknowledges if after removing person the question has enough people
       to match people evenly.

    Arguments:
        duplicate_people {list} -- list of people who have voted several times
        people_dict {dict} -- dict of people who voted several times : questions they voted for
        slack_dict {dict} -- dict of questions : list of people who voted for them

    Returns:
        [dict] -- dict of question : list of people who voted for it without duplicate people
    """
    for person in duplicate_people:
        person_keys = people_dict.get(person)

        key_lenght_tuple_list = []
        for key in person_keys:
            key_tuple = (key, len(slack_dict.get(key)) - 1)
            key_lenght_tuple_list.append(key_tuple)

        removal_list = []
        for tuple_item in key_lenght_tuple_list:
            if len(key_lenght_tuple_list) - len(removal_list) > 1:
                if tuple_item[1] == 0:
                    removal_list.append(tuple_item[0])
                elif tuple_item[1] % 2 != 0:
                    removal_list.append(tuple_item[0])
                else:
                    removal_list.append(tuple_item[0])
            else:
                break

        not_duplicate_slack_dict = slack_dict.copy()
        for removal_key in removal_list:
            removal_people_list = not_duplicate_slack_dict.get(
                removal_key).remove(person)
            not_duplicate_slack_dict[removal_key] = removal_people_list

    return not_duplicate_slack_dict


def get_nice_slack_array(path_to_slack_file):
    """Takes a slack txt file with text from voting polls and converts it into a dict of question : people who voted

    Arguments:
        path_to_slack_file {string} -- path to slack txt file

    Returns:
        dict -- question : list of people who voted for those questions
    """
    slack_file = read_txt(path_to_slack_file)
    nice_slack_file = find_questions(convert_to_array(slack_file))
    duplicate_people, duplicate_dict = check_for_duplicates(nice_slack_file)
    if duplicate_people:
        removed_dupl_slack_file = remove_duplicates(
            duplicate_people, duplicate_dict, nice_slack_file)
        nice_slack_file = removed_dupl_slack_file

    return nice_slack_file
