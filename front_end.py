import tkinter as tk
from tkinter import ttk
import shutil
import os

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
    value.set('Walk')  # Reset the transportation option
    var1.set('Reviews')  # Reset the first filter option
    var2.set('Rating')  # Reset the second filter option
    var3.set('Price Level')  # Reset the third filter option
def get_directions(item):
    # Add your code here to handle getting directions for the shop
    # ...

    # Record the shop's information in the notes dictionary
    notes[item['name']] = f"Directions for {item['name']}: ..."

# Show the map
def show_map(item):
    # Create a new window to display the map
    map_window = tk.Toplevel(details_window)
    map_window.title(f"Map for {item['name']}")
    map_window.geometry('400x200')

    # Add code here to display the map
    map_label = ttk.Label(map_window, text=f"Map for {item['name']} goes here...")
    map_label.pack()

    # Add a "Directions" button to the map window
    directions_button = tk.Button(map_window, text='Directions', command=lambda: get_directions(item))
    directions_button.pack()

    # Add a "Back" button to the map window
    back_button = tk.Button(map_window, text='Back', command=map_window.destroy,fg='blue')
    back_button.pack()

# Submit the search
def submit_search():
    chosen_option = value.get()
    chosen_time = scale_h.get()
    search_keyword = entry_search.get()
    sort_order = [var1.get(), var2.get(), var3.get()]

    # Open a new window to display the search results
    result_window = tk.Toplevel(root)
    result_window.title('Search Results')
    result_window.geometry('800x600')

    ##### Get backend data
    data = [
        {"name": "Shop 1", "opening_status": "Open", "Reviews": 10, "Rating": 4.5, "Price Level": 2, "Five-star Review": 5},
        {"name": "Shop 2", "opening_status": "Closed", "Reviews": 5, "Rating": 4.0, "Price Level": 3, "Five-star Review": 2},
        {"name": "Shop 3", "opening_status": "Open", "Reviews": 20, "Rating": 3.5, "Price Level": 1, "Five-star Review": 10},
    ]

    # Sort the data based on the selected sorting order
    for sort_key in reversed(sort_order):
        data.sort(key=lambda x: x[sort_key], reverse=True)

   

    # Add "Open Now" button
    open_now_button = tk.Button(result_window, text='Open Now', command=lambda: filter_open_now(result_window, data), bg='grey')
    open_now_button.pack()
    
     # Display the data
    display_data(data, result_window)
    # Store the reference to the "Open Now" button
    submit_search.open_now_button = open_now_button

# Display data
def display_data(data, result_window):
    # Create shop buttons
    for item in data:
        button = tk.Button(result_window, text=item['name'], font=('Arial', 30))
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
    open_now_data = [item for item in data if item['opening_status'] == 'Open']

    # Display only open shops
    display_data(open_now_data, result_window)

    # Destroy the "Open Now" button
    submit_search.open_now_button.destroy()

def create_form():
    global frame  # Make the frame a global variable so it can be accessed in reset_form
    global value, scale_h, entry_search, var1, var2, var3
    global frame, menu1, menu2, menu3
    style = ttk.Style()
    style.configure('Custom.TFrame', background='red', foreground='black')

    frame = ttk.Frame(root, style='Custom.TFrame')

    # Set the background label as the master for frame
    frame.master.title('Landscanner')
    frame.master.geometry('370x700')
    frame.master.resizable(False, False)

    frame.grid(sticky='nsew', padx=10, pady=10)

    optionList = ['Car', 'Walk', 'Motorbike']
    value = tk.StringVar()
    value.set('Walk')

    label_title = ttk.Label(frame, text='Quickly scan all your destinations', font=('Arial', 20, 'bold'))
    label_title.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    
    label_transport = ttk.Label(frame, text='Transportation:', font=('Arial', 14, 'bold'))
    label_transport.grid(row=1, column=0, padx=10, pady=5)

    menu = tk.OptionMenu(frame, value, *optionList)
    menu.config(width=10)
    menu.grid(row=2, column=0, padx=10, pady=5)

    scale_h = tk.Scale(frame, from_=0, to=300, orient='horizontal', label='Time minutes  ', font=('Arial', 14, 'bold'))
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

    
    
    

def show_details(item):
    global details_window
    details_window = tk.Toplevel(root)
    details_window.title('Shop Details')
    details_window.geometry('500x300')

    label_name = ttk.Label(details_window, text=f"Name: {item['name']}", font=('Arial', 22, 'bold'), anchor='center')
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

    map_button = tk.Button(details_window, text='Show Map', command=lambda: show_map(item))
    map_button.pack()

    back_button = tk.Button(details_window, text='Back', command=details_window.destroy, fg='blue')
    back_button.pack()


create_form()
# Run the main event loop
root.mainloop()
