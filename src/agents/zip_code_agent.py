import os, googlemaps

class ZipCodeAgent:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
        self.gmaps = googlemaps.Client(key=self.api_key)

    async def lookup(self, zip_code: str):

        try:
            results = self.gmaps.geocode(zip_code)
        except Exception as e:
            return (None, None, None)
        if not results:
            return (None, None, None)

        address_components = results[0]['address_components']
        city = state = None
        for comp in address_components:
            types = comp['types']
            if 'locality' in types:       # city
                city = comp['long_name']
            if 'administrative_area_level_1' in types:  # state
                state = comp['short_name']
        location = results[0]['geometry']['location']
        lat, lng = location['lat'], location['lng']
        hospitals = []
        try:
            places = self.gmaps.places_nearby(location=(lat, lng), radius=10000, type='hospital')
        except Exception as e:
            places = {}
        for place in places.get('results', [])[:3]:
            name = place.get('name')
            vicinity = place.get('vicinity') or place.get('formatted_address', '')
            hospitals.append(f"{name} ({vicinity})")
        return (city, state, hospitals)
