import tkinter as tk
from tkinter import messagebox
import requests
import threading
# REAL-TIME DATA FUSION & PIPELINE LOGIC
def start_search():
    threading.Thread(
        target=fetch_city_weather,
        daemon=True
    ).start()
def fetch_city_weather():
    btn_search.config(state="disabled", text="LOADING...")
    window.update()
    # 1. READ INPUT: Extracting the user's text from the input bar
    city_name = entry_city.get().strip()
    if not city_name:
        messagebox.showwarning("Input Error", "Please type a city name first!")
        return
    # 2. DATA PIPELINE PHASE 1: Geocoding API Request
    # Converts text strings (e.g., "London") into decimal coordinates (Latitude/Longitude)
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}&count=5&language=en&format=json"
    try:
        geo_response = requests.get(geo_url, timeout=5).json()
        # Data Validation: Check if the API returned an actual physical location
        if "results" not in geo_response or len(geo_response["results"]) == 0:
            messagebox.showerror(
                "City Not Found",
                f"No city found for '{city_name}'. Check spelling."
            )
            return
        # Extract structured location data
        location_data = geo_response["results"][0]
        entered = city_name.lower()
        found = location_data["name"].lower()
        if entered != found:
            lbl_suggestion.config(
                text=f"Showing results for: {location_data['name']}"
            )
        else:
            lbl_suggestion.config(text="")
        suggested_city = location_data["name"]
        lat = location_data["latitude"]
        lon = location_data["longitude"]
        display_location = f"{location_data.get('name')}, {location_data.get('country')}"
        # 3. DATA PIPELINE PHASE 2: Core Weather Data Stream
        # Requests actual temperature, apparent feel, precipitation, wind, and WMO codes
        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&timezone=auto"
        weather_raw = requests.get(weather_url, timeout=5).json()
        current_weather = weather_raw["current"]
        # 4. DATA PIPELINE PHASE 3: Air Quality Index (AQI) Stream
        # Pulls live particle data metrics from a separate specialized environmental API
        aqi_url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}&current=us_aqi&timezone=auto"
        aqi_raw = requests.get(aqi_url, timeout=5).json()
        current_aqi = aqi_raw["current"]
        # 5. DATA TRANSFORMATION & DATA MAPPING
        # Translating standard global World Meteorological Organization (WMO) numerical status codes to clean text descriptions
        wmo_code_map = {
            0: "Clear Sky ☀️",
            1: "Mainly Clear 🌤️",
            2: "Partly Cloudy ⛅",
            3: "Overcast ☁️",
            45: "Foggy 🌫️",
            48: "Freezing Fog 🌫️",
            51: "Light Drizzle 🌧️",
            53: "Moderate Drizzle 🌧️",
            55: "Heavy Drizzle 🌧️",
            61: "Slight Rain 🌧️",
            63: "Moderate Rain 🌧️",
            65: "Heavy Rain 🌧️",
            71: "Slight Snow ❄️",
            75: "Heavy Snow ❄️",
            80: "Light Rain Showers 🌦️",
            81: "Moderate Rain Showers 🌦️",
            82: "Violent Rain Showers ⛈️",
            95: "Thunderstorm ⛈️",        }
        raw_code = current_weather["weather_code"]
        weather_condition = wmo_code_map.get(raw_code, "Variable Conditions")
        # Analytical classification of numeric AQI ratings to ordinal safety bands
        aqi_val = int(current_aqi["us_aqi"])
        if aqi_val <= 50:
            aqi_desc, aqi_color = "Good", "#4CAF50"
        elif aqi_val <= 100:
            aqi_desc, aqi_color = "Moderate", "#FFC107"
        elif aqi_val <= 150:
            aqi_desc, aqi_color = "Unhealthy (Sensitive)", "#FF9800"
        else:
            aqi_desc, aqi_color = "Unhealthy", "#F44336"
        # 6. UI UPDATE LAYER: Pushing parsed data tokens directly onto screen widgets
        lbl_city_title.config(text=display_location.upper())
        lbl_live_temp.config(text=f"{current_weather['temperature_2m']}°C")
        lbl_condition.config(text=weather_condition)
        lbl_val_feels.config(text=f"{current_weather['apparent_temperature']}°C")
        lbl_val_wind.config(text=f"{current_weather['wind_speed_10m']} km/h")
        lbl_val_precip.config(text=f"{current_weather['precipitation']} mm")
        lbl_val_aqi.config(text=f"{aqi_val} - {aqi_desc}", fg=aqi_color)
    except Exception as error:
        messagebox.showerror(
            "Connection Error", f"Unable to fetch data from cloud servers: {error}"        )
    finally:
        btn_search.config(state="normal", text="SEARCH")
