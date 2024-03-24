from bs4 import BeautifulSoup
import requests
import pandas as pd
from omegaconf import DictConfig
import json
import re

# URL of the calculator
url = 'https://strengthlevel.com/'

# Data to be submitted
data = {
    "gender": "male",
    "ageyears": 30,
    "bodymass": 85,
    "bodymassunit": "kg",
    "exercise": "bench-press",  # You can change this to squat or deadlift as needed
    "liftmass": 90,  # Your lift mass (e.g., one-rep max)
    "liftmassunit": "kg",
    "repetitions": 10,  # Number of repetitions
    "timezone": 1,
    "source": "homepage"
}

# Send a POST request with the form data
response = requests.post(url, data=data)

# Check if the request was successful
if response.status_code == 200:
    print("Request successful!")
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.title
    print("Title of the webpage:", title.text)

    paragraphs = soup.find_all('p')
    # for p in paragraphs:
    #     print("Paragraph:", p.text)
    
    one_rep_max = None
    stronger_than = 0
    stronger_than_weight_adjusted = None
    max_lift_times_bodyweight = None

    for p in paragraphs:
        # if any(char.isdigit() for char in p.text):
        #     print("Paragraph with number:", p.text)
        if "We estimate that your one-rep max is" in p.text:
            temp = re.findall("\d+", p.text)[0]
            one_rep_max = int(temp)
        if "lifters your age weighing" in p.text:
            temp = re.findall("\d+", p.text)[0]
            stronger_than_weight_adjusted = int(temp)
        if "Result: stronger than" in p.text:
            temp = re.findall("\d+", p.text)[0]
            if int(temp) > stronger_than:
                stronger_than = int(temp)
        if "times your bodyweight" in p.text:
            temp = re.findall("\d+\.\d+", p.text)[0]  # Extract float number
            max_lift_times_bodyweight = float(temp)
else:
    print("Failed to submit the form. Status code:", response.status_code)

# Print the results
print("One-rep max:", one_rep_max)
print("Stronger than weight adjusted:", stronger_than_weight_adjusted)
print("Stronger than:", stronger_than)
print("Max lift times bodyweight:", max_lift_times_bodyweight)
