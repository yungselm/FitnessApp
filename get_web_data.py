from bs4 import BeautifulSoup
import requests
import pandas as pd
from omegaconf import DictConfig

def get_muscle_data(config:DictConfig):
    wikiurl = config.get_web_data.muscle_url
    response=requests.get(wikiurl)
    print("Wiki muscle data response:", response.status_code)

    # parse data from the html into a beautifulsoup object
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable=soup.find('table',{'class':"wikitable"})

    df=pd.read_html(str(indiatable))
    # convert list to dataframe
    df=pd.DataFrame(df[0])
    print(df.head(10))

    # save as excel
    df.to_excel('C:/WorkingData/Documents/2_Coding/Python/FitnessApp/data_internal/muscles.xlsx')

exercise_url = 'https://strengthlevel.com/strength-standards'
response = requests.get(exercise_url)
print("Strength level data response:", response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
exercises = soup.find_all('a', {'class': 'button is-fullwidth exerciseitem__button'})

exercise_info = []

for exercise in exercises:
    # Extract exercise name
    name = exercise.find('span', {'class': 'title'}).text.strip()
    
    # Extract exercise URL
    exercise_url = exercise['href']
    
    # Extract exercise picture URL
    picture_url = exercise.find('img')['src']
    
    # Append the extracted information to the exercise_info list as a dictionary
    exercise_info.append({
        'name': name,
        'url': exercise_url,
        'picture_url': picture_url
    })

# Print the extracted information for each exercise
for exercise in exercise_info:
    print("Exercise Name:", exercise['name'])
    print("Exercise URL:", exercise['url'])
    print("Picture URL:", exercise['picture_url'])
    print()
