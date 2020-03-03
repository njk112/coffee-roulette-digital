import argparse
import csv
import json
import random
from datetime import date
from operator import itemgetter

##################################################
## Coffee roullete script for Digital@BP account
##################################################
## Author: Naglis J. Kazlauskas
## Copyright: 2020, Coffee-roulette script
## Version: 1.0.0
## Mmaintainer: Naglis J.Kazlauskas
## Email: naglis.kazlauskas@ibm.com
## Status: Testing phase
##################################################

def read_csv_file(path_to_file, new_line = ''):
    csv_file = csv.reader(open(path_to_file, newline=new_line))
    return csv_file

def write_csv_file(file_name, pair, newline = '\n'):
    csv.writer(open(file_name, 'a', newline=newline)).writerows([pair])

def read_json_file(path_to_file):
    json_file = json.load(open(path_to_file, 'r'))
    return json_file

def write_json_file(json_obj = None):
    if json_obj:
        json.dump(json_obj, open('matched_people.json', 'w'))
    else:
        json.dump({}, open('matched_people.json', 'w'))

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
    persons_previous_matches = []
    if matched_people_json:
        try:
            persons_previous_matches = matched_people_json.get(person)
        except:
            pass
        
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

def create_tuple_list(all_people_list, matched_people_json):
    tuple_list = []
    for person in all_people_list:
        tuple_list.append((person, len(matched_people_json.get(person))))
    return tuple_list

def sort_tuple_list(tuple_list):
    sorted_tuple_list = sorted(tuple_list, key=itemgetter(1), reverse=True)
    sorted_people_list = []
    for person in sorted_tuple_list:
        sorted_people_list.append(person[0])
    return sorted_people_list

def main(args):
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
            print('Only use the program generated matched_people.json file')
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

    """
    TODO: 
          1. Scalability?
          2. Code cleaning
    """
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Coffee roulette script, add csv file with member names and run')
    parser.add_argument("path_to_coffee", help="Path to people file.csv")
    parser.add_argument("--matched_json", help="If any people have been matched previously give path to the json")

    args = parser.parse_args()
    main(args)