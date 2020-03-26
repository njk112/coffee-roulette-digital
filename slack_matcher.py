import argparse
from slack_reader import get_nice_slack_array
from util import (read_json_file, write_json_file, matcher, create_matched_people_string,
                  create_today_matched, update_current_json, create_today_unmatched, make_summary, write_txt_file)
from datetime import date


def main_slack(args):
    slack_path = args.slack_path
    if args.slack_json:
        slack_json = args.slack_json
    else:
        slack_json = None
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
        write_json_file(None, 'matched_people.json')
        matched_people_json = read_json_file('matched_people.json')

    for key in slack_keys:
        key_people_list = slack_dict.get(key)
        matched_people_txt += "\n{0}".format(key)
        matched_people_string += '\n\033[33m{0}\033[0m'.format(key)
        if key_people_list:
            matched_people, unmatched_people = matcher(
                key_people_list, matched_people_json)
            matched_people_string = create_matched_people_string(
                matched_people, matched_people_string)
            matched_in_this_session += matched_people
            matched_people_txt = create_matched_people_string(
                matched_people, matched_people_txt)
            outside_group += unmatched_people
        else:
            matched_people_string = create_matched_people_string(
                key_people_list, matched_people_string)
            matched_people_txt = create_matched_people_string(
                key_people_list, matched_people_txt)

    if outside_group:
        matched_people_txt += "\nMixed Group"
        matched_people_string += "\n\033[93mMixed Group\033[0m"
        outside_matches, outside_unmatches = matcher(
            outside_group, matched_people_json)
        matched_people_string = create_matched_people_string(
            outside_matches, matched_people_string)
        matched_in_this_session += outside_matches
        matched_people_txt = create_matched_people_string(
            outside_matches, matched_people_txt)  # fix this sometime later
        unmatched_in_this_session += outside_unmatches

    create_today_matched(matched_in_this_session)
    updated_json = update_current_json(
        matched_people_json, matched_in_this_session)
    if slack_json:
        write_json_file(updated_json, slack_json)
    else:
        write_json_file(updated_json, 'matched_people.json')

    if unmatched_in_this_session:
        create_today_unmatched(unmatched_in_this_session)

    summary, matched_people_txt = make_summary(
        matched_in_this_session, unmatched_in_this_session, matched_people_string, matched_people_txt)
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