# MODERN FLAT USER INTERFACE DESIGN
window = tk.Tk()
window.title("Weather Analytics Dashboard")
window.geometry("450x600")
window.configure(bg="#1E293B")  # Premium deep slate dark background
#INPUT AREA
frame_search = tk.Frame(window, bg="#1E293B")
frame_search.pack(pady=25, fill="x", padx=30)
lbl_suggestion = tk.Label(
    window,
    text="",
    font=("Segoe UI", 10),
    bg="#1E293B",
    fg="#FACC15"
)
lbl_suggestion.pack()
entry_city = tk.Entry(
    frame_search,
    font=("Segoe UI", 14),
    bg="#334155",
    fg="white",
    bd=0,
    insertbackground="white",
    highlightthickness=1,
    highlightbackground="#475569",)
entry_city.insert(0, "Enter City Name...")
entry_city.bind("<FocusIn>", lambda e: entry_city.delete(0, "end"))
entry_city.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
entry_city.bind("<Return>", lambda event: fetch_city_weather())
btn_search = tk.Button(
    frame_search,
    text="SEARCH",
    font=("Segoe UI", 11, "bold"),
    bg="#3B82F6",
    fg="white",
    bd=0,
    activebackground="#2563EB",
    activeforeground="white",
    cursor="hand2",
    command=start_search,)
btn_search.pack(side="right", ipady=7, ipadx=15)
lbl_suggestion = tk.Label(
    window,
    text="",
    font=("Segoe UI", 10),
    bg="#1E293B",
    fg="#FACC15"
)
lbl_suggestion.pack()
#RESULTS HERO TEXT PANEL
lbl_city_title = tk.Label(
    window,
    text="SEARCH A CITY ABOVE",
    font=("Segoe UI", 12, "bold"),
    bg="#1E293B",
    fg="#94A3B8",)
lbl_city_title.pack(pady=(10, 0))
lbl_live_temp = tk.Label(
    window, text="--°C", font=("Segoe UI", 54, "bold"), bg="#1E293B", fg="white")
lbl_live_temp.pack()
lbl_condition = tk.Label(
    window, text="Waiting for input...", font=("Segoe UI", 14), bg="#1E293B", fg="#94A3B8")
lbl_condition.pack(pady=(0, 25))
#GRID OF DISPLAY CARDS
frame_grid = tk.Frame(window, bg="#1E293B")
frame_grid.pack(fill="both", expand=True, padx=30, pady=10)
# Styling configuration maps for data card cells
card_config = {"bg": "#334155", "bd": 0, "highlightthickness": 0}
lbl_title_config = {"font": ("Segoe UI", 10), "bg": "#334155", "fg": "#94A3B8"}
lbl_data_config = {"font": ("Segoe UI", 14, "bold"), "bg": "#334155", "fg": "white"}
# Card 1: Apparent Feel
card_feels = tk.Frame(frame_grid, **card_config)
card_feels.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
tk.Label(card_feels, text="FEELS LIKE", **lbl_title_config).pack(pady=(10, 2))
lbl_val_feels = tk.Label(card_feels, text="--", **lbl_data_config)
lbl_val_feels.pack(pady=(0, 10))
# Card 2: Wind Metrics
card_wind = tk.Frame(frame_grid, **card_config)
card_wind.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
tk.Label(card_wind, text="WIND SPEED", **lbl_title_config).pack(pady=(10, 2))
lbl_val_wind = tk.Label(card_wind, text="--", **lbl_data_config)
lbl_val_wind.pack(pady=(0, 10))
# Card 3: Moisture/Precipitation
card_precip = tk.Frame(frame_grid, **card_config)
card_precip.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
tk.Label(card_precip, text="PRECIPITATION", **lbl_title_config).pack(pady=(10, 2))
lbl_val_precip = tk.Label(card_precip, text="--", **lbl_data_config)
lbl_val_precip.pack(pady=(0, 10))
# Card 4: Air Quality Index (AQI)
card_aqi = tk.Frame(frame_grid, **card_config)
card_aqi.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)
tk.Label(card_aqi, text="AIR QUALITY (AQI)", **lbl_title_config).pack(pady=(10, 2))
lbl_val_aqi = tk.Label(card_aqi, text="--", **lbl_data_config)
lbl_val_aqi.pack(pady=(0, 10))
# Equalize distribution weight sizes inside grid framework layout
frame_grid.columnconfigure(0, weight=1)
frame_grid.columnconfigure(1, weight=1)
frame_grid.rowconfigure(0, weight=1)
frame_grid.rowconfigure(1, weight=1)
window.mainloop()