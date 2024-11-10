import requests
from ics import Calendar, Event
from datetime import datetime, timedelta
import pytz
from geopy.geocoders import Nominatim

# Constants
year = 2025
latitude = 30.0444196
longitude = 31.2357116
method = 5
URL = f"http://api.aladhan.com/v1/calendar/{year}?latitude={latitude}&longitude={longitude}&method={method}"

# Fetch prayer times data for 2025
response = requests.get(URL)
data = response.json()['data']

# Initialize a new calendar
calendar = Calendar()

# Cache variable to store the last requested location
onetime_location_request = {}

def get_location(latitude, longitude):
    # Convert the latitude and longitude into a tuple to use as a key
    location_key = (latitude, longitude)

    # Check if the location is already cached
    if location_key in onetime_location_request:
        # If cached, return the cached result
        return onetime_location_request[location_key]

    # If not cached, perform the geolocation request
    geolocator = Nominatim(user_agent="MyUniqueGeocodingApp_2025")
    try:
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        if location:
            address = location.raw['address']
            city = address.get('city', '') or address.get('town', '') or address.get('village', '')
            country = address.get('country', '')
            result = (city, country)
        else:
            result = (None, None)
    except Exception as e:
        print(f"Error occurred while geocoding: {e}")
        result = (None, None)

    # Cache the result for future use
    onetime_location_request[location_key] = result

    return result


# Prayer titles in English and Arabic
prayer_names = {
    "Fajr": ("Fajr", "الفجر"),
    "Dhuhr": ("Dhuhr", "الظهر"),
    "Asr": ("Asr", "العصر"),
    "Maghrib": ("Maghrib", "المغرب"),
    "Isha": ("Isha", "العشاء"),
    "Lastthird":("Lastthird", "الثلث الأخير")
}

# Loop through each month in the data
for month_data in data.values():
    # Loop through each day in the month
    for day_data in month_data:
        # Extract Gregorian and Hijri dates
        gregorian_date = day_data['date']['gregorian']['date']
        hijri_date = day_data['date']['hijri']['date']
        gregorian_readable = day_data['date']['readable']
        hijri_readable = f"{day_data['date']['hijri']['day']} {day_data['date']['hijri']['month']['en']} {day_data['date']['hijri']['year']} AH"
        hijri_readable_ar = f"{day_data['date']['hijri']['day']} {day_data['date']['hijri']['month']['ar']} {day_data['date']['hijri']['year']} AH"

        # Loop through each prayer time
        for prayer, timing in day_data['timings'].items():
            # Only create events for the main prayers
            if prayer in prayer_names:
                # Parse the prayer time
                time_str = timing.split(" ")[0]  # remove timezone part
                event_start = datetime.strptime(f"{gregorian_date} {time_str}", "%d-%m-%Y %H:%M")
                
                city_tz = pytz.timezone(day_data['meta']['timezone'])
                event_start = city_tz.localize(event_start)

                # Define a 30-minute duration for each prayer
                event_end = event_start + timedelta(minutes=30)

                # Create the event
                event = Event()
                event.name = f"{prayer_names[prayer][0]} | {prayer_names[prayer][1]}"
                event.begin = event_start
                event.end = event_end
                event.description = f"Gregorian Date: {gregorian_readable}\nHijri Date: {hijri_readable}\n Hijri AR: {hijri_readable_ar}"
                location = day_data['meta']['method']['location']
                city, country = get_location(location['latitude'], location['longitude'])
                event.location = f"{city}, {country}"
                # Add the event to the calendar
                calendar.events.add(event)
                

# Write the calendar to an .ics file with UTF-8 encoding
with open(f'prayer_times_{year}.ics', 'w', encoding='utf-8') as f:
    f.writelines(calendar)