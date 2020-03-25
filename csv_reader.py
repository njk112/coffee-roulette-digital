from util import *
import argparse
def main_csv_reader(args):
    path_to_coffee = args.path_to_coffee
    path_to_matched = args.matched_json
    all_people_list = flat_list(list(read_csv_file(path_to_coffee)))
    matched_in_this_session = []
    error = False

    if path_to_matched:
        try:
            matched_people_json = read_json_file(path_to_matched)
            tuple_list = create_tuple_list(all_people_list,matched_people_json)
            sorted_people_list = sort_tuple_list(tuple_list)
        except:
            raise('Only use the program generated matched_people.json file')
    else:
        write_json_file()
        matched_people_json = read_json_file('matched_people.json')
        sorted_people_list = all_people_list

    for person in sorted_people_list:
        if person not in matched_in_this_session:
            individual_match_list = invidual_preproc(person, all_people_list, matched_people_json,matched_in_this_session)
            matched_pair = coffee_roulette(person, individual_match_list)
            if matched_pair is not None:
                for person in matched_pair:
                    matched_in_this_session.append(person)
            else:
                error = True
                break
        else:
            pass

    if error is False:
        create_today_matched(matched_in_this_session)
        updated_json = update_current_json(matched_people_json, matched_in_this_session)
        write_json_file(updated_json)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coffee roulette script, add csv file with member names and run')
    parser.add_argument("path_to_coffee", help="Path to people file.csv")
    parser.add_argument("--matched_json", help="If any people have been matched previously give path to the json")
