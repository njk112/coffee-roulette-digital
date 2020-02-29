import argparse
import csv
import json
import random
from datetime import date

def read_csv_file(path_to_file, new_line = ''):
    csv_file = csv.reader(open(path_to_file, newline=new_line))
    return csv_file

def write_csv_file(file_name, pair, newline = '\n'):
    csv.writer(open(file_name, 'a', newline=newline)).writerows([pair])

def read_json_file(path_to_file):
    json_file = json.load(open(path_to_file, 'r'))
    return json_file

def write_json_file(json_obj):
    json.dump(json_obj, open('matched_people.json', 'w'))

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

def flat_list(all_people_list):
    flat_pair = [item for sublist in all_people_list for item in sublist]
    return flat_pair


def invidual_preproc(person, all_people_list, matched_people_json, matched_this_session):
    individual_match_list = all_people_list.copy()
    persons_previous_matches = matched_people_json.get(person)
    if persons_previous_matches is None:
        persons_previous_matches = []
    individual_match_list.remove(person)
    for person in matched_this_session:
        try:
            individual_match_list.remove(person)
        except:
            pass
    [individual_match_list.remove(person) for person in persons_previous_matches if person in individual_match_list]
    return individual_match_list
    
def coffee_roulette(person, individual_match_list):
    try:
        random_pick = random.sample(individual_match_list, 1)
        return [person,random_pick[0]]
    except ValueError:
        print('{} has no available matches, please run again'.format(person))
    return None

def grouped_for(iterable, n):
    return zip(*[iter(iterable)]*n)

def create_today_matched(today_matched_list, n=2):
     for x, y in grouped_for(today_matched_list, n):
         pair = [x,y]
         write_csv_file('{0}_matches.csv'.format(date.today()), pair)

def main(args):
    path_to_coffee = args.path_to_coffee
    path_to_matched = args.matched_json
    #config_path = args.config

    all_people_list = flat_list(list(read_csv_file(path_to_coffee)))
    matched_people_json = read_json_file(path_to_matched)
    matched_in_this_session = []
    error = False

    for person in all_people_list:
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

    """
    TODO: 
          1. Add error handling and default config
          2. Scalability?
          3. Sorting list depending on your current match len(),
          for example if you have matched 99% of people -> get priority
          4. Code cleaning
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