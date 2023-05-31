import tkinter as tk
from tkinter import ttk
import shutil
import os
import googlemaps
import pandas as pd
import numpy as np
import requests
import googlemaps
import folium
from tkinter import Tk
from tkwebview2.tkwebview2 import WebView2, have_runtime, install_runtime
from System.Windows.Forms import Control
from System.Threading import Thread,ApartmentState,ThreadStart
from geopy.geocoders import Nominatim
import geocoder

api_key = 'AIzaSyCc-jWH_NoUFgD2Dcy4nwoRhk91DoQ3Wkg'
gmaps = googlemaps.Client(key=api_key)


# Global dictionaries to store notes and image paths
notes = {}
images = {}
root = tk.Tk()
root.title('Landscanner')
root.geometry('500x700')
# Reset the form
def reset_form():
    global frame  # Make the frame a global variable so it can be accessed in reset_form
    frame.destroy()  # Destroy the existing frame
    reset_application()  # Reset the application

    # Reset the OptionMenu values
    value.set('walking')  # Reset the transportation option
    var1.set('Reviews')  # Reset the first filter option
    var2.set('Rating')  # Reset the second filter option
    var3.set('Price Level')  # Reset the third filter option
def get_directions(item):
    # Add your code here to handle getting directions for the shop
    # ...

    # Record the shop's information in the notes dictionary
    notes[item['name']] = f"Directions for {item['name']}: ..."


def show_result_map(): 
    global FE_results
    global value, scale_h, entry_search
    global spot, mody, open_sorted_placeid
    rev = spot.split(', ')
    lat = rev[0]
    lng = rev[1]
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    place_id_origin = str(reverse_geocode_result[0]['place_id'])
    possible_dest_id_list = open_sorted_placeid  # 搜尋結果的List

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
    m.save("C:\\Users\\denni\\Desktop\\result_map.html")
    for i in range(len(possible_dest_id_list)):
        place_details = gmaps.place(place_id = possible_dest_id_list[i], fields = ['geometry'])
        place = place_details['result']['geometry']['location']
        latitude = place['lat']
        longitude = place['lng']
        marker = folium.Marker(location=(latitude, longitude), popup = FE_results[i]['Name'])
        marker.add_to(m)
    # 儲存地圖
    m.save("C:\\Users\\denni\\Desktop\\result_map.html")


    # 顯示地圖
    def main():
        if not have_runtime():
            install_runtime()
        root=Tk()
        root.title('result_map')
        root.geometry('1200x600+5+5')
        root.iconbitmap('C:\\Users\\denni\\Desktop\\uaena.ico.ico')

        frame2=WebView2(root,500,500)
        frame2.pack(side='left',padx=20,fill='both',expand=True)
        frame2.load_url('file:///C:/Users/denni/Desktop/result_map.html')

        root.mainloop()

    if __name__ == "__main__":
        t = Thread(ThreadStart(main))
        t.ApartmentState = ApartmentState.STA
        t.Start()
        t.Join()


