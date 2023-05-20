from tkinter import *
from tkinter import ttk
import random

import threading
from threading import Thread

from time import sleep as s
from datetime import datetime as d

import os
import json

# Gray (BG): #292929
# Orange (FG): #fe844e
# Dark Orange (Highlight BG): #d64728


# Static Color Variable
bg_color = '#292929'
fg_color = '#fe844e'

# Static Color Variable for Highlited text
high_bg_color = '#d64728'
high_fg_color = '#292929'

# Static Font Variable
st_font = 'Sitka'

# Define Paths
first_flag = False
appdata_path = os.environ['AppData']
makatopia_dir_path = appdata_path + r'\Makatopia'
static_makatopia_conf_path = appdata_path + r'\Makatopia\makatopia_database.json'

# Database Formate
database_formate = json.loads('[{}]')

# Database Updator Function
def update_json(data, filename=static_makatopia_conf_path):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=2)

# Delete Element from Database by ID
def delete_by_iD(iD, filename=static_makatopia_conf_path):
    new_data = []
    iD = int(iD)
    with open(filename) as f:
        data_list = json.load(f)
        for items in data_list:
            if items['ID'] == iD:
                pass
            else:
                new_data.append(items)

    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=2)

# Folder and File Creator for First Use
def file_manager():
    global first_flag, database_formate, appdata_path, makatopia_dir_path, static_makatopia_conf_path

    if 'Makatopia' in os.listdir(appdata_path):
        if 'makatopia_database.json' not in os.listdir(makatopia_dir_path):
            first_flag = True
            with open(f'{makatopia_dir_path}\makatopia_database.json', 'w') as f:
                json.dump(database_formate, f, indent=2)
                f.close()
        elif int(os.path.getsize(static_makatopia_conf_path)) <= 10:
            first_flag = True
            with open(f'{makatopia_dir_path}\makatopia_database.json', 'w') as f:
                json.dump(database_formate, f, indent=2)
                f.close()
        else:
            pass
    else:
        first_flag = True
        os.mkdir(f'{appdata_path}\Makatopia')
        with open(f'{makatopia_dir_path}\makatopia_database.json', 'w') as f:
            json.dump(database_formate, f, indent=2)
            f.close()
        pass

file_manager()

# Indexed Day Function
def indexed_day(today:str):
    for index, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']):
        if today == day:
            return index

# Define Thread Event
thread_Event = threading.Event()
thread_Event.clear()

thread_Event2 = threading.Event()
thread_Event2.clear()

# Tk Windiow Initiation
brain = Tk()
brain.configure(background=fg_color)
brain.geometry('1100x650+150+70')
brain.overrideredirect(True)
brain.resizable(False, False)

# ttk Style
style = ttk.Style()

# Body
body = Frame(brain,
width=1098,
height=625,
highlightthickness=0,
bg=bg_color
)
body.pack_propagate(False)
body.place(x=1,y=24)

# Banner
img = PhotoImage(file=r"F:\Spoiled Projects (py)\Makatopia Source\img.png")
banner = Label(body,
image=img,
bg=bg_color
)
banner.place(x=-2,y=-60)

# Title Bar Implimantation
title_bar = Label(brain,
bg=fg_color,
padx=1100,
pady=3
)
title_bar.place(x=0,y=0)

# Window Move Function
def get_position(evn):
    xwin = brain.winfo_x()
    ywin = brain.winfo_y()

    rtp_x = evn.x_root
    rtp_y = evn.y_root

    xwin = xwin - rtp_x
    ywin = ywin - rtp_y

    def move_fun(e):
        brain.geometry('+{0}+{1}'.format(e.x_root + xwin, e.y_root + ywin))
    rtp_x = evn.x_root
    rtp_y = evn.y_root
    title_bar.bind('<B1-Motion>', move_fun)

title_bar.bind('<Button-1>', get_position)
title_bar.bind('<B1-Motion>', get_position)

# Exit Button
exit_button_icon = PhotoImage(file=r"F:\Spoiled Projects (py)\Makatopia Source\exit_button.png")
exit_button = Button(brain,
    image=exit_button_icon,
    bd=0,
    repeatdelay=1,
    bg=fg_color,
    relief=FLAT,
    activebackground=fg_color,
    highlightthickness=0,
    padx=10,
    pady=2,
    command=brain.quit
)
exit_button.place(x=1070, y=2)

