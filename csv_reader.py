from util import (flat_list, read_csv_file, read_json_file, create_tuple_list, sort_tuple_list, write_json_file,
                  invidual_preproc, coffee_roulette, create_today_matched, create_today_unmatched, update_current_json,
                  create_matched_people_string, make_summary, write_txt_file)

import argparse
from datetime import date

def main_csv_reader(args):
    path_to_coffee = args.path_to_coffee
    path_to_matched = args.matched_json
    all_people_list = flat_list(list(read_csv_file(path_to_coffee)))
    matched_in_this_session = []
    error = False

    if path_to_matched:
        try:
            matched_people_json = read_json_file(path_to_matched)
            tuple_list = create_tuple_list(
                all_people_list, matched_people_json)
            sorted_people_list = sort_tuple_list(tuple_list)
        except:
            raise('Only use the program generated matched_people.json file')
    else:
        write_json_file()
        matched_people_json = read_json_file('matched_people.json')
        sorted_people_list = all_people_list

    unmatched_people = []

    for person in sorted_people_list:
        if person not in matched_in_this_session:
            individual_match_list = invidual_preproc(
                person, all_people_list, matched_people_json, matched_in_this_session)
            if individual_match_list:
                matched_pair = coffee_roulette(person, individual_match_list)
                if matched_pair is not None:
                    for person in matched_pair:
                        matched_in_this_session.append(person)
                else:
                    error = True
                    break
            else:
                unmatched_people.append(person)
        else:
            pass

    if error is False:
        create_today_matched(matched_in_this_session)
        if unmatched_people:
            create_today_unmatched(unmatched_people)

        updated_json = update_current_json(
            matched_people_json, matched_in_this_session)
        summary = "\n{} Matches".format(date.today())
        summary = create_matched_people_string(
            matched_in_this_session, summary)
        summary_messsage, alone = make_summary(
            matched_in_this_session, unmatched_people, summary, "")
        summary += alone
        write_json_file(updated_json)
        write_txt_file(summary)
        print(summary_messsage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Coffee roulette script, add csv file with member names and run')
    parser.add_argument("path_to_coffee", help="Path to people file.csv")
    parser.add_argument(
        "--matched_json", help="If any people have been matched previously give path to the json")
