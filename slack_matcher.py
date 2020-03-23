import argparse
from slack_reader import get_nice_slack_array 
from coffee import *

def preprocess_individual_group(people_list, matched_slack_json):
    try:
        invidual_group_tuple_list = create_tuple_list(people_list, matched_slack_json)
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
            individual_match_list = invidual_preproc(person, all_people_list, matched_slack_json,matched_in_this_function)
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
        sorted_people_list = preprocess_individual_group(people_list, matched_people_json)
        matched_people, unmatched_people = match_individual_group(sorted_people_list, matched_people_json)
        return matched_people, unmatched_people

def make_summary(matched_len, unmatched_len):
    summary = "{0}\n☕️ COFFEE ROULETTE RESULTS ☕️\n{0}\n".format('='*30)
    if matched_len > 0:
        summary += "{} pairs matched\n".format(matched_len)
    if unmatched_len > 0:
        summary += "{} people unmatched\n".format(unmatched_len)
    return summary

def main_slack(args):
    slack_path = args.slack_path
    slack_json = args.slack_json
    slack_dict = get_nice_slack_array(slack_path)
    slack_keys = [*slack_dict]

    matched_in_this_session = []
    matched_outside_group = []
    outside_group = []
    unmatched_in_this_session = []

    if slack_json:
        try:
            matched_people_json = read_json_file(slack_json)
        except:
            raise('Only use the program generated matched_slack_people.json file')
    else:
        write_json_file(None, 'matched_slack_people.json')
        matched_people_json = read_json_file('matched_slack_people.json')

    for key in slack_keys:
        matched_people, unmatched_people = matcher(slack_dict.get(key), matched_people_json)
        matched_in_this_session += matched_people
        outside_group += unmatched_people
    
    if outside_group:
        outside_matches, outside_unmatches = matcher(outside_group, matched_people_json)
        matched_in_this_session += outside_matches
        unmatched_in_this_session += outside_unmatches


    create_today_matched(matched_in_this_session)
    updated_json = update_current_json(matched_people_json, matched_in_this_session)
    write_json_file(updated_json, 'matched_slack_people.json')

    if unmatched_in_this_session:
        print('hello')
        create_today_unmatched(unmatched_in_this_session)

    summary = make_summary(len(matched_in_this_session), len(unmatched_in_this_session))
    print(summary)





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coffee roulette script, add Slack txt file with info from polls')
    parser.add_argument("slack_path", help="Enter slack path to match people only from slack poll message ")
    parser.add_argument("--slack_json", help="Previously matched people from slack poll")

    args = parser.parse_args()
    main_slack(args)