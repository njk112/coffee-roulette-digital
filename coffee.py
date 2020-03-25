import argparse
from slack_matcher import main_slack
from csv_reader import main_csv_reader

##################################################
# Coffee roullete script for Digital@BP account
##################################################
# Author: Naglis J. Kazlauskas
# Copyright: 2020, Coffee-roulette script
# Version: 1.1.0
# Maintainer: Naglis J.Kazlauskas
# Email: naglis.kazlauskas@ibm.com
# Status: Testing phase
# Github: https://github.ibm.com/Naglis-Kazlauskas/coffee-roulette
##################################################

def main(args):
    path_to_coffee = args.path_to_coffee_csv
    slack_path = args.slack_path
    path_to_matched = args.matched_json

    argparser = argparse.ArgumentParser()
    if slack_path:
        argparser.add_argument(
                "slack_path", help="Enter slack path to match people only from slack poll message ")
        argparser.add_argument(
                "--slack_json", help="Previously matched people from slack poll")
        if path_to_matched:
            args = argparser.parse_args(
                ["{}".format(slack_path), "--slack_json", "{}".format(path_to_matched)])
            main_slack(args)
        else:
            args = argparser.parse_args([slack_path])
            main_slack(args)

    else:
        argparser.add_argument("path_to_coffee", help="Path to people file.csv")
        argparser.add_argument("--matched_json", help="If any people have been matched previously give path to the json")
        if path_to_matched:
            args = argparser.parse_args(
                ["{}".format(path_to_coffee), "--matched_json", "{}".format(path_to_matched)])
            main_csv_reader(args)
        else:
            args = argparser.parse_args(["{}".format(path_to_coffee)])
            main_csv_reader(args)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Coffee roulette script, add csv file with member names and run')
    parser.add_argument("--path_to_coffee_csv", help="Path to people file.csv")
    parser.add_argument("--slack_path", help="Path to slack txt")
    parser.add_argument(
        "--matched_json", help="If any people have been matched previously give path to the json")

    args = parser.parse_args()
    main(args)  
