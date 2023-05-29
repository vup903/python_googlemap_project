import googlemaps
import folium

API_KEY = 'MY_API_KEY'
gmaps = googlemaps.Client(key=API_KEY)

# input
place_id_origin = '起點的地點ID'
place_id_dest = '目的地的地點ID'
mode_select = 'driving/walking'

# 把地點ID轉換為經緯度
place_details_origin = gmaps.place(place_id=place_id_origin, fields=['geometry'])
place_details_dest = gmaps.place(place_id=place_id_dest, fields=['geometry'])

location_origin = place_details_origin['result']['geometry']['location']
latitude_origin = location_origin['lat']
longitude_origin = location_origin['lng']

location_dest = place_details_dest['result']['geometry']['location']
latitude_dest = location_dest['lat']
longitude_dest = location_dest['lng']

# 獲取路徑
directions_result = gmaps.directions((latitude_origin, longitude_origin), (latitude_dest, longitude_dest), mode=mode_select)

# 獲取路徑時長
total_duration = directions_result[0]['legs'][0]['duration']['text']

# 加入地圖
map = folium.Map(location=[latitude_origin, longitude_origin], zoom_start=15)
polyline = directions_result[0]['overview_polyline']['points']
decoded_polyline = googlemaps.convert.decode_polyline(polyline)
coordinates = [(point['lat'], point['lng']) for point in decoded_polyline]

# 加入總時長的標記
icon = folium.Icon(color='blue', icon='hourglass', prefix='fa')
folium.Marker(location=coordinates[int(len(coordinates) / 2)], popup=f'總時長：{total_duration}', icon=icon).add_to(map)

# 加入起點和目的地的標記
for i, coordinate in enumerate(coordinates):
    if i == 0:
        marker = folium.Marker(location=coordinate, popup='起點', icon=folium.Icon(color='green'))
    elif i == len(coordinates) - 1:
        marker = folium.Marker(location=coordinate, popup='目的地', icon=folium.Icon(color='red'))
    marker.add_to(map)

polyline = folium.PolyLine(locations=coordinates, color='deepskyblue', weight=4)
polyline.add_to(map)

# 顯示地圖
map


