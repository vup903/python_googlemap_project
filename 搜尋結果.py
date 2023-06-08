#!/usr/bin/env python
# coding: utf-8

# In[2]:


get_ipython().system(' pip install -U googlemaps')
import googlemaps
import pandas as pd
import numpy as np
import requests


# In[4]:


API_KEY = 'insert your google place API'


# In[5]:


gmaps = googlemaps.Client(key = API_KEY)


# In[6]:


def get_location_name(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        result = data.get("result")
        if result is not None:
            location_name = result.get("name")
            if location_name is not None:
                return location_name
    else:
        return None


# In[7]:


def get_reviews(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        result = data.get("result")
        if result is not None:
            review_count = result.get("user_ratings_total")
            if review_count is not None:
                return review_count
    else:
        return 0


# In[8]:


def get_price_level(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        result = data.get("result")
        if result is not None:
            price_level = result.get("price_level")
            if price_level is not None:
                return price_level
    else:
        price_level = np.nan
        return price_level


# In[9]:


def get_rating(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        result = data.get("result")
        if result is not None:
            rating = result.get("rating")
            if rating is not None:
                return rating
    else:
        return 0


# In[10]:


def get_open_status(place_id, api_key):
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    try:
        if data["status"] == "OK":
            result = data.get("result")
            if result is not None:
                opening_hours = result.get("opening_hours")
                opening_status = opening_hours['open_now']
                if opening_status is not None:
                    return opening_status
        else:
            opening_status = np.nan
            return opening_status
    except:
        opening_status = np.nan
        return opening_status


# In[13]:


# sort result by number of review
review_lst = []
#id_lst = ['王子凌的output']
# 我自己拿來試的 place id
id_lst = ['ChIJObxVCIapQjQRJtRS36iiCpw', 'ChIJj_hw4oapQjQRqzf5Vytr4-Q', 'ChIJT3Jp6dSpQjQRih35iMUOttc',
          'ChIJD12ae_KrQjQRLlnZx0yg8mg'] #應該放王子凌的output
#for p in place_lst:
    #places_result = gmaps.places(p)
    #place_id = places_result['results'][0]['place_id']
for ID in id_lst:
    #place_id = ID
    location_name = get_location_name(ID, API_KEY)
    review_count = get_reviews(ID, API_KEY)
    price_level = get_price_level(ID, API_KEY)
    rating = get_rating(ID, API_KEY)
    place = gmaps.place(place_id = ID)
    five_star = False
    for r in place['result']['reviews']:
        if five_star == False:
            if r['rating'] == 5:
                try:
                    five_star_review = r['text']
                    five_star = True
                except:
                    pass
        
        if five_star == True:
            break
    if five_star == False:
        five_star_review = 'No Five-star Comments'
    if price_level != None:
        price_level = float(price_level)
    else:
        price_level = np.nan
    opening_status = get_open_status(ID, API_KEY)
    if opening_status == False:
        opening_status = 'closed'
    elif opening_status == True:
        opening_status = 'open now'
    review_dict = {'Name': location_name,
                   'opening_status': opening_status,
                   'Reviews': int(review_count),
                   'Rating': float(rating),
                   'Price Level': price_level
                   'Five-star Review': five_star_review,
                   'Place ID': ID
                      }
    # 一個dictionary裡面會一個地點的資訊包含：名字、現在是否營業、評論數、評分、價格、一則五星評論、ID
    #(最後可以不要顯示Place ID，ID只是讓地圖更好的呈現)
    #所有的地點資訊(多個dict)會組成一個list
    review_lst.append(review_dict)
# function to order the list in 6 ways
def order(first, second, third):
    return sorted(review_lst, key = lambda x: (np.isnan(x[first]),
                                         -x[first] if not np.isnan(x[first]) else np.inf,
                                         np.isnan(x[second]),
                                         -x[second] if not np.isnan(x[second]) else np.inf,
                                         np.isnan(x[third]),
                                         -x[third] if not np.isnan(x[third]) else np.inf))

def output_by_choice(first, second, third):
    for r in review_lst:
        if first == 'Reviews':
            if second == 'Rating':
                return order('Reviews', 'Rating', 'Price Level')
            elif second == 'Price Level':
                return order('Reviews', 'Price Level', 'Rating')
        elif first == 'Rating':
            if second == 'Reviews':
                return order('Rating', 'Reviews', 'Price Level')
            elif second == 'Price Level':
                return order('Rating', 'Price Level', 'Reviews')
        elif first == 'Price Level':
            if second == 'Reviews':
                return order('Price Level', 'Reviews', 'Rating')
            elif second == 'Rating':
                return order('Price Level', 'Rating', 'Reviews')
            
# first: 第一順位選擇的指標 ('Reviews' or 'Rating' or 'Price Level')
first = input()
# first: 第二順位選擇的指標 ('Reviews' or 'Rating' or 'Price Level')
second = input()
# first: 第三順位選擇的指標 ('Reviews' or 'Rating' or 'Price Level')
third = input()

# 輸出值會依據使用者選擇的指標順序對這些地點做排序，輸出排好的地點裡面一樣有地點資訊(但不包含place ID)
# 前端要呈現的內容(FE_subset_keys: frontend subset keys) [ 給負責前端的人的資訊: FE_results (type:dicts inside list)]
FE_subset_keys = ['Name', 'opening_status', 'Reviews', 'Rating', 'Price Level', 'Five-star Review']
FE_results = [{key: item[key] for key in FE_subset_keys} for item in output_by_choice(first, second, third)]
print(FE_results)


# In[14]:


# 排序好的 place ID list [ 給負責地圖的人的資訊: sorted_placeid_lst (type: list) ] 
map_subset_key = ['Place ID']
sorted_placeid_dict = [{key: item[key] for key in map_subset_key} for item in output_by_choice(first, second, third)]
sorted_placeid_lst = [p['Place ID'] for p in sorted_placeid_dict]
print(sorted_placeid_lst)


# In[23]:


# 如果選擇 open now
# 只顯示現在有開的店家 (可以做成一個button,如果點了button可以多跑這個把現在沒開的篩掉)
# 如果沒有選擇 open now 就不用跑這段
def open_result(lst):
    return [x for x in lst if x['opening_status'] != 'closed']
open_FE_results = open_result(FE_results)
print(open_FE_results)


# In[20]:


sorted_placeid_dict


# In[25]:


# 如果選擇 open now
# 只顯示現在有開的店家的placeid (可以做成一個button,如果點了button可以多跑這個把現在沒開的篩掉)
# 如果沒有選擇 open now 就不用跑這段
open_sorted_placeid = [p['Place ID'] for p in sorted_placeid_dict]
print(open_sorted_placeid)


# In[17]:


# 如果沒有選擇 open now 

# 列出使用者最終選擇的 destinaion
# 假設choice以排序後選擇的排名表示
choice = int(input()) - 1  # eg.選結果中的第一名input視為1 則 choice == 0 在list中的第一個結果
def choosed_destination(choice):
    return FE_results[choice]
def choosed_destination_id(choice):
    return sorted_placeid_lst[choice]
# 列出使用者最終選擇的 destinaion 的資訊 for frontend
print(choosed_destination(choice))
# 列出使用者最終選擇的 destinaion 的資訊 for map use
print(choosed_destination_id(choice))


# In[26]:


# 如果選擇 open now

choice = int(input()) - 1  # eg.選結果中的第一名input視為1 則 choice == 0 在list中的第一個結果
def choosed_destination(choice):
    return open_FE_results[choice]
def choosed_destination_id(choice):
    return open_sorted_placeid[choice]
# 列出使用者最終選擇的 destinaion 的資訊 for frontend
print(choosed_destination(choice))
# 列出使用者最終選擇的 destinaion 的資訊 for map use
print(choosed_destination_id(choice))

