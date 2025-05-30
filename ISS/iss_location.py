import requests
import psycopg2
import reverse_geocode
from tenacity import retry, wait_fixed, stop_after_attempt


@retry(wait=wait_fixed(5), stop=stop_after_attempt(3))
def fetch_iss_data():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    print(response)
    response.raise_for_status()
    data = response.json()
    timestamp = data['timestamp']
    latitude = float(data['iss_position']['latitude'])
    longitude = float(data['iss_position']['longitude'])
    return timestamp, latitude, longitude

def get_country(latitude, longitude):
    coordinates = (latitude, longitude)
    location = reverse_geocode.search([coordinates])[0]
    country = location['country']
    return country

def store_data(timestamp, latitude, longitude, country):
    conn = psycopg2.connect(
        user='postgres',
        password='123',
        host='localhost',
        port='5432',
        dbname='iss_location_db'
    )

    cur = conn.cursor()
    cur.execute("""
        INSERT INTO iss_location (timestamp, latitude, longitude, country)
        VALUES (%s, %s, %s, %s)
    """, (timestamp, latitude, longitude, country))
    conn.commit()
    cur.close()
    conn.close()

def main():
    try:
        timestamp, latitude, longitude = fetch_iss_data()
        country = get_country(latitude, longitude)
        store_data(timestamp, latitude, longitude, country)
        print(f"Data stored successfully: {timestamp}, {latitude}, {longitude}, {country}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()