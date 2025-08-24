# weather_gui_modern.py
import tkinter as tk
from tkinter import messagebox
import requests
import ttkbootstrap as tb

# API endpoints
TEXT_URL = "https://wttr.in/{city}?format=%C+%t"
JSON_URL = "https://wttr.in/{city}?format=j1"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

# Fetch JSON Weather
def fetch_weather(city: str) -> dict:
    try:
        r = requests.get(JSON_URL.format(city=city), headers=HEADERS, timeout=10)
        if r.ok:
            return r.json()
        else:
            return None
    except:
        return None

def on_get_weather(event=None):
    city = city_entry.get().strip()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city name")
        return
    status_var.set("Fetching...")
    root.after(100, update_weather, city)

def update_weather(city: str):
    data = fetch_weather(city)
    if not data:
        weather_main.config(text="❌ Failed to fetch weather.")
        status_var.set("Failed.")
        return

    # Extract values
    area = data.get("nearest_area", [{}])[0].get("areaName", [{}])[0].get("value", city)
    region = data.get("nearest_area", [{}])[0].get("region", [{}])[0].get("value", "")
    country = data.get("nearest_area", [{}])[0].get("country", [{}])[0].get("value", "")

    current = (data.get("current_condition") or [{}])[0]
    cond = (current.get("weatherDesc") or [{}])[0].get("value", "N/A")
    tempC = current.get("temp_C", "N/A")
    feels = current.get("FeelsLikeC", "N/A")
    hum = current.get("humidity", "N/A")
    wind = current.get("windspeedKmph", "N/A")
    vis = current.get("visibility", "N/A")

    # Choose emoji/icon
    emoji = "🌞"
    if "rain" in cond.lower(): emoji = "🌧️"
    elif "cloud" in cond.lower(): emoji = "☁️"
    elif "snow" in cond.lower(): emoji = "❄️"

    # Update GUI
    weather_main.config(
        text=f"{emoji} {cond}\n🌡️ {tempC}°C (Feels {feels}°C)"
    )
    weather_extra.config(
        text=f"🌍 {area}, {region}, {country}\n💧 Humidity: {hum}%   💨 Wind: {wind} km/h   👀 Visibility: {vis} km"
    )
    status_var.set("Updated ✔")

# ---------------- GUI Setup ----------------
root = tb.Window(themename="superhero")  # themes: flatly, cyborg, superhero, solar
root.title("🌦️ Weather App")
root.geometry("660x420")
root.resizable(False, False)

# Title
title = tb.Label(root, text="Weather App", font=("Segoe UI", 22, "bold"))
title.pack(pady=10)

# Input
input_frame = tb.Frame(root)
input_frame.pack(pady=5)

city_entry = tb.Entry(input_frame, font=("Segoe UI", 14), width=28)
city_entry.grid(row=0, column=0, padx=8)
city_entry.focus_set()

get_btn = tb.Button(input_frame, text="Get Weather", bootstyle="primary", command=on_get_weather)
get_btn.grid(row=0, column=1, padx=5)

# Weather display
weather_main = tb.Label(root, text="Enter a city and click Get Weather 🌍", font=("Segoe UI", 14), justify="center")
weather_main.pack(pady=15)

weather_extra = tb.Label(root, text="", font=("Segoe UI", 11), justify="center")
weather_extra.pack(pady=5)

# Status bar
status_var = tk.StringVar(value="Ready.")
status_bar = tb.Label(root, textvariable=status_var, anchor="w", bootstyle="inverse-dark")
status_bar.pack(fill="x", side="bottom")

root.bind("<Return>", on_get_weather)

root.mainloop()
