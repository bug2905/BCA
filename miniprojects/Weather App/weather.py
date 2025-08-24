import requests

def get_weather(city):
    api_key = "https://wttr.in"  # Free weather service
    url = f"{api_key}/{city}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return "Error fetching data"
