## Version 1.1
### Summary
Now you can use coffee script with information from slack polls and match people based on their answers.
Script commands have changed.
More files outputed after the script finished running.

![Terminal V1.1](coffee1.gif)

### FAQ
1. Do I still need fill in people_list.csv if I am using information from the Slack polls?
> No you do not. The only thing you have to do is to copy and paste information form the slack
> poll into the Slack.txt and script will automatically detect people and match them accordingly.
2. If I am using the original coffee script without slack polls what do I need to know?
> Now there will be <b>3 files outputed</b>: 2 csv files for todays matches and unmatches and 1 txt file
> which contains ready to copy paste information directly into slack. However, if on Slack people have
> different names/tags than the ones in your people_list.csv file then you need to review matches pairs
> to see if output tags are the equal between slack.txt and actual slack channel.
3. How did the original script running command changed?
> Now to run the original script you would enter:<br/>
```python3 coffee.py --path_to_coffee_csv people_list.csv```<br/>
> or if you are using historical match data<br/>
```python3 coffee.py --path_to_coffee_csv people_list.csv --matched_json matched_people.json```
4. How do I run the Slack script?
> Firsly you have to copy paste information from slack poll to slack.txt and then run the following commands<br/>
```python3 coffee.py --slack_path slack.txt```<br/>
>or if yu are using historical data<br/>
```python3 coffee.py --slack_path slack.txt --matched_json matched_people.json```

### Changes:
* Added Slack Polls "integration". Now you can copy slack poll information into slack.txt in the following
format : 
```
Which Harry Potter house do you think you belong in?
:slytherin: Slytherin:  Ambition, Leadership, Cunning
1 vote:  @Albus Severus Potter @Lord Voldemort
:hufflepuff: Hufflepuff: Hardwork, Patience, Loyalty
2 votes:  @Helga.Hufflepuff @Pomona Sprout 
:gryffindor-pride: Gryffindor: Courage, Bravery, Nerve
2 votes:  @Harry_potter @Nigel Wolpert 
:ravenclaw: Ravenclaw: Intelligence, Creativity, Learning
2 votes:  @Luna Lovegood @Pupulis
:harry_potter: I've never seen or read Harry Potter
1 vote:  @Kukulis 
```

it will produce the following output:
```
==============================
☕️ COFFEE ROULETTE RESULTS ☕️
==============================
4 pairs matched
1 people unmatched
==============================
PAIRS
==============================
Slytherin:  Ambition, Leadership, Cunning
----------
@Albus Severus + @Lord Voldemort
----------
Hufflepuff: Hardwork, Patience, Loyalty
----------
@Helga.Hufflepuff + @Pomona Sprout
----------
Gryffindor: Courage, Bravery, Nerve
----------
@Harry_potter + @Nigel Wolpert
----------
Ravenclaw: Intelligence, Creativity, Learning
----------
@Luna Lovegood + @Pupulis1
----------
I've never seen or read Harry Potter
----------
None
----------
Mixed Group
----------
None
----------
==============================
ALONE
==============================
Kukulis
```

All people are matched depending on how they answered a specific question. Slytherin would be matched with slytherin etc. If there are no available pairs in the specific group, people would be matched in Mixed Group. All people who did not get a match would be in ALONE section.

* Instead of today_matches.csv now script generates 3 files:
> today_matches.csv with all the match pairs
> today_paste_me_to_slack.txt file containing all relevant information to copy paste to slack, with @signs.
> today_unmatches.csv all people who did not get matched.

* Coffee.py running commands have changed:
* Coffee.py original script now shows the output in terminal.

Everyone who is using script with their own csv file with people names:<br/>
<b> CSV file commands </b><br/>
>```python3 coffee.py --path_to_coffee_csv people_list.csv``` <br/>
>```python3 coffee.py --path_to_coffee_csv people_list.csv --matched_json matched_people.json```

Who wants to use information from slack polls:<br/>
<b>Slack txt file commands</b><br/>
```python3 coffee.py --slack_path slack.txt```<br/>
```python3 coffee.py --slack_path slack.txt --matched_json matched_people.json```

* Bug Fixes
