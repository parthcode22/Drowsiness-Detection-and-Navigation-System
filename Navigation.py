import folium
import random
import webbrowser
import os
import time
from geopy.distance import geodesic
import threading
import geocoder  
from datetime import datetime
import sys

class ReststopRecommender:
    def __init__(self): 
        """Initialize the rest stop recommender system."""
        self.current_location = self.get_real_location() or (37.7749, -122.4194)  # Default: San Francisco
        self.last_recommendation_time = None
        self.recommendation_cooldown = 60  # seconds

        # database sample mock data
        self.rest_stop_db = self._initialize_rest_stop_db()

        # html map
        self.map_file = os.path.join(os.getcwd(), 'rest_stops_map.html')

        # thread to avoid block of data
        self.map_thread = None

    def get_real_location(self):
        """Get real-time latitude and longitude using geocoder."""
        try:
            g = geocoder.ip('me')
            if g.latlng:
                print(f"Real location detected: {g.latlng}")
                return tuple(g.latlng)  # returns (latitude, longitude)
            else:
                print("Could not fetch real-time location. Using default.")
                return None
        except Exception as e:  
            print(f"Error getting real location: {e}")
            return None
            
    def update_current_location(self, lat, lng):
        """Update the current location dynamically."""
        self.current_location = (lat, lng)
        self.rest_stop_db = self._initialize_rest_stop_db()

    def _initialize_rest_stop_db(self):
        """Initialize a mock database of rest stops."""
        rest_stop_types = [
            "Rest Area",
            "Gas Station",
            "Parking Area",
            "Service Plaza",
            "Hotel/Motel"
        ]

        rest_stop_names = [
            "Highway Rest Stop",
            "Quick Nap Zone",
            "24/7 Gas Station",
            "Roadside Cafe",
            "Budget Inn",
            "Safe Parking Area",
            "Driver's Rest Point",
            "Coffee Break Stop",
            "Truck Stop",
            "Rest & Refresh",
            "Highway Oasis"
        ]

        mock_db = []
        # create 15 mock rest stop around current location
        for i in range(15):
            lat_offset = (random.random() - 0.5) * 0.05
            lng_offset = (random.random() - 0.5) * 0.05

            lat = self.current_location[0] + lat_offset
            lng = self.current_location[1] + lng_offset

            rest_stop = {
                "id": f"stop_{i}",
                "name": f"{random.choice(rest_stop_names)} #{i+1}",
                "type": random.choice(rest_stop_types),
                "location": (lat, lng),
                "amenities": self._generate_random_amenities(),
                "rating": round(random.uniform(3.0, 5.0), 1)
            }

            mock_db.append(rest_stop)

        return mock_db

    def _generate_random_amenities(self):  
        """Generate random amenities for mock rest stops."""
        all_amenities = [
            "Restrooms", "Coffee", "Food", "Wifi", "Shower",
            "Gas", "ATM", "Convenience Store", "Parking",
            "24/7 Service", "EV Charging"
        ]

        num_amenities = random.randint(2, 5)
        return random.sample(all_amenities, num_amenities)

    def find_nearby_rest_stops(self, max_distance=50):
        """Find rest stops near the current location."""
        nearby_stops = []

        for stop in self.rest_stop_db:
            distance = geodesic(
                self.current_location,
                stop["location"]
            ).kilometers

            if distance <= max_distance:
                stop_info = stop.copy()
                stop_info["distance"] = round(distance, 1)  
                nearby_stops.append(stop_info)

        nearby_stops.sort(key=lambda x: x["distance"])

        return nearby_stops[:5]  

    def create_rest_stop_map(self, nearby_stops):
        """Create a map with the current location and nearby rest stops."""
        try:
            m = folium.Map(
                location=self.current_location,
                zoom_start=12
            )

            # marker
            folium.Marker(
                location=self.current_location,
                popup="Your Current Location",
                icon=folium.Icon(color="red", icon="info-sign")
            ).add_to(m)

            for stop in nearby_stops:
                icon_color = "green"
                # create a popup content with rest stop details HTML
                popup_html = f"""
                <div style="width: 200px">
                    <h4>{stop['name']}</h4>
                    <p><strong>Type:</strong> {stop['type']}</p>
                    <p><strong>Distance:</strong> {stop['distance']} km</p>
                    <p><strong>Rating:</strong> {stop['rating']} / 5.0</p>
                    <p><strong>Amenities:</strong> {', '.join(stop['amenities'])}</p>
                    <a href="https://www.google.com/maps/dir/?api=1&destination={stop['location'][0]},{stop['location'][1]}&travelmode=driving" 
                       target="_blank" style="background-color: #4CAF50; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">
                       Get Directions
                    </a>
                </div>
                """

                folium.Marker(
                    location=stop["location"],
                    popup=folium.Popup(popup_html, max_width=300),
                    icon=folium.Icon(color=icon_color)
                ).add_to(m)

            title_html = '''
            <div style="position: fixed;
                        top: 10px;
                        left: 50%;
                        transform: translateX(-50%);
                        z-index: 9999;
                        background-color: #d9534f;
                        color: white;
                        font-size: 16pt;
                        padding: 10px;
                        border-radius: 5px;">
            Drowsiness Detected! Find a place to rest safely.
            </div>
            '''
            m.get_root().html.add_child(folium.Element(title_html))

            for stop in nearby_stops:
                folium.PolyLine(
                    locations=[self.current_location, stop["location"]],  
                    color="blue",
                    weight=2,
                    opacity=0.7
                ).add_to(m)
            m.save(self.map_file)

            return self.map_file
        except Exception as e:
            print(f"Error creating map: {e}")
            return None
            
    def show_rest_stop_recommendations(self):
        """Show rest stop recommendations."""
        current_time = time.time()
        if (self.last_recommendation_time and
            current_time - self.last_recommendation_time < self.recommendation_cooldown):
            return

        self.last_recommendation_time = current_time

        try:
            nearby_stops = self.find_nearby_rest_stops()

            if nearby_stops:
                map_file_path = self.create_rest_stop_map(nearby_stops)

                if map_file_path and os.path.exists(map_file_path):
                    file_url = 'file://' + os.path.abspath(map_file_path)
                    webbrowser.open(file_url)
                    print(f"Rest stop map opened in Browser")
                else:
                    print("Failed to create map file")
            else:
                print("No rest stops found nearby.")
        except Exception as e:
            print(f"Error showing rest stop recommendations: {e}")

def main():
    recommender = ReststopRecommender()
    recommender.show_rest_stop_recommendations()

if __name__ == "__main__":
    main()
