import weather

while True:
    city = input("Enter city name (or 'exit' to quit): ")
    if city.lower() == "exit":
        break
    result = weather.get_weather(city)
    print(f"Weather in {city}: {result}")