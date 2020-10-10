import csv
import json
import numpy as np
import urllib.request as ur
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk
import matplotlib.pyplot as plt

###############-------------------------Logic Section-------------------------###############
#--------------convert json to csv file----------------------#


def Json_2_csv():
    url = ur.urlopen(
        "https://api.covid19india.org/state_district_wise.json").read().decode()

    data = json.loads(url)

    ####-------------------District Logic-------------------####

    dist = dict()
    for i in data.keys():
        dist.update(dict(data[i].get('districtData')))

    DistKeys = dist.keys()

    Head = ['District', 'Active', 'Confirmed', 'Deceased', 'Recovered']
    Record = []
    for key in DistKeys:
        Record.append([key, dist[key]['active'], dist[key]['confirmed'],
                       dist[key]['deceased'], dist[key]['recovered']])

    Write_2_CSV(Head, Record, "Districts")
    ####-------------------State Logic-------------------####
    dist = []
    States = []
    for i in data.keys():
        States.append(i)
        dist.append(data[i]['districtData'])

    def Find_Data(status):
        Data_List = []
        Temp_List = []
        for i in range(len(States)):
            for j in dist[i].keys():
                Temp_List.append(dist[i][j][status])
            Data_List.append(np.array(Temp_List).sum())
        return Data_List

    Head = ['State', 'Active', 'Confirmed', 'Deceased', 'Recovered']
    Record = []
    for state in range(len(States)):
        Record.append([States[state], Find_Data("active")[state], Find_Data("confirmed")[
                      state], Find_Data("deceased")[state], Find_Data("recovered")[state]])

    Write_2_CSV(Head, Record, "States")

#---------------------Store csv file-----------------------------#


def Write_2_CSV(Header, Rows, Type):
    if Type == "Districts":
        with open('Covid_District_Wise.csv', 'w+', newline='') as fp:
            csvW = csv.writer(fp)
            csvW.writerow(Header)
            csvW.writerows(Rows)
    if Type == "States":
        with open('Covid_States_Wise.csv', 'w+', newline='') as fp:
            csvW = csv.writer(fp)
            csvW.writerow(Header)
            csvW.writerows(Rows)


#-----------------max active cased-----------------------------#
def Max_Active_Case(data, choice, lable):
    for i in range(1, len(data)):
        if data[i]['Active'] == data[:]['Active'].max():
            lable.config(text="Maximum Active Case "+choice+" is '" +
                         str(data[i][choice])+"' With '"+str(data[i]['Active'])+"' Cases.", font=('verdana 12 bold'), bg='cyan')
            lable.place(x=200, y=220)


#------------------max Confirmed cases------------------------#
def Max_Confirmed_Case(data, choice, lable):
    for i in range(1, len(data)):
        if data[i]['Confirmed'] == data[:]['Confirmed'].max():
            lable.config(text="Maximum Confirmed Case "+choice+" is '" +
                         str(data[i][choice])+"' With '"+str(data[i]['Confirmed'])+"' Cases.", font=('verdana 12 bold'), bg='cyan')
            lable.place(x=200, y=220)


#-----------------------fetch Max Deceased Case-----------------------#
def Max_Deceased_Case(data, choice, lable):
    for i in range(1, len(data)):
        if data[i]['Deceased'] == data[:]['Deceased'].max():
            lable.config(text="Maximum Deceased Case "+choice+" is '" +
                         str(data[i][choice])+"' With '"+str(data[i]['Deceased'])+"' Cases.", font=('verdana 12 bold'), bg='cyan')
            lable.place(x=200, y=220)


#----------------------------Max Recovered Cased---------------------#
def Max_Recovered_Case(data, choice, lable):
    for i in range(1, len(data)):
        if data[i]['Recovered'] == data[:]['Recovered'].max():
            lable.config(text="Maximum Recovered Case "+choice+" is '" +
                         str(data[i][choice])+"' With '"+str(data[i]['Recovered'])+"' Cases.", font=('verdana 12 bold'), bg='cyan')
            lable.place(x=200, y=220)


#------------------------Find Data---------------------------------------#
def Find(data, choice, lable, F_lable, F_Entry, F_Button, c_b_f1, c_b_f2):

    def Find_City():
        city = F_Entry.get().strip()
        for i in range(1, len(data)):
            flag = False
            if str(data[i][choice]).upper() == str(city).upper():
                lable.config(text="""{}: {} 
Active: {}
Confirmed: {}
Deceased: {}
Recovered: {}""".format(choice, city, data[i]['Active'], data[i]['Confirmed'], data[i]['Deceased'], data[i]['Recovered']), justify='left', font=('verdana 12 bold'), bg='cyan')
                lable.place(x=520, y=320)

                names = ['Active', 'Confirmed', 'Deceased', 'Recovered']
                values = [data[i]['Active'], data[i]['Confirmed'],
                          data[i]['Deceased'], data[i]['Recovered']]
                plt.bar(names, values)
                Title = "Graph of "+city
                fig = plt.gcf()
                fig.canvas.set_window_title(Title)
                flag = True
                break

        if not flag:
            mb.showerror("Not Found", choice+" Not Found")
            lable.place_forget()

    # Lable
    F_lable.config(text="Enter District Name:",
                   font=("verdana 12 bold"))
    F_lable.place(x=325, y=250)

    # Entry
    F_Entry.config(font=("verdana 12"))
    F_Entry.place(x=520, y=250)

    # Button
    F_Button.config(text="submit", bg="white",
                    fg="blue", font=("verdana 12 bold"), command=Find_City)
    F_Button.place(x=650, y=280)

    def Show():
        val = F_Entry.get()
        if val != '':
            plt.show()
        else:
            mb.askokcancel("Input Error", "Please Enter Valid input")


    if choice == 'District':
        c_b_f1.config(command=Show)
        c_b_f1.place(x=325, y=360)

    if choice == 'State':
        c_b_f2.config(command=Show)
        c_b_f2.place(x=325, y=360)


