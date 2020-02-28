import argparse
import csv
import json
import random

def read_csv_file(path_to_file, new_line = ''):
    csv_file = csv.reader(open(path_to_file, newline=new_line))
    return csv_file

def read_json_file(path_to_file):
    json_file = json.load(open(path_to_file, 'r'))
    return json_file

def flat_list(all_people_list):
    flat_pair = [item for sublist in all_people_list for item in sublist]
    return flat_pair

def add_people_to_matched(matched_pair, matched_people_list):
    matched_people_list.append(matched_pair)
    return matched_people_list

def invidual_preproc(person, all_people_list, matched_people_json):
    individual_match_list = all_people_list.copy()
    persons_previous_matches = matched_people_json.get(person)
    individual_match_list.remove(person)
    [individual_match_list.remove(person) for person in persons_previous_matches if person in individual_match_list]
    return individual_match_list
    
def coffee_roulette(person, individual_match_list):
    random_pick = random.sample(individual_match_list, 1)
    return [[person],[random_pick]]

def add_matched_to_json(matched_pair, matched_people_json):
    matched_people_json[matched_pair[0]] = [matched_people_json.get(matched_pair[0])] + matched_pair[1]
    matched_people_json[matched_pair[1]] = [matched_people_json.get(matched_pair[1])] + matched_pair[0]
    return matched_people_jsonfor 


def main(args):
    path_to_coffee = args.path_to_coffee
    path_to_matched = args.matched_json
    #config_path = args.config

    all_people_list = flat_list(list(read_csv_file(path_to_coffee)))
    matched_people_json = read_json_file(path_to_matched)

    individual_match_list = invidual_preproc('Naglis Kazlauskas', all_people_list, matched_people_json)
    matched_pair = coffee_roulette('Naglis Kazlauskas', individual_match_list)
    print(matched_pair)
    

    """
    TODO: 1. If a is matched with b, don't run with b
          2. Save to json, create todays_matches file
          3. Add error handling and default config
          4. Scalability?
    """

    #if config_path:
    #    param = load_config(config_path)
    #else:
    #    param = default_config()

    #save(output, save_dir, param)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("path_to_coffee", help="Path to people file.csv")
    parser.add_argument("--matched_json", help="If any people have been matched previously give path to the file")
    #parser.add_argument("--path_to_matched", help="If any people have been matched previously give path to the file")

    args = parser.parse_args()
    main(args)