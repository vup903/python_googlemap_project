import googlemaps
import folium

API_KEY = 'MY_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

# input
possible_dest_id_list = []  # 搜尋結果的List
place_id_origin = '起點的地點ID'

# 建立地圖
# 找到搜尋中心的座標以作為地圖中心
place_details_origin = gmaps.place(place_id=place_id_origin, fields=['geometry'])
location_origin = place_details_origin['result']['geometry']['location']
latitude_origin = location_origin['lat']
longitude_origin = location_origin['lng']
map_center = (latitude_origin, longitude_origin)
m = folium.Map(location=map_center, zoom_start=15)

# Add markers for each place
for place_id in possible_dest_id_list:
    place_details = gmaps.place(place_id=place_id, fields=['geometry'])
    place = place_details['result']['geometry']['location']
    latitude = place['lat']
    longitude = place['lng']
    marker = folium.Marker(location=(latitude, longitude))
    marker.add_to(m)

# Display the map
m