Json_2_csv()
#-------------------------setting column types in csv file(District)----------------------------#
dt = np.dtype([('District', np.str, 20), ('Active', np.int),
               ('Confirmed', np.int), ('Deceased', np.int), ('Recovered', np.int)])


#------------------------fetch data from csv file(District)-------------------------------------#
data = np.genfromtxt(
    fname=r"Covid_District_Wise.csv", delimiter=',', dtype=dt, skip_header=1)


#-------------------------setting column types in csv file(State)-------------------------------#
State_dt = np.dtype([('State', np.str, 20), ('Active', np.int),
                     ('Confirmed', np.int), ('Deceased', np.int), ('Recovered', np.int)])

#------------------------fetch data from csv file(State)----------------------------------------#
State_Data = np.genfromtxt(
    fname=r"Covid_States_Wise.csv", delimiter=',', dtype=State_dt, skip_header=1)

#------------------Over All Data------------------#
total_active_num=data[:]['Active'].sum()
total_confirm_num=data[:]['Confirmed'].sum()
total_deceased_num=data[:]['Deceased'].sum()
total_recovered_num=data[:]['Recovered'].sum()

Total_Active = "Total Active Cases in India: " + \
    str(total_active_num)
Total_Confirmed = "Total Confirmed Cases in India: " + \
    str(total_confirm_num)
Total_Deceased = "Total Deceased Cases in India: " + \
    str(total_deceased_num)
Total_Recovered = "Total Recovered Cases in India: " + \
    str(total_recovered_num)


#--------------------------All Graph--------------------------#
def data_graph():
    names = ['Active', 'Confirmed', 'Deceased', 'Recovered']

    values = [np.log(total_active_num), np.log(total_confirm_num),
                          np.log(total_deceased_num), np.log(total_recovered_num)]
    plt.bar(names, values)
    Title = "Graph of India"
    fig = plt.gcf()
    fig.canvas.set_window_title(Title)
    plt.show()

##################------------------------------------GUI Section--------------------------------------##################
root = tk.Tk()
root.title("Survay of Covid-19")

#------------------Required widgets------------------#
NoteBook = ttk.Notebook(root)

frame1 = tk.Frame(NoteBook, width=900, height=500)
frame2 = tk.Frame(NoteBook, width=900, height=500)
frame3 = tk.Frame(NoteBook, width=900, height=500)

Find_Lable = tk.Label(frame1)
Find_Entry = tk.Entry(frame1)
Find_Button = tk.Button(frame1)

Find_State_Lable = tk.Label(frame2)
Find_State_Entry = tk.Entry(frame2)
Find_State_Button = tk.Button(frame2)

chart_button_f1 = tk.Button(
    frame1, text="Show Chart", bg="white", fg="blue", font=("verdana 12 bold"))


chart_button_f2 = tk.Button(
    frame2, text="Show Chart", bg="white", fg="blue", font=("verdana 12 bold"))

chart_button_f3 = tk.Button(
    frame3, text="Show Chart", bg="white", fg="blue", font=("verdana 12 bold"),command=data_graph)
chart_button_f3.place(x=450, y=140)





NoteBook.add(frame1, text="District")
NoteBook.add(frame2, text="State")
NoteBook.add(frame3, text="Over All")
NoteBook.pack()


#------------------Hide The Widgets-----------------#
def Forget_Widget(F_Lable, F_Entry, F_Button, c_b_f1, c_b_f2):
    F_Lable.place_forget()
    F_Entry.place_forget()
    F_Button.place_forget()
    c_b_f1.place_forget()
    c_b_f2.place_forget()
    

#------------------Display District Data------------------#


def Display_Data():
    Forget_Widget(Find_Lable, Find_Entry, Find_Button,
                  chart_button_f1, chart_button_f2)
    Choice = Dis_Choice_Entry_Field.get().strip()
    if Choice == '1':
        Max_Active_Case(data, "District", Display_Lable)

    elif Choice == '2':
        Max_Confirmed_Case(data, "District", Display_Lable)

    elif Choice == '3':
        Max_Deceased_Case(data, "District", Display_Lable)

    elif Choice == '4':
        Max_Recovered_Case(data, "District", Display_Lable)

    elif Choice == '5':
        Find(data, "District", Display_Lable,
             Find_Lable, Find_Entry, Find_Button, chart_button_f1, chart_button_f2)

    elif Choice == '6':
        if mb.askyesno("Confirm Quit", "Are You Sure ?"):
            root.destroy()

    else:
        mb.askretrycancel("Input Error", "Wrong Input Please try agian")

