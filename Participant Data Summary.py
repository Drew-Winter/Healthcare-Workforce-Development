
import csv
import datetime
import collections
import pprint

PROGRAM_NAME = "Rural Healthcare Workforce Development"
PROGRAM_START_DATE = datetime.date(2021, 9, 1)
PROGRAM_END_DATE = datetime.date(2024, 12, 31)




def initialize_all_functions(filename, keyfield, separator, quote):
    print("Program: {}\nStart Date: {} \nEnd Date: {}\n".format(
        PROGRAM_NAME, PROGRAM_START_DATE, PROGRAM_END_DATE))
    print(participants_by_organization(filename, keyfield, separator, quote))
    print(participant_gender(filename, keyfield, separator, quote))
    print(participant_race(filename, keyfield, separator, quote))
    print(most_common_professions(filename, keyfield, separator, quote))
    return "End of Report"

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}

    
    with open(filename, "rt", newline='', encoding="utf8") as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=separator, quotechar=quote)
        for row in csvreader:
                table[row[keyfield]] = row
    
    return table


def participants_by_organization(filename, keyfield, separator, quote):
    org_dict = {}
    org_number = 0
    # Read the CSV data into a nested dictionary
    csvfile = read_csv_as_nested_dict(filename, keyfield, separator, quote)
    
    # Iterate through each row in the CSV (which is a dictionary of rows)
    for key, row in csvfile.items():
        # Assuming 'organization' is the field for the organization name or ID
        org = row['MWA_ID']  # Replace 'organization' with the actual field name in your CSV
        if org not in org_dict:
            org_dict[org] = 1
            org_number += 1
        else:
            org_dict[org] += 1
            
    sorted_org_results = sorted(org_dict.items(), key=lambda org_dict: org_dict[1], reverse=True)
    org_number_output = "\nTotal number of organizations: {}".format(org_number)
    
    print("Participants by Organization \n----------------------------")
    
    for key, value in sorted_org_results:
        if value > 1:
            print("MWA {}: {} participants".format(key, value))
        if value <= 1:
            print("MWA {}: {} participant".format(key, value))
    return org_number_output
    

def participant_gender(filename, keyfield, separator, quote):
    
    male_participants = 0
    female_participants = 0
    did_not_say_participants = 0
    
    
    csvfile = read_csv_as_nested_dict(filename, keyfield, separator, quote)

    for values in csvfile.values():
        if values['SEX'] == "WIA_SEX_M":
            male_participants += 1
        elif values['SEX'] == "WIA_SEX_F":
            female_participants += 1
        else:
            did_not_say_participants += 1
            
    gender_output = (
        "\n Participants By Gender: \n ----------------------- \n"
    " Male Participants: {} \n Female Participants: {} \n Did Not Specify: {} \n"
    .format(male_participants, female_participants, did_not_say_participants)
    )
    
    return gender_output
    
def participant_race(filename, keyfield, separator, quote):
    asian = 0
    alaska_native = 0
    black = 0
    pacific_islander = 0
    white = 0
    did_not_say = 0
    
    csvfile = read_csv_as_nested_dict(filename, keyfield, separator, quote)
    
    for values in csvfile.values():
        if values['ASIAN'] == "Y":
            asian += 1
        if values['BLACK'] == "Y":
            black += 1
        if values['ALASKAN_INDIAN'] == "Y":
            alaska_native += 1
        if values['PACIFIC_ISLANDER'] == "Y":
            pacific_islander += 1
        if values['WHITE'] == "Y":
            white += 1
        if values['DID_NOT_SAY'] == "Y":
            did_not_say += 1
    race_output = (" Participants By Race: \n --------------------- \n Asian Participants:"
                   " {} \n Alaska Native Participants: {} \n Black Participants: {} \n "
                   "Pacific Islander Participants: {} \n white participants {} \n Did Not Specify: {}\n"
                   .format(asian, alaska_native, black, pacific_islander, white, did_not_say))
    return race_output

def most_common_professions(filename, keyfield, separator, quote):

    
    professions = collections.Counter()
    with open(filename) as input_file:
        for row in csv.reader(input_file, delimiter=separator):
            professions[row[18]] += 1
    
    profession_counter = 0
    
    top_professions = dict(sorted(professions.items(), key=lambda item: item[1],reverse=True))
    print("Top Professions: \n----------------------------------------------------")
    for key, value in top_professions.items():
        if profession_counter < 10:
            profession_counter += 1
            print("{}. {} ({})".format(profession_counter, key, value))
            
        
    return "\n--------"


print(initialize_all_functions('template participant data.csv', 'ID', ',', '"'))
# print(participants_by_organization('participant data.csv', 'ID', ',', '"'))
# print(participant_gender('participant data.csv','ID',',','"'))
# print(participant_race('participant data.csv','ID',',','"'))