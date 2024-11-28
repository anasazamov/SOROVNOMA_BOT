import csv
import datetime

hour_ = int(datetime.datetime.now().strftime("%H")) + 5
time_ = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")



def write_survey_results_to_csv(survey_question, options, total_counts, values):
    with open(f'{time_} natijalari.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the survey question
        writer.writerow([survey_question])
        
        # Write the options header
        writer.writerow(options)
        
        # Write the total counts
        writer.writerow(total_counts)
        # Write the values
        for value_row in values:
            if value_row is None:
                value_row = ""
            writer.writerow(value_row)
    
    return f'{time_} {survey_question}.csv'


dictionary = {
    "Qestion":{
        "Variant A": [
            "Jami = 123",
            "Anas",
            "Azamov"
        ],
    
        "Variant B": [
            "Jami = 123",
            "Anas",
            "Azamov"
        ],
    
        "Variant C": [
            "Jami = 123",
            "Anas",
            "Azamov"
        ]
    
        }
    }  
