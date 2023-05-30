#啟用API
import googlemaps
api_key = 'AIzaSyCLmBVoMPZA5HHOrxT9FAh8w3FZC3QAH64'
gmaps = googlemaps.Client(key=api_key)


#找現在地點的經緯度
from geopy.geocoders import Nominatim

def get_current_location():
    geolocator = Nominatim(user_agent="my_app")  # 创建一个 geolocator 对象
    location = geolocator.geocode("")  # 获取当前位置
    return location.latitude, location.longitude

try:
    current_location = get_current_location()
except Exception:
    location = "25.0174775, 121.5397653"
    current_location = None
    

if current_location is not None:
    latitude = current_location[0]
    longitude = current_location[1]
    print("Current Location:")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    location = "current_location[0], current_location[1]"
else:
    location = "25.0174775, 121.5397653"  # 台大的经纬度


#input
mode = input("請輸入您所選擇的交通方式(driving或walking或transit或bicycling):")
duration = int(input("請輸入交通時間限制(分鐘):"))
keyword = input("想找怎樣的地點呢？:")


# 轉化時間成搜尋半徑（單位：公尺）
if mode == "driving" or mode == "transit":
    radius = 120*duration/60*1000
elif mode == "walking":
    radius = 10*duration/60*1000
elif mode == "bicycling":
    radius = 100*duration/60*1000

# 發送請求並獲取附近尋找店家結果
places_result = gmaps.places_nearby(
    location=location,
    radius=radius,
    keyword='cafe',
)
print(places_result.keys())
#導航並找出所需時間，篩選
import googlemaps

duration_in_minutes = []
for i in range(len(places_result["results"])):
    start = "25.0329636, 121.5654268"
    end = "place_id:" + places_result["results"][i]["place_id"]
    #print(end)
    directions_result = gmaps.directions(start, end)
    # 提取预计到达时间（分钟）
    duration_in_minutes.append(directions_result[0]['legs'][0]['duration']['value'] // 60)
    #print("预计到达时间：{} 分钟".format(duration_in_minutes[i]))


#輸出list place的ID
results_placeID = []
for i in range(len(duration_in_minutes)):
    if int(duration_in_minutes[i]) <= duration:
        results_placeID.append(places_result["results"][i]["place_id"])
print(results_placeID)

