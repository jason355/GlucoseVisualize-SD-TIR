import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import datetime 
import os
csv_path = f'../data/{datetime.datetime.today().strftime("%Y%m%d")}'

today = datetime.datetime.today().date()
startDay = today - datetime.timedelta(days=90)


saving_folder = f"../data/image/{startDay}-{today}"
if not os.path.exists(saving_folder):
    os.makedirs(saving_folder)
    print(f"Folder '{saving_folder}' created successfully.")
else:
        print(f"Folder '{saving_folder}' already exists.")

def read_csv(csv_path, delimiter=";", header = None, names = None):
    single = []
    data = []
    try:
        with open(csv_path, "r") as f:
            for line in f.readlines():
                # print(f"line repr:{repr(line)}")
                cleaned_line = line.replace("\x00", '')
                sequence = cleaned_line.split(';')
                single = [item for i, item in enumerate(sequence) if i in [1,6, 9]]
                if single != [] :
                    data.append(single)
                # print(f"data: {data}")
            return data
        # df = pd.read_csv(csv_path, delimiter=delimiter, header=header, names = names)
        # print(f"CSV file read successfully: \n {df.head()}")
        # return df
    except Exception as e:
        print(f'Error reading CSV file: {e}')
        return None
    
# 移除新CGM前8筆資料
def remove_inaccurate_data(data):
    serial = data[0][2]
    toRemove = []
    for index,single in enumerate(data):
        if single[2] != serial and " " not in single[2]:
            # print(f"remove start from : {single}")
            serial = single[2]
            toRemove.extend(range(index, index + 8))
    data = [single for i, single in enumerate(data) if i not in toRemove]
    return data

def date_select(data, date):
    temp = []
    for single in data:
        if date in single[0]:
            temp.append(single)
            # print(single)
    return temp


def separate_datetime_column(data):
    originalFormat = "%d/%m/%Y %H.%M.%S"
    dateFormat = "%d/%m/%Y"
    timeFormat = "%H.%M"
    newData = []
    for single in data:
        original = single[0]

        dateObj = datetime.datetime.strptime(original, originalFormat).strftime(dateFormat)
        timeObj = datetime.datetime.strptime(original, originalFormat).strftime(timeFormat)

        newData.append([dateObj, float(timeObj), int(single[1]), single[2]])
    return newData

def three_month():
    today = datetime.datetime.today().date()
    startDay = today - datetime.timedelta(days=90)
    dateList = []
    current_day = today
    while current_day >= startDay:
        dateList.append(current_day.strftime("%d/%m/%Y"))
        current_day -= datetime.timedelta(days=1)
    return dateList

def get_three_month_data(data):
    dateList = three_month()
    newData = []
    for single in data:
        if single[0] in dateList:
            newData.append(single)
    return newData

def glucose_per_day(data):
    MaxGlucose = 0
    
    plt.figure(figsize=(10, 6))  # Optional: set the figure size

    dateList = three_month()
    for date in dateList:
        oneDayData = date_select(data,date)
        if not oneDayData:
            continue
        
        time = [single[1] for single in oneDayData]
        glucose = [single[2] for single in oneDayData]
        MaxGlucose = max(glucose + [MaxGlucose])
        plt.plot(time, glucose, linestyle='-')  # Plotting the line chart

    # Plotting the data
    plt.xlim(0, 23.59)
    plt.ylim(0, MaxGlucose+20)
    plt.title('Glucose Levels Over Time')  # Adding a title
    plt.xlabel('Time')  # Adding X-axis label
    plt.ylabel('Glucose Level')  # Adding Y-axis label
    plt.grid(True)  # Optional: add gridlines
    plt.gca().yaxis.set_major_locator(MultipleLocator(50))  # Set major ticks every 5 units
    plt.gca().xaxis.set_major_locator(MultipleLocator(1))  # Set major ticks every 5 units

    plt.legend()  # Adding a legend
    plt.tight_layout()  # Optional: improve layout

    # Display the plot
    plt.savefig(f'{saving_folder}/Glucose Levels Over Time', dpi=500)


def save_text_data(data):
    with open(f"{saving_folder}/data.txt", 'w') as file:
        for sublist in data:
            file.write(str(sublist) + '\n')

    print(f"Data written to {saving_folder}")



