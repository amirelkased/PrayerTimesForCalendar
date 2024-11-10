# Prayer Times Calendar Generator

## Overview

This script fetches Islamic prayer times for the specified year (2025) from the Aladhan API and generates an `.ics` calendar file containing prayer times for each day. Each prayer time is stored as a calendar event with associated details like Gregorian and Hijri dates and prayer names in both English and Arabic. The location of each prayer time is also retrieved and added to each event.

## Requirements

The script requires the following libraries:

- `requests`: To make HTTP requests to the Aladhan API to fetch prayer times.
- `ics`: To create and manage calendar events in `.ics` format.
- `pytz`: To manage time zones for the event start and end times.
- `geopy`: To perform reverse geocoding and retrieve the city and country based on latitude and longitude coordinates.
- `datetime`: For working with date and time.

To install these libraries, run:
```bash
pip install requests ics pytz geopy
```

## How It Works
1. Fetch Prayer Times: The script sends a request to the Aladhan API to retrieve prayer times for each day of the specified year (2025) based on the provided latitude, longitude, and calculation method.

2. Initialize Calendar: A new calendar is created to store events.

3. Geolocation Caching: The get_location function caches geolocation results to minimize repetitive requests, enhancing performance.

4. Prayer Event Creation: The script loops through each day and each prayer time. For each prayer, an event is created with:
   
  - Prayer Name: Displayed in English and Arabic.
  - Start and End Times: Each event starts at the scheduled prayer time and lasts for 30 minutes.
  - Gregorian and Hijri Dates: Gregorian and Hijri dates are included in the event description.
  - Location: Based on latitude and longitude coordinates, the city and country are retrieved using geopy.
    
5. Export Calendar: The final calendar is saved as an .ics file, named prayer_times_2025.ics.

## Usage
Run the script to generate the calendar file:
```bash
python script_name.py
```

The generated file, prayer_times_2025.ics, will be saved in the same directory as the script.
This file can be imported into any calendar application that supports .ics files.

## Configuration

`Year`: Change the year variable to fetch prayer times for a different year.

`Location`: Update latitude and longitude to fetch prayer times for a specific location.

`Calculation Method`: Change method to use a different prayer calculation method based on Aladhan API’s supported methods.