# Dynamic Event Frame (For Placement)
dyn_event_frame = Frame(body,
width=944,
height=469,
relief=SOLID,
bg=bg_color,
highlightbackground=fg_color,
highlightcolor=fg_color,
highlightthickness=1,
bd=0
)
dyn_event_frame.pack_propagate(False)
dyn_event_frame.place(x=140,y=142)

# Style for Event TreView
style.theme_use('classic')
style.configure('Treeview.Heading',
font=(st_font, 12,'bold'),
borderwidth=0,
background=fg_color, 
foreground=bg_color
)
style.configure('Treeview',
font=(st_font, 13),
borderwidth=0,
background=bg_color,
foreground=fg_color,
fieldbackground=bg_color
)
style.map('Treeview', background=[('selected', fg_color)], foreground=[('selected', bg_color)])
style.map('Treeview.Heading', background=[('selected', fg_color)], foreground=[('selected', fg_color)])

# Event TreeView
event_tree = ttk.Treeview(dyn_event_frame, height=22, columns=('event', 'time', 'day', 'id'))

# Prevent from Resizing Headings 
def disabled(event):
    if event_tree.identify_region(event.x, event.y) == "separator":
        return "break"
event_tree.bind('<Button-1>', disabled)

# Columns
event_tree.column('#0', width=0, stretch=NO)
event_tree.column('event', width=619, anchor=W)
event_tree.column('time', width=80, anchor=W)
event_tree.column('day', width=80, anchor=W)
event_tree.column('id', width=80, anchor=W)

# Headings for event_tree
event_tree.heading('#0', text='')
event_tree.heading('event', text='Event', anchor=W)
event_tree.heading('time', text='Time', anchor=W)
event_tree.heading('day', text=' Day', anchor=W)
event_tree.heading('id', text='ID', anchor=W)

event_tree.pack(fill=BOTH, expand=1)

# Existing Data Sorter
if first_flag == True:
    pass
else:
    with open(static_makatopia_conf_path) as onetime:
        extracted_data = json.load(onetime)
        for values in extracted_data:
            b_EVENT = values['event_name']
            b_TIME = values['time']
            b_DAY = values['day']
            b_ID = values['ID']
            iid = int(values['ID'])
            event_tree.insert(parent='', index='end', iid=iid, text='', values=(b_EVENT, b_TIME, b_DAY, b_ID))
    thread_Event2.set()

# Event Label
event_label = Label(body,
text='Register an Event',
font=(st_font, 13, 'bold'),
bg=fg_color,
fg=bg_color,
height=2
)
event_label.place(x=140, y=16, width=650)

# Event Entry
event_entry = Text(body,
insertbackground=fg_color,
highlightthickness=1,
highlightbackground=fg_color,
highlightcolor=fg_color,
font=(st_font, 18),
bd=0,
bg=bg_color,
fg=fg_color
)
event_entry.place(x=140, y=52, height=82, width=650)

# Colon Label
colon_label = Label(body,
text=':',
font=(st_font, 14, 'bold'),
bg=bg_color,
fg=fg_color
)
colon_label.place(x=796, y=44, height=33, width=151)

# Time Label
time_label = Label(body,
text='Time (24-Hour)',
font=(st_font, 11, 'bold'),
bg=fg_color,
fg=bg_color
)
time_label.place(x=796, y=16, height=33, width=151)

# Time Entry (Hours)
hours = Entry(body,
insertbackground=fg_color,
highlightthickness=1,
highlightbackground=fg_color,
highlightcolor=fg_color,
font=(st_font, 13),
bd=0,
bg=bg_color,
fg=fg_color
)
hours.place(x=796, y=48, height=24, width=70)

# Time Entry (Minutes)
minutes = Entry(body,
insertbackground=fg_color,
highlightthickness=1,
highlightbackground=fg_color,
highlightcolor=fg_color,
font=(st_font, 13),
bd=0,
bg=bg_color,
fg=fg_color
)
minutes.place(x=877, y=48, height=24, width=70)

