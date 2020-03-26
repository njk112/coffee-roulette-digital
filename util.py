import csv
import json
import random
from datetime import date
from operator import itemgetter

"TODO: Comment code"
"TODO: Refactor"

def read_csv_file(path_to_file, new_line = ''):
    csv_file = csv.reader(open(path_to_file, newline=new_line))
    return csv_file

def write_csv_file(file_name, pair, unmatched = False, newline = '\n'):
    if unmatched is False:
        csv.writer(open(file_name, 'a', newline=newline)).writerows([pair])
    if unmatched:
        csv.writer(open(file_name, 'a', newline=newline)).writerow([pair])

def read_json_file(path_to_file):
    json_file = json.load(open(path_to_file, 'r'))
    return json_file

def write_json_file(json_obj = None, file_name = 'matched_people.json'):
    if json_obj:
        json.dump(json_obj, open(file_name, 'w'))
    else:
        json.dump({}, open(file_name, 'w'))

def update_current_json(current_json, todays_matches, n=2):
    for x, y in grouped_for(todays_matches, n):
        try:
            current_json[x] = current_json.get(x) + [y]
        except:
            current_json[x] =  [y]
        try:
            current_json[y] = current_json.get(y) + [x]
        except:
            current_json[y] =  [x]
    return current_json

def coffee_roulette(person, individual_match_list):
    try:
        random_pick = random.sample(individual_match_list, 1)
        return [person,random_pick[0]]
    except ValueError:
        raise('{} has no available matches, please run again'.format(person))
    return None

def grouped_for(iterable, n):
    return zip(*[iter(iterable)]*n)

def create_today_matched(today_matched_list, n=2):
     for x, y in grouped_for(today_matched_list, n):
         pair = [x,y]
         write_csv_file('{0}_matches.csv'.format(date.today()), pair)

def create_today_unmatched(unmatched_people_list):
    for person in unmatched_people_list:
        write_csv_file('{0}_unmatches.csv'.format(date.today()), person, True)

def create_tuple_list(all_people_list, matched_people_json):
    tuple_list = []
    for person in all_people_list:
        person_from_json = matched_people_json.get(person)
        if person_from_json:
            tuple_list.append((person, len(person_from_json)))
        else:
            tuple_list.append((person, 0))
    return tuple_list

def sort_tuple_list(tuple_list):
    sorted_tuple_list = sorted(tuple_list, key=itemgetter(1), reverse=True)
    sorted_people_list = []
    for person in sorted_tuple_list:
        sorted_people_list.append(person[0])
    return sorted_people_list

def flat_list(all_people_list):
    flat_pair = [item for sublist in all_people_list for item in sublist]
    return flat_pair

def invidual_preproc(person, all_people_list, matched_people_json, matched_this_session):
    individual_match_list = all_people_list.copy()
    persons_previous_matches = []
    if matched_people_json:
        try:
            persons_previous_matches = matched_people_json.get(person)
        except:
            pass
    individual_match_list.remove(person)

    if individual_match_list:
        for person in matched_this_session:
            try:
                individual_match_list.remove(person)
            except:
                pass
        try:
            [individual_match_list.remove(person) for person in persons_previous_matches if person in individual_match_list]
        except:
            pass
    return individual_match_list


###Slack files

def preprocess_individual_group(people_list, matched_slack_json):
    try:
        invidual_group_tuple_list = create_tuple_list(
            people_list, matched_slack_json)
        sorted_people_list = sort_tuple_list(invidual_group_tuple_list)
    except:
        sorted_people_list = people_list.copy()

    return sorted_people_list


def match_individual_group(sorted_people_list, matched_slack_json):
    all_people_list = sorted_people_list.copy()
    matched_in_this_function = []
    unmatched_in_this_function = []
    for person in sorted_people_list:
        if person not in matched_in_this_function:
            individual_match_list = invidual_preproc(
                person, all_people_list, matched_slack_json, matched_in_this_function)
            try:
                matched_pair = coffee_roulette(person, individual_match_list)
            except:
                matched_pair = None

            if matched_pair is not None:
                for person in matched_pair:
                    matched_in_this_function.append(person)
            else:
                unmatched_in_this_function.append(person)
        else:
            pass

    return matched_in_this_function, unmatched_in_this_function


def matcher(people_list, matched_people_json):
    sorted_people_list = preprocess_individual_group(
        people_list, matched_people_json)
    matched_people, unmatched_people = match_individual_group(
        sorted_people_list, matched_people_json)
    return matched_people, unmatched_people


def make_summary(matched_in_this_session, unmatched_in_this_session, matched_people_string, slack_txt):
    matched, unmatched, matched_people, unmatched_people = "", "", "", ""
    if len(matched_in_this_session) > 0:
        matched = "\n{} pairs \033[92mmatched\033[0m".format(int(len(matched_in_this_session) /2))
        matched_people += '\n{0}\n\033[93mPAIRS\033[0m\n{0}'.format('='*30)
        matched_people += matched_people_string
    if len(unmatched_in_this_session) > 0:
        unmatched = "\n{} people \033[91munmatched\033[0m".format(
            len(unmatched_in_this_session))
        unmatched_in_this_session
        unmatched_people += '\n{0}\n\033[93mALONE\033[0m\n{0}'.format('='*30)
        slack_txt += '\n{0}\nALONE\n{0}'.format('='*30)
        for person in unmatched_in_this_session:
            unmatched_people += "\n{}".format(person)
            slack_txt += "\n@{}".format(person)

    summary = "{0}\n☕️ \033[93mCOFFEE ROULETTE RESULTS\033[0m ☕️\n{0}{1}{2}{3}{4}".format(
        '='*30, matched, unmatched, matched_people, unmatched_people)

    return summary, slack_txt

def create_matched_people_string(people_list, current_string):
    current_string += "\n{0}".format("-"*10)
    if people_list:
        for x, y in grouped_for(people_list, 2):
            current_string += '\n@{0} + @{1}'.format(x, y)
    else:
        current_string += '\nNone'
    current_string += "\n{0}".format("-"*10)
    return current_string

def write_txt_file(summary):
    file = open("{0}_paste_me_to_slack.txt".format(date.today()),"w")
    file.write(summary)
    file.close() 