# Submit the search
def submit_search():
    global FE_results
    global value, scale_h, entry_search
    global spot, mody, open_sorted_placeid
    chosen_option = value.get()
    chosen_time = scale_h.get()
    search_keyword = entry_search.get()
    sort_order = [var1.get(), var2.get(), var3.get()]
    mody = chosen_option
    duration = chosen_time
    keyword = search_keyword
    # print(chosen_option, chosen_time, search_keyword, mody, duration, keyword)
     # Open a new window to display the search results
    result_window = tk.Toplevel(root)
    result_window.title('Search Results')
    result_window.geometry('800x600')
    
    g = geocoder.ip('me')
    coordinates = g.latlng
    location = '\"' + ','.join(str(coord) for coord in coordinates) + '\"'

    spot = str(coordinates[0]) + ', ' + str(coordinates[1])

    #input
    mody = chosen_option
    duration = chosen_time
    keyword = search_keyword

    # 轉化時間成搜尋半徑（單位：公尺）
    if mody == "driving" or mody == "transit":
        radius = 120*duration/60*1000
    elif mody == "walking":
        radius = 10*duration/60*1000
    elif mody == "bicycling":
        radius = 100*duration/60*1000

    # 發送請求並獲取附近尋找店家結果
    try:
        places_result = gmaps.places_nearby(
            location=spot,
            radius=radius,
            keyword=keyword,
        )
    except Exception:
        quit()
    
    duration_in_minutes = []
    for i in range(len(places_result["results"])):
        start = spot
        end = "place_id:" + places_result["results"][i]["place_id"]
        directions_result = gmaps.directions(start, end)
        # 提取预计到达时间（分钟）
        duration_in_minutes.append(directions_result[0]['legs'][0]['duration']['value'] // 60)
        #print("预计到达时间：{} 分钟".format(duration_in_minutes[i]))

    #輸出list place的ID
    results_placeID = []
    for i in range(len(duration_in_minutes)):
        if int(duration_in_minutes[i]) <= duration:
            results_placeID.append(places_result["results"][i]["place_id"])
   

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


    # sort result by number of review
    review_lst = []
    id_lst = results_placeID
    for ID in id_lst:
        #place_id = ID
        location_name = get_location_name(ID, api_key)
        review_count = get_reviews(ID, api_key)
        price_level = get_price_level(ID, api_key)
        rating = get_rating(ID, api_key)
        place = gmaps.place(place_id = ID)
        five_star = False
        try:
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
        except Exception:
            quit()
        if five_star == False:
            five_star_review = 'No Five-star Comments'
        if price_level != None:
            price_level = float(price_level)
        else:
            price_level = np.nan
        opening_status = get_open_status(ID, api_key)
        if opening_status == False:
            opening_status = 'closed'
        elif opening_status == True:
            opening_status = 'open now'
        review_dict = {'Name': location_name,
                       'opening_status': opening_status,
                       'Reviews': int(review_count),
                       'Rating': float(rating),
                       'Price Level': price_level,
                       'Five-star Review': five_star_review,
                       'Place ID': ID}


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


    first = var1.get()
    second = var2.get()
    third = var3.get()

    FE_subset_keys = ['Name', 'opening_status', 'Reviews', 'Rating', 'Price Level', 'Five-star Review', 'Place ID']
    FE_results = [{key: item[key] for key in FE_subset_keys} for item in output_by_choice(first, second, third)]

    map_subset_key = ['Place ID']
    sorted_placeid_dict = [{key: item[key] for key in map_subset_key} for item in output_by_choice(first, second, third)]
    sorted_placeid_lst = [p['Place ID'] for p in sorted_placeid_dict]

    
    
    def open_result(lst):
        return [x for x in lst if x['opening_status'] != 'closed']
    open_FE_results = open_result(FE_results)
    
    sorted_placeid_dict
    
    open_sorted_placeid = [p['Place ID'] for p in sorted_placeid_dict]

    ##### Get backend data
    data = FE_results

    # Sort the data based on the selected sorting order
    for sort_key in reversed(sort_order):
        data.sort(key=lambda x: x[sort_key], reverse=True)

   
    # Add "Open Now" button
    open_now_button = tk.Button(result_window, text='Open Now', command=lambda: filter_open_now(result_window, data), bg='grey')
    open_now_button.pack()
    
     # Display the data
    result_window.iconbitmap('C:\\Users\\denni\\Desktop\\uaena.ico.ico')
    display_data(data, result_window)
    
    show_result_map()

    # Store the reference to the "Open Now" button
    submit_search.open_now_button = open_now_button



# Display data
def display_data(data, result_window):
    # Create shop buttons
    for item in data:
        button = tk.Button(result_window, text=item['Name'], font=('Arial', 30))
        button.bind("<Button-1>", lambda event, item=item: show_details(item))
        button.pack(fill=tk.BOTH, expand=True)

    # Add a back button
    back_button = tk.Button(result_window, text='Back', command=result_window.destroy, fg='blue', font=('Arial', 16))
    back_button.pack()



# Drag and drop image
def drop_image(item):
    drop_window = tk.Toplevel(root)
    drop_window.title(f"Drop an image for {item['name']}")
    drop_window.geometry('400x200')

    label_drop = tk.Label(drop_window, text='Drag and drop your image file here...')
    label_drop.pack(fill=tk.BOTH, expand=tk.YES)

    label_drop.drop_target_register(tk.DND_FILES)
    label_drop.dnd_bind('<<Drop>>', lambda event: save_image_from_local(event.data, item, drop_window))

# Save local image
def save_image_from_local(image_path, item, drop_window):
    destination_path = os.path.join('images', os.path.basename(image_path))
    shutil.copy(image_path, destination_path)

    images[item['name']] = destination_path

    drop_window.destroy()

# Show notes
def show_notes(item, details_window=None):
    notes_window = tk.Toplevel(details_window)
    notes_window.title(f"Notes for {item['name']}")
    notes_window.geometry('400x400')

    label_notes = ttk.Label(notes_window, text="Here you can write your notes:")
    label_notes.pack()

    text_notes = tk.Text(notes_window)
    text_notes.insert('1.0', notes.get(item['name'], ''))  # Use existing note if it exists, otherwise use empty string
    text_notes.pack()

    button_save = tk.Button(notes_window, text='Save', command=lambda: save_notes(item, text_notes, notes_window))
    button_save.pack()

    button_back = tk.Button(notes_window, text='Back', command=notes_window.destroy, fg='blue')
    button_back.pack()


# Save notes
def save_notes(item, text_notes, notes_window):
    notes[item['name']] = text_notes.get('1.0', 'end-1c')  # Save the note to the global dictionary
    notes_window.destroy()

# Reset the application
def reset_application():
    # Clear the global dictionaries
    global notes, images, frame
    notes.clear()
    images.clear()

    # Destroy all children of root
    for widget in root.winfo_children():
        widget.destroy()

    # Recreate the frame and widgets
    create_form()

# Show introduction
def show_introduction():
    introduction_window = tk.Toplevel(root)
    introduction_window.title('README')
    introduction_window.geometry('800x300')

    label_intro = ttk.Label(introduction_window, text='Welcome to the Introduction Screen!')
    label_intro.pack()

    # Add your additional text
    additional_text = """
    This is a Landscanner application that allows you to quickly scan all your destinations. 
    It provides features such as searching for shops, filtering results, dropping images, and adding notes.

    Usage:
    1. Select your transportation option from the drop-down menu.
    2. Set the desired time in minutes using the scale.
    3. Enter a search keyword to find relevant shops.
    4. Choose filter options to sort the search results.
    5. Click on the "Search" button to display the results.
    6. Click on a shop to view detailed information and perform actions like adding notes or dropping images.
    7. Use the "Reset" button to clear the form and start a new search.

    Feel free to explore all the features and enjoy using Landscanner!

    """
    additional_label = ttk.Label(introduction_window, text=additional_text, justify=tk.LEFT)
    additional_label.pack()
    # Add a back button
    back_button = tk.Button(introduction_window, text='Back', command=introduction_window.destroy, fg='blue')
    back_button.pack()

# Callback function when an option is changed
def option_changed(*args):
    global menu1 
    global menu2 
    global menu3 
    options = ['Reviews', 'Rating', 'Price Level']
    selected_options = [var1.get(), var2.get(), var3.get()]

    # Clear the existing options in the menus
    menu1['menu'].delete(0, 'end')
    menu2['menu'].delete(0, 'end')
    menu3['menu'].delete(0, 'end')

    # Add new options to the menus
    for option in options:
        if selected_options.count(option) < 2:
            menu1['menu'].add_command(label=option, command=lambda option=option: var1.set(option))
            menu2['menu'].add_command(label=option, command=lambda option=option: var2.set(option))
            menu3['menu'].add_command(label=option, command=lambda option=option: var3.set(option))



# Show only open now shops
def filter_open_now(result_window, data):
    # Clear the current buttons
    for widget in result_window.winfo_children():
        if isinstance(widget, tk.Button) and widget['text'] != 'Open Now':
            widget.destroy()

    # Filter only open shops
    open_now_data = [item for item in data if item['opening_status'] == 'open now']

    # Display only open shops
    display_data(open_now_data, result_window)

    # Destroy the "Open Now" button
    submit_search.open_now_button.destroy()

def create_form():
    global frame  # Make the frame a global variable so it can be accessed in reset_form
    global value, scale_h, entry_search, var1, var2, var3
    global frame, menu1, menu2, menu3
    style = ttk.Style()
    style.configure('Custom.TFrame', background='#EE82EE', foreground='black')

    frame = ttk.Frame(root, style='Custom.TFrame')

    # Set the background label as the master for frame
    frame.master.title('Landscanner')
    frame.master.geometry('500x650')
    frame.master.resizable(False, False)
    frame.master.iconbitmap('C:\\Users\\denni\\Desktop\\uaena.ico.ico')

    frame.grid(sticky='nsew', padx=10, pady=10)

    optionList = ['driving', 'walking', 'bicycling']
    value = tk.StringVar()
    value.set('walking')

    label_title = ttk.Label(frame, text='Quickly scan all your destinations', font=('Arial', 20, 'bold'))
    label_title.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    label_transport = ttk.Label(frame, text='Transportation:', font=('Arial', 14, 'bold'))
    label_transport.grid(row=1, column=0, padx=10, pady=5)

    menu = tk.OptionMenu(frame, value, *optionList)
    menu.config(width=10)
    menu.grid(row=2, column=0, padx=10, pady=5)

    scale_h = tk.Scale(frame, from_=0, to=300, orient='horizontal', label='                  Time(mins)', font=('Arial', 14, 'bold'), length=300)
    scale_h.grid(row=3, columnspan=1, padx=10, pady=5)

    label_search = ttk.Label(frame, text='Search Keyword:', font=('Arial', 14, 'bold'))
    label_search.grid(row=4, column=0, padx=10, pady=5)

    entry_search = tk.Entry(frame)
    entry_search.grid(row=5, column=0, padx=10, pady=5)

    button_reset = ttk.Button(frame, text='Reset', command=reset_form)
    button_reset.grid(row=16, column=0, padx=10, pady=5)

    button_notes = ttk.Button(frame, text='Notes', command=show_notes)
    button_notes.grid(row=17, column=0, padx=10, pady=5)

    options = ['Reviews', 'Rating', 'Price Level']
    var1 = tk.StringVar()
    var2 = tk.StringVar()
    var3 = tk.StringVar()
    var1.set(options[0])
    var2.set(options[1])
    var3.set(options[2])

    filter_label = ttk.Label(frame, text='Filters', font=('Arial', 16, 'bold'))
    filter_label.grid(row=6, column=0, padx=10, pady=5)

    label1 = ttk.Label(frame, text='1:', font=('Arial', 14, 'bold'))
    label1.grid(row=7, column=0, padx=10, pady=5)

    menu1 = tk.OptionMenu(frame, var1, *options)
    menu1.grid(row=8, column=0, padx=10, pady=5)

    label2 = ttk.Label(frame, text='2:', font=('Arial', 14, 'bold'))
    label2.grid(row=9, column=0, padx=10, pady=5)

    menu2 = tk.OptionMenu(frame, var2, *options)
    menu2.grid(row=10, column=0, padx=10, pady=5)

    label3 = ttk.Label(frame, text='3:', font=('Arial', 14, 'bold'))
    label3.grid(row=11, column=0, padx=10, pady=5)

    menu3 = tk.OptionMenu(frame, var3, *options)
    menu3.grid(row=12, column=0, padx=10, pady=5)

    var1.trace_add('write', option_changed)
    var2.trace_add('write', option_changed)
    var3.trace_add('write', option_changed)
    
    style = ttk.Style()
    style.configure('Special.TButton', font=('Arial', 22, 'bold'))
    button_search = ttk.Button(frame, text='Search', command=submit_search,style='Special.TButton')
    button_search.grid(row=13, padx=10, pady=5)

    button_intro = ttk.Button(root, text='README', command=show_introduction)
    button_intro.grid(row=14, column=0, padx=10, pady=5)

    button_exit = ttk.Button(frame, text='Exit', command=root.destroy)
    button_exit.grid(row=15, column=0, padx=10, pady=5)

    
def show_route_map():
    global spot, mody, zzz
    # input
    rev = spot.split(', ')
    lat = rev[0]
    lng = rev[1]
    reverse_geocode_result = gmaps.reverse_geocode((lat, lng))
    place_id_origin = str(reverse_geocode_result[0]['place_id'])
    place_id_dest = str(zzz)
    mode_select = mody

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
    mapp = folium.Map(location=[latitude_origin, longitude_origin], zoom_start=15)
    polyline = directions_result[0]['overview_polyline']['points']
    decoded_polyline = googlemaps.convert.decode_polyline(polyline)
    coordinates = [(point['lat'], point['lng']) for point in decoded_polyline]

    # 加入總時長的標記
    icon = folium.Icon(color='blue', icon='hourglass', prefix='fa')
    folium.Marker(location=coordinates[int(len(coordinates) / 2)], popup=f'總時長：{total_duration}', icon=icon).add_to(mapp)

    # 加入起點和目的地的標記
    for i, coordinate in enumerate(coordinates):
        if i == 0:
            marker = folium.Marker(location=coordinate, popup='起點', icon=folium.Icon(color='green'))
        elif i == len(coordinates) - 1:
            marker = folium.Marker(location=coordinate, popup='目的地', icon=folium.Icon(color='red'))
        marker.add_to(mapp)

    polyline = folium.PolyLine(locations=coordinates, color='deepskyblue', weight=4)
    polyline.add_to(mapp)

    # 儲存地圖
    mapp.save("C:\\Users\\denni\\Desktop\\route_map.html")

    
    # 顯示地圖
    def main():
        if not have_runtime():
            install_runtime()
        root=Tk()
        root.title('route_map')
        root.geometry('1200x600+5+5')
        root.iconbitmap('C:\\Users\\denni\\Desktop\\uaena.ico.ico')

        frame2=WebView2(root,500,500)
        frame2.pack(side='left',padx=20,fill='both',expand=True)
        frame2.load_url('file:///C:/Users/denni/Desktop/route_map.html')

        root.mainloop()

    if __name__ == "__main__":
        t = Thread(ThreadStart(main))
        t.ApartmentState = ApartmentState.STA
        t.Start()
        t.Join()


def show_details(item):
    global details_window
    global zzz
    details_window = tk.Toplevel(root)
    details_window.title('Shop Details')
    details_window.geometry('1000x500')
    details_window.iconbitmap('C:\\Users\\denni\\Desktop\\uaena.ico.ico')
    zzz = item['Place ID']

    label_name = ttk.Label(details_window, text=f"Name: {item['Name']}", font=('Arial', 22, 'bold'), anchor='center')
    label_name.pack()

    label_opening_status = ttk.Label(details_window, text=f"Opening Status: {item['opening_status']}", font=('Arial', 20), anchor='center')
    label_opening_status.pack()

    label_reviews = ttk.Label(details_window, text=f"Reviews: {item['Reviews']}", font=('Arial', 20), anchor='center')
    label_reviews.pack()

    label_rating = ttk.Label(details_window, text=f"Rating: {item['Rating']}", font=('Arial', 20), anchor='center')
    label_rating.pack()

    label_price_level = ttk.Label(details_window, text=f"Price Level: {item['Price Level']}", font=('Arial', 20), anchor='center')
    label_price_level.pack()

    label_five_star = ttk.Label(details_window, text=f"Five-star Review: {item['Five-star Review']}", font=('Arial', 20), anchor='center')
    label_five_star.pack()

    button_notes = ttk.Button(details_window, text='Notes', command=lambda: show_notes(item, details_window))
    button_notes.pack()

    button_drop_image = tk.Button(details_window, text='Drop an image here...', command=lambda: drop_image(item))
    button_drop_image.pack()

    map_button = tk.Button(details_window, text='Show Map', command=lambda: show_route_map())
    map_button.pack()

    back_button = tk.Button(details_window, text='Back', command=details_window.destroy, fg='blue')
    back_button.pack()

create_form()
# Run the main event loop
root.mainloop()