# Date Entry
day_label = Label(body,
text='Day',
font=(st_font, 11, 'bold'),
bg=fg_color,
fg=bg_color
)
day_label.place(x=796, y=78, height=33, width=151)

# Day OptionMenu
days = StringVar()
days.set('Choose Day')
days_optionmenu = OptionMenu(body, days, 
'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
days_optionmenu.configure(bg=bg_color,
fg=fg_color,
highlightbackground=fg_color, 
highlightcolor=fg_color, 
activebackground=bg_color,
activeforeground=fg_color,
borderwidth=0,
bd=0, 
highlightthickness=1,
relief=FLAT,
font=(st_font, 11, 'bold'))

days_optionmenu['menu'].config(bg=bg_color, 
fg=fg_color, 
activebackground=fg_color, 
activeforeground=bg_color,
selectcolor=fg_color,
foreground=fg_color,
background=bg_color)
days_optionmenu.place(x=796, y=111, height=23, width=151)

# Main Event Scheduler
def main_event_scheduler():
    global static_makatopia_conf_path, database_formate, looped
    global style, highlighted_ids

    looped = False
    highlighted_ids = []

    while True:
        s(0.3)

        # Check any File Error
        file_manager()

        thread_Event2.wait()

        with open(static_makatopia_conf_path) as f:
            fields = json.load(f)
                
            if str(fields) == str(database_formate):
                while True:
                    s(0.1)
                    with open(static_makatopia_conf_path) as file:
                        new_fields = json.load(file)
                        if new_fields != database_formate:
                            break
                        file.close()
                        
            try:
                for field in fields:
                    last_min = d.now().minute
                    if field['time'] == f'{d.now().hour}:{last_min}' and indexed_day(field['day']) == d.now().weekday():
                        highlighted_ids.append(field['ID'])
                        looped = True
                
                if looped == True:
                    brain.attributes('-topmost',True)
                    brain.attributes('-topmost',False)
                    style.map('Treeview', background=[('selected', high_bg_color)], foreground=[('selected', high_fg_color)])

                    try:
                        event_tree.selection_set(tuple(highlighted_ids))
                    except Exception:
                        event_tree.selection_remove(tuple(highlighted_ids))
                        style.map('Treeview', background=[('selected', fg_color)], foreground=[('selected', bg_color)])
                        highlighted_ids = []
                        looped = False
                        continue

                    while d.now().minute == last_min:
                        s(1)

                    try:
                        event_tree.selection_remove(tuple(highlighted_ids))
                    except Exception:
                        pass

                    style.map('Treeview', background=[('selected', fg_color)], foreground=[('selected', bg_color)])
                    highlighted_ids = []
                    looped = False

            except KeyError:
                highlighted_ids = []
                looped = False
                continue

# Insert Button Function
def insert_button_function():
    global event_entry, hours, minutes, days
    global event_label, time_label, day_label
    global event_error, time_error
    global f_EVENT, f_TIME, f_DAY
    global first_flag, static_makatopia_conf_path, temp_list, temp_data, database_formate

    while True:
        event_error = False
        time_error = False
        day_error = False

        event_to_insert = ''
        hours_to_insert = ''
        minutes_to_insert = ''

        f_EVENT = ''
        f_TIME = ''
        f_DAY = ''

        thread_Event.wait()

        # Check any File Error
        file_manager()

        # Get Event
        event_to_insert = event_entry.get('1.0', END)
        if event_to_insert == '\n':
            event_error = True
            pass
        else:
            f_EVENT = event_to_insert.strip('\n')
        
        # Get Time
        hours_to_insert = hours.get()
        minutes_to_insert = minutes.get()

        # Check for Valid Time
        if not hours_to_insert.isdigit() or not minutes_to_insert.isdigit():
            time_error = True
            pass
        else:
            if hours_to_insert == '0' or minutes_to_insert == '0':
                time_error = True
                pass

            if len(hours_to_insert) == 1:
                hours_to_insert = '0' + hours_to_insert
            if len(minutes_to_insert) == 1:
                minutes_to_insert = '0' + minutes_to_insert

            if len(hours_to_insert) >= 3 or len(minutes_to_insert) >= 3:
                time_error = True
                pass

            f_TIME = f'{hours_to_insert}:{minutes_to_insert}'

        # Set f_DAY
        day_to_insert = days.get()
        if day_to_insert == 'Choose Day':
            day_error = True
            pass
        else:
            f_DAY = day_to_insert

        # Random ID Generator
        temp_rnd_iD = ''
        with open(static_makatopia_conf_path) as rnd_id_check:
            data_to_match_id_with = json.load(rnd_id_check)
            for every_id_of_data_fields in data_to_match_id_with:
                temp_rnd_iD = ''.join(random.choices('0123456789', k=6)) #.strip('[]').replace("'",'').replace(' ','').replace(',','')
                if every_id_of_data_fields == temp_rnd_iD:
                    pass
                else:
                    temp_rnd_iD = int(temp_rnd_iD)
                    break

        # Error Checking Block and Data Registration
        if event_error is True or time_error is True or day_error is True:
            if event_error is True:
                event_label.configure(text="Event can't be Empty")
                event_error = False
                pass
            if time_error is True:
                time_label.configure(text='Time Not Valid')
                time_error = False
                pass
            if day_error is True:
                day_label.configure(text="Day Not Valid")
                day_error = False
                pass
            s(2.5)
            event_label.configure(text='Register an Event')
            time_label.configure(text='Time')
            day_label.configure(text='Day')
            thread_Event.clear()
            continue
        else:
            event_tree.insert(parent='', index='end', iid=temp_rnd_iD, text='', values=(f_EVENT, f_TIME, f_DAY, temp_rnd_iD))

            # Add Data to Database
            new_database_field_to_append = {"event_name": f_EVENT, "time": f_TIME, "day": f_DAY, "ID": temp_rnd_iD}

            with open(static_makatopia_conf_path) as f:
                data_to_read = json.load(f)
                data_to_read.append(new_database_field_to_append)
                update_json(data_to_read)

            # Remove first Empty Data Field
            if first_flag == True:
                temp_list = []
                with open(static_makatopia_conf_path) as f:
                    temp_data = json.load(f)
                    for data_fields in temp_data:
                        indx = temp_data.index(data_fields)
                        if indx == 0:
                            pass
                        else:
                            temp_list.append(data_fields)
                    
                    update_json(temp_list)
                first_flag = False

            thread_Event2.set()

            thread_Event.clear()

Thread(target=insert_button_function, daemon=True).start()
Thread(target=main_event_scheduler, daemon=True).start()

# Insert Button
insert_button = Button(body, 
    text='Insert',
    font=(st_font, 13, 'bold'),
    bd=0,
    bg=fg_color,
    fg=bg_color,
    activebackground=bg_color,
    activeforeground=fg_color,
    repeatdelay=1,
    relief=RAISED,
    padx=49,
    pady=6,
    height=2,
    width=3,
    highlightthickness=0,
    command=thread_Event.set
    )
insert_button.place(x=954,y=16)

# Delete Button Function
def delete_button_function():
    global style

    with open(static_makatopia_conf_path) as checker_file:
        d_to_match_with = json.load(checker_file)
        if str(d_to_match_with) == str(database_formate):
            return

    style.map('Treeview', background=[('selected', fg_color)], foreground=[('selected', bg_color)])

    try:
        empty_check = event_tree.selection()
        
        if len(empty_check) > 1:
            for delete_ids in empty_check:
                data_field_iD = event_tree.item(delete_ids)['values']
                delete_by_iD(data_field_iD[3])

                if empty_check != tuple():
                    event_tree.delete(delete_ids)
        else:
            data_field_iD = event_tree.item(empty_check)['values']
            delete_by_iD(data_field_iD[3])

            if empty_check != tuple():
                event_tree.delete(empty_check)
    except Exception:
        pass

    # Check any File Error
    file_manager()

# Delete Button
delete_button = Button(body, 
    text='Delete',
    font=(st_font, 13, 'bold'),
    bd=0,
    bg=fg_color,
    fg=bg_color,
    activebackground=bg_color,
    activeforeground=fg_color,
    repeatdelay=1,
    relief=RAISED,
    padx=49,
    pady=6,
    height=2,
    width=3,
    highlightthickness=0,
    command=delete_button_function
    )
delete_button.place(x=954,y=78)

# Main Loop
if __name__ == "__main__":
    brain.mainloop()
