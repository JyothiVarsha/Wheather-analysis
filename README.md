# Wheather-analysis
A clean and modern desktop weather application built with Python and Tkinter. This application fetches real-time weather metrics and live Air Quality Index (AQI) data for any city worldwide using free, open-source environmental APIs.
Features:
**Real-Time Data:** Instantly fetches current temperature, "feels like" temperature, wind speed, and precipitation.
**Air Quality Tracking:** Displays the US AQI rating and automatically color-codes it based on health safety levels (Green for Good, Red for Unhealthy).
**Smart UI Threading:** Keeps the application smooth and responsive, showing a `LOADING...` status while fetching data from the cloud.
**No API Keys Required:** Uses the public Open-Meteo API, meaning it works immediately without creating an account.
Installation & Setup:-
Follow these exact steps to get this project running on your computer:
1. Prerequisites:
Make sure you have *Python* installed on your computer. You can download it from [python.org](https://www.python.org/).
2. Download the Project:
Download your code files from this GitHub repository to your computer.
3. Install Required Libraries:
This project uses the `requests` library to talk to the internet. Open your terminal, command prompt, or PowerShell and run this command-
pip install requests
4. Run the App:
​Navigate to the folder where your file is saved and run this command in your terminal:
python miniproject.py

HOW THE CODE WORKS:
​The application is broken down into two main parts: the Data Pipeline and the User Interface (UI).

​1. The Data Pipeline (Fetching Weather)
​When you type a city name and click SEARCH, the code runs a function in the background using threading so the app doesn't freeze. It goes through these steps:
​Geocoding API: It sends the city name to an API to find its exact latitude and longitude coordinates.
​Weather API: Using those coordinates, it requests the current temperature, wind speed, and rain metrics.
​Air Quality API: It makes a separate request to get the live pollution data (AQI).
​Data Mapping: It translates numeric weather codes into clear descriptions with emojis (e.g., Code 0 becomes Clear Sky).

​2. The Modern UI Design
​Built using Python's standard Tkinter library.
​Uses a dark slate background (#1E293B) for a modern, eye-friendly look.
​Organizes data cleanly into a grid of 4 display cards: Feels Like, Wind Speed, Precipitation, and Air Quality.

License:​This project is open-source and available under the MIT License.