#------------------Display State Data------------------#


def Display_State_Data():
    Forget_Widget(Find_State_Lable, Find_State_Entry,
                  Find_State_Button, chart_button_f1, chart_button_f2)
    Choice = State_Choice_Entry_Field.get().strip()
    if Choice == '1':
        Max_Active_Case(State_Data, "State", State_Display_Lable)

    elif Choice == '2':
        Max_Confirmed_Case(State_Data, "State", State_Display_Lable)

    elif Choice == '3':
        Max_Deceased_Case(State_Data, "State", State_Display_Lable)

    elif Choice == '4':
        Max_Recovered_Case(State_Data, "State", State_Display_Lable)

    elif Choice == '5':
        Find(State_Data, "State", State_Display_Lable,
             Find_State_Lable, Find_State_Entry, Find_State_Button, chart_button_f1, chart_button_f2)

    elif Choice == '6':
        if mb.askyesno("Confirm Quit", "Are You Sure ?"):
            root.destroy()

    else:
        mb.askretrycancel("Input Error", "Wrong Input Please try agian")

#------------------Display Over all data------------------#


def Display_All_Data():
    Choice = All_Choice_Entry_Field.get().strip()
    if Choice == '1':
        All_Display_Lable.config(
            text=str(Total_Active), font=('verdana 12 bold'), bg='cyan')
        All_Display_Lable.place(x=200, y=220)

    elif Choice == '2':
        All_Display_Lable.config(
            text=str(Total_Confirmed), font=('verdana 12 bold'), bg='cyan')
        All_Display_Lable.place(x=200, y=220)

    elif Choice == '3':
        All_Display_Lable.config(
            text=str(Total_Deceased), font=('verdana 12 bold'), bg='cyan')
        All_Display_Lable.place(x=200, y=220)

    elif Choice == '4':
        All_Display_Lable.config(
            text=str(Total_Recovered), font=('verdana 12 bold'), bg='cyan')
        All_Display_Lable.place(x=200, y=220)


    elif Choice == '5':
        if mb.askyesno("Confirm Quit", "Are You Sure?"):
            root.destroy()

    else:
        mb.askretrycancel("Input Error", "Wrong Input Please try agian")


#----------------------District Module----------------------#
Choice_List = tk.Label(frame1, text="""1.Max Active case District
2.Max Confirmed case District
3.Max Deceased case District
4.Max Recovered case District
5.Find Data of District
6.Quit""", font=("verdana 12 bold italic"), justify='left').pack()


Dis_Choice_Field = tk.Label(frame1, text="Enter Your Choice:", font=(
    "verdana 12 bold italic"), justify='left').place(x=10, y=150)

Dis_Choice_Entry_Field = tk.Entry(frame1, font=("verdana 12"))
Dis_Choice_Entry_Field.place(x=200, y=150)


tk.Button(frame1, text="submit", bg="white",
          fg="blue", font=("verdana 12 bold"), command=Display_Data).place(x=325, y=180)


Display_Lable = tk.Label(frame1)

#----------------------State Module----------------------#
State_Choice_List = tk.Label(frame2, text="""1.Max Active case State
2.Max Confirmed case State
3.Max Deceased case State
4.Max Recovered case State
5.Find Data of State
6.Quit""", font=("verdana 12 bold italic"), justify='left')
State_Choice_List.place(x=315, y=0)


State_Choice_Field = tk.Label(frame2, text="Enter Your Choice:", font=(
    "verdana 12 bold italic"), justify='left').place(x=10, y=150)

State_Choice_Entry_Field = tk.Entry(frame2, font=("verdana 12"))
State_Choice_Entry_Field.place(x=200, y=150)

tk.Button(frame2, text="submit", bg="white", fg="blue", font=(
    "verdana 12 bold"), command=Display_State_Data).place(x=325, y=180)

State_Display_Lable = tk.Label(frame2)


#----------------------Over All Module----------------------#
State_Choice_List = tk.Label(frame3, text="""1.Total Active case in India
2.Total Confirmed case in India
3.Total Deceased case in India
4.Total Recovered case in India
5.Quit""", font=("verdana 12 bold italic"), justify='left')
State_Choice_List.place(x=315, y=0)


All_Choice_Field = tk.Label(frame3, text="Enter Your Choice:", font=(
    "verdana 12 bold italic"), justify='left').place(x=10, y=150)

All_Choice_Entry_Field = tk.Entry(frame3, font=("verdana 12"))
All_Choice_Entry_Field.place(x=200, y=150)

tk.Button(frame3, text="submit", bg="white", fg="blue", font=(
    "verdana 12 bold"), command=Display_All_Data).place(x=325, y=180)

All_Display_Lable = tk.Label(frame3)


root.mainloop()
