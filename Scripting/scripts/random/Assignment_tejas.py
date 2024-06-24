import csv
import datetime
import pandas as pd

def date_function():
    data = pd.read_csv('load_settings.csv')
    print(data)
    


    date_to_compare = datetime.date(2023,1,1) # we can set custom date here as well, i am putting 1st jan

    # taking input of the custom date
    birthday=input("Input the date? (in DD/MM/YYYY)->  ") #string type
    date_object = datetime.datetime.strptime(birthday, '%d/%m/%Y').date() 

    print()

    #empty array for the dates to be entered.
    fields = []

    # comparing the range of given dates, keeping the delta of 1
    delta = datetime.timedelta(days=1)

    if(date_to_compare > date_object):
        #if the number of rows are empty -> full load
        if(data.shape[0] == 0):
            while(date_to_compare <= date_object):
                print(date_to_compare, end="\n")
                fields.append(date_to_compare)
                new_rows = [{'dates': date_to_compare}]
                data = data.append(new_rows, ignore_index=True)
                date_to_compare += delta
            data.to_csv('load_settings.csv',mode='w',index=False)    
            print(data)
        else: # if there is some data present already, then just append it -> incremental load
            max_date = data['dates'].iloc[-1]
            max_date_date = datetime.datetime.strptime(max_date,'%Y-%m-%d').date()
            while(max_date_date <= date_object):
                print(max_date_date, end="\n")
                fields.append(max_date_date)
                new_rows = [{'dates': max_date_date}]
                data = data.append(new_rows, ignore_index=True)
                max_date_date += delta
            data.to_csv('load_settings.csv',mode='a',index=False) 
    elif(date_to_compare< date_object):
        #if the number of rows are empty -> full load
        if(data.shape[0] == 0):
            while(date_to_compare <= date_object):
                print(date_to_compare, end="\n")
                fields.append(date_to_compare)
                new_rows = [{'dates': date_to_compare}]
                data = data.append(new_rows, ignore_index=True)
                date_to_compare += delta
            data.to_csv('load_settings.csv',mode='w',index=False) 
            print(data)
        else: 
        # if there is some data present already, then just append it -> incremental load
        # a:  open an existing file for append operation. It won’t override existing data.
            max_date = data['dates'].iloc[-1]
            max_date_date = datetime.datetime.strptime(max_date,'%Y-%m-%d').date()
            while(max_date_date <= date_object):
                print(max_date_date, end="\n")
                fields.append(max_date_date)
                new_rows = [{'dates': max_date_date}]
                data = data.append(new_rows, ignore_index=True)
                max_date_date += delta
            data.to_csv('load_settings.csv',mode='a',index=False) 
    elif(date_to_compare == date_object):
        if(max_date == date_object):
            print("Already present in the csv")
    else:
        print("Error in checking the dates")


def new_function():
    data = pd.read_csv('load_settings.csv')
    today = datetime.datetime.today().date()

    # Default date to compare and to input if nothing exists
    date_to_compare = datetime.date(2023,1,1)
    
    fields = []

    # delta is 1 day
    delta = datetime.timedelta(days=1)
    
    # if the csv is empty, stop appending every row, just insert one row into the settings.csv
    if(data.shape[0] == 0):
        print("The load settings file is empty")
        fields.append(date_to_compare)
        new_rows = [{'dates': date_to_compare}]
        data = data.append(new_rows, ignore_index=True)
        data.to_csv('load_settings.csv',mode='w',index=False)    
        print(data)
    else:
        print("The load settings is not empty")
        # find out how to remove the existing row present in the excel
        fields.append(today)
        new_rows = [{'dates':today}]
        data = data.append(new_rows, ignore_index = True)
        data.to_csv('load_settings.csv',mode='w',index = False)
        print(data)

new_function()