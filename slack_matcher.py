import argparse
from slack_reader import get_nice_slack_array
from coffee import *
from datetime import date


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

def main_slack(args):
    slack_path = args.slack_path
    slack_json = args.slack_json
    slack_dict = get_nice_slack_array(slack_path)
    slack_keys = [*slack_dict]

    matched_in_this_session = []
    matched_outside_group = []
    outside_group = []
    unmatched_in_this_session = []
    matched_people_string = ""
    matched_people_txt = ""

    if slack_json:
        try:
            matched_people_json = read_json_file(slack_json)
        except:
            raise('Only use the program generated matched_slack_people.json file')
    else:
        write_json_file(None, 'matched_slack_people.json')
        matched_people_json = read_json_file('matched_slack_people.json')

    for key in slack_keys:
        key_people_list = slack_dict.get(key)
        matched_people_txt += "\n{0}".format(key)
        matched_people_string += '\n\033[33m{0}\033[0m'.format(key)
        if key_people_list:
            matched_people, unmatched_people = matcher(
                key_people_list, matched_people_json)
            matched_people_string = create_matched_people_string(matched_people, matched_people_string)
            matched_in_this_session += matched_people
            matched_people_txt = create_matched_people_string(matched_people, matched_people_txt)
            outside_group += unmatched_people
        else:
           matched_people_string = create_matched_people_string(key_people_list, matched_people_string)
           matched_people_txt = create_matched_people_string(key_people_list, matched_people_txt) 

    if outside_group:
        matched_people_txt += "\nMixed Group"
        matched_people_string += "\n\033[93mMixed Group\033[0m"
        outside_matches, outside_unmatches = matcher(
            outside_group, matched_people_json)
        matched_people_string = create_matched_people_string(outside_matches, matched_people_string)
        matched_in_this_session += outside_matches
        matched_people_txt = create_matched_people_string(outside_matches, matched_people_txt) #fix this sometime later
        unmatched_in_this_session += outside_unmatches

    create_today_matched(matched_in_this_session)
    updated_json = update_current_json(
        matched_people_json, matched_in_this_session)
    write_json_file(updated_json, 'matched_slack_people.json')

    if unmatched_in_this_session:
        create_today_unmatched(unmatched_in_this_session)

    summary, matched_people_txt = make_summary(matched_in_this_session, unmatched_in_this_session, matched_people_string, matched_people_txt)
    write_txt_file(matched_people_txt)
    print(summary)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Coffee roulette script, add Slack txt file with info from polls')
    parser.add_argument(
        "slack_path", help="Enter slack path to match people only from slack poll message ")
    parser.add_argument(
        "--slack_json", help="Previously matched people from slack poll")

    args = parser.parse_args()
    main_slack(args)