def get_hour_percentage(data, method):
    data = get_three_month_data(data)
    sortedData = sorted(data, key=lambda x: x[1])
    print(sortedData[:5])
    # with open(f"{saving_folder}/hour_sorted_data.txt", "a+") as f:
    #     f.write("sorted:\n")
    #     for sublist in sortedData:
    #         f.write(str(sublist) + '\n')
    index = -1
    total = []
    levels = []
    average = []
    for hour in range(0, 24):
        count = 0
        GlucoseSum = 0
        extremeHigh = 0
        High = 0
        Intarget = 0
        Low = 0
        extremeLow = 0
        for data in sortedData:
            if int(data[1]) == hour:
                index += 1
                count += 1
                GlucoseSum += data[2]
                if data[2] >= 250:
                    extremeHigh += 1
                elif data[2] >= 180 and data[2] < 250:
                    High += 1
                elif data[2] >= 70 and data[2] < 180:
                    Intarget += 1
                elif data[2] >= 50 and data[2] < 70:
                    Low += 1
                else:
                    extremeLow += 1
            else:
                break
        if count != 0:
            level = [(extremeHigh/count)*100,(High/count)*100,(Intarget/count)*100,(Low/count)*100,(extremeLow/count)*100]
            total.append(count)
            levels.append(level)
            average.append(GlucoseSum/count)
        else:
            level = [0,0,0,0]
            total.append(0)
            levels.append(level)
            average.append(0)

        sortedData = sortedData[index+1:]
        # print(f"len:{len(sortedData)}, index :{index}")
        index = -1
    # print(f"total:{total}")
    # print(f"levels:{levels}")
    # print(f"average:{average}")
    
    # with open(f"{saving_folder}/hour_sorted_data.txt", "a+") as f:
    #     f.write("\nTotal:\n")
    #     for sublist in total:
    #         f.write(str(sublist) + '\n')
    #     f.write("Levels:\n")
    #     for sublist in levels:
    #         f.write(str(sublist) + '\n')
    #     f.write("Average:\n")
    #     for sublist in average:
    #         f.write(str(sublist) + '\n')


    if method == "avg":
        return average
    else:
        return levels
    

# seperate levels in to extremeLow Low Intarget High extremeHigh
def seperate_levels(data):

    levels = get_hour_percentage(data, "levels")

    EL = []
    L = []
    I = []
    H = []
    EH = []

    for item in levels:
        EL.append(item[4])
        L.append(item[3])
        I.append(item[2])
        H.append(item[1])
        EH.append(item[0])

    EL = np.array(EL)
    L = np.array(L)
    I = np.array(I)
    H = np.array(H)
    EH = np.array(EH)

    plt.figure(figsize=(12,8))

    x = list(range(0,24, 1))
    

    plt.bar(x, EL,label="extremeLow", color = "#fa1d0d", width=0.75)
    plt.bar(x, L,label="Low", bottom=EL, color = "#f8948d", width=0.75)
    plt.bar(x, I,label="Intartget", bottom=EL+L, color = "#21bf30", width=0.75)
    plt.bar(x, H,label="High", bottom=EL+L+I, color = "#f29d62", width=0.75)
    plt.bar(x, EH,label="extremeHigh", bottom=EL+L+I+H, color = "#f78400", width=0.75)

    for xpos, ypos, yval in zip(x, EL/2, EL):
        plt.text(xpos, ypos, "%.1f"%yval, ha="center", va="center")
    for xpos, ypos, yval in zip(x, EL+L/2, L):
        plt.text(xpos, ypos, "%.1f"%yval, ha="center", va="center")
    for xpos, ypos, yval in zip(x, EL+L+I/2, I):
        plt.text(xpos, ypos, "%.1f"%yval, ha="center", va="center")
    for xpos, ypos, yval in zip(x, EL+L+I+H/2, H):
        plt.text(xpos, ypos, "%.1f"%yval, ha="center", va="center")
    for xpos, ypos, yval in zip(x, EL+L+I+H+EH/2, EH):
        plt.text(xpos, ypos, "%.1f"%yval, ha="center", va="center")


    plt.xlim(-1,24)
    plt.ylim(0,110)
    plt.gca().xaxis.set_major_locator(MultipleLocator(1))  # Set major ticks every 5 units
    plt.xlabel('Hours')
    plt.ylabel('Percentage')
    plt.title(f'Hourly Glucose Levels {datetime.datetime.today().date() - datetime.timedelta(days=90)} - {datetime.datetime.today().date()} ')
    plt.legend()
    
    # plt.text(0.5, 1.5, f'Notes: Data range: {len(data)}, start: {datetime.datetime.today().date() - datetime.timedelta(days=90)}, end:{datetime.datetime.today().date()}', horizontalalignment='center', verticalalignment='center', transform=plt.gca().transAxes)

    plt.tight_layout()


    plt.savefig(f'{saving_folder}/percentage per hour ', dpi=500)


def standard_day(data):
    average = get_hour_percentage(data, "avg")


    # print(average)
    plt.figure(figsize=(8,6))
    x = list(range(0, 24))
    plt.plot(x, average, linestyle='-')  # Plotting the line chart
    plt.ylim(20, max(average)+30)
    plt.title('Avreage Glucose Levels per hour')  # Adding a title
    plt.xlabel('Time')  # Adding X-axis label
    plt.ylabel('Glucose Level')  # Adding Y-axis label
    plt.grid(True)  # Optional: add gridlines
    plt.gca().yaxis.set_major_locator(MultipleLocator(50))  # Set major ticks every 5 units
    plt.gca().xaxis.set_major_locator(MultipleLocator(1))  # Set major ticks every 5 units

    plt.legend()  # Adding a legend
    plt.tight_layout()  # Optional: improve layout

    # Display the plot
    plt.savefig(f'{saving_folder}/average glucose every hour line chart', dpi=500)





