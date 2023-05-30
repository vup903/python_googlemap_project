#啟用API
import googlemaps
api_key = 'AIzaSyCLmBVoMPZA5HHOrxT9FAh8w3FZC3QAH64'
gmaps = googlemaps.Client(key=api_key)

import geolocation

def get_current_location():
    location = geolocation.get_location()
    return location



#找現在地點的經緯度
current_location = get_current_location()

if current_location is not None:
    latitude = current_location["latitude"]
    longitude = current_location["longitude"]
    location = current_location["latitude"], current_location["longitude"]
    # print("Current Location:")
    # print(f"Latitude: {latitude}")
    # print(f"Longitude: {longitude}")
else:
    location = 25.0174775, 121.5397653 #台大的
    #print("Unable to retrieve current location.")

#input
mode = input("請輸入您所選擇的交通方式(driving或walking或transit或bicycling):")
duration = int(input("請輸入交通時間限制(分鐘):"))
keyword = input("想找怎樣的地點呢？:")


# import requests

# def geolocate_device(api_key):
#     # 构建Geolocation API请求的URL
#     url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={api_key}'

#     # 发送POST请求到Geolocation API
#     response = requests.post(url)

#     if response.status_code == 200:
#         # 解析响应的JSON数据
#         data = response.json()
#         # 提取设备的地理位置信息
#         location = data['location']
#         latitude = location['lat']
#         longitude = location['lng']
#         accuracy = data['accuracy']

#         print(f"设备位置：纬度={latitude}, 经度={longitude}")
#         print(f"精度：{accuracy} 米")
#     else:
#         print("无法获取设备位置")

# # 调用设备定位函数
# geolocate_device(api_key)


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
    print(end)
    directions_result = gmaps.directions(start, end)
    # 提取预计到达时间（分钟）
    duration_in_minutes.append(directions_result[0]['legs'][0]['duration']['value'] // 60)
    print("预计到达时间：{} 分钟".format(duration_in_minutes[i]))


#輸出list place的ID
results_placeID = []
for i in range(len(duration_in_minutes)):
    if int(duration_in_minutes[i]) <= duration:
        results_placeID.append(places_result["results"][i]["place_id"])
#print(results_placeID)





# for cafe in places_result["results"]:
#     print(cafe)
# for i in range(len(places_result["results"])):
#     print(places_result["results"][i]["place_id"])
# 提取咖啡廳的詳細資訊
# cafes = places_result['results']
# for cafe in cafes:
#     name = cafe['name']
#     address = cafe['vicinity']
#     print(f"名稱：{name}，地址：{address}")

