import csv
import datetime
import os

time_ = datetime.datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

def write_survey_results_to_csv(survey_question, options, total_counts, values):
    # Create the filename
    filename = f'{time_}_natijalari.csv'
    
    # Determine the maximum number of voters for any option to set the width of the columns
    max_voters = max(len(v) for v in values)

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the survey question
        writer.writerow([survey_question] + [''] * (len(options) - 1))
        
        # Write the options header
        options_row = [option.option for option in options]
        writer.writerow(options_row)
        
        # Write the total counts
        total_counts_row = total_counts
        writer.writerow(total_counts_row)
        
        # Write the voters, padding with empty strings as necessary
        for i in range(max_voters):
            row = []
            for voters in values:
                row.append(voters[i] if i < len(voters) else '')
            writer.writerow(row)
    
    return filename
