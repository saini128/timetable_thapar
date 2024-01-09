import datetime
from time import sleep
import pandas as pd
import json

excel_file_path = 'timetable.xlsx'



def extract_groups(df,groupname):
    desired_row_index = None
    for i, row in df.iterrows():
        if isinstance(row[0], str) and any(char.isdigit() for char in row[0]) and any(char.isalpha() for char in row[0]) and any(char == '-' for char in row[0]):
            desired_row_index = i
            break

    group = df.loc[:, df.eq(groupname).any()]
    classtime=df.loc[:, df.eq('HOURS').any()]

    classgroup = None
    for col in df.columns[:df.columns.get_loc(group.columns[0])+1]:

        if any(isinstance(cell, str) and len(cell) == 8 and cell.endswith(' L') for cell in df[col]):
            classgroup = col

    print(f"Found column: {classgroup}")

    class_group=df[classgroup].to_frame()

    if classgroup==df.columns.get_loc(group.columns[0]):
        print("They are same ",classgroup,df.columns.get_loc(group.columns[0]))
    else:
        print("not same ",classgroup,df.columns.get_loc(group.columns[0]))
        group_col_index = df.columns.get_loc(group.columns[0])

        
        class_group.reset_index(drop=True, inplace=True)
        for index, row in df.iterrows():
            if type(df.at[index, class_group.columns[0]])==str and (df.at[index, class_group.columns[0]].endswith(' L') or df.at[index, class_group.columns[0]]=='UTA026 P') :
                
                df.at[index, group.columns[0]] = df.at[index, class_group.columns[0]]
                df.at[index+1, group.columns[0]] = df.at[index+1, class_group.columns[0]]
                
                

    group = df.loc[:, df.eq(groupname).any()]
    days = []
    current_day = []
    specific_time = datetime.time(hour=8, minute=0, second=0)

    for index, (group_value, classtime_value) in enumerate(zip(group.iterrows(), classtime.iterrows())):
        group_index, group_row = group_value
        classtime_index, classtime_row = classtime_value
        
        if not group_row.isnull().all()  and not classtime_row.values[1]=='HOURS':
            if group_row.values[0].endswith(' L') or group_row.values[0].endswith(' P') or group_row.values[0].endswith(' T'):
                print(type(classtime_row.values[1]),classtime_row.values[1],type(specific_time),specific_time)
                if type(classtime_row.values[1]) == str:
                    classtime = datetime.datetime.strptime(classtime_row.values[1], '%I:%M: %p').time()
                if classtime<specific_time:
                    days.append(current_day)
                    current_day=[]
                current_day.append({"class":group_row.values[0],
                                    "time":str(classtime_row.values[1]),
                                    "venue":"",
                                    })
                specific_time=classtime
            elif current_day and current_day[-1]["venue"] == "":
                current_day[-1]["venue"] = group_row.values[0]

    days.append(current_day)
                
    
    print(len(days))
    for data in days:
        print(data)
    return days
import json 
def convert_to_json(days, mapping):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    json_structure = {}

    for index, day in enumerate(days):
        modified_day = []
        for slot in day:
            
            subject_code = slot["class"].split()[0]
            suffix = slot["class"].split()[-1]
            print(subject_code)
            try:
                slot["class"] = str(mapping.get(subject_code, subject_code)["name"]) + " " + suffix
            except:
                slot["class"] = subject_code + " " + suffix

            modified_day.append(slot)

        json_structure[weekdays[index]] = modified_day

    return json_structure


with open('subjects.json', 'r') as file:
    subject_mapping = json.load(file)

xl = pd.ExcelFile(excel_file_path)
for sheet_name in xl.sheet_names:
    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)

    
    day_rows = df[df.apply(lambda row: row.astype(str).str.contains('DAY').any(), axis=1)]

    for day_row in day_rows.iterrows():
        index, row = day_row
        group_names = row[row.str.match(r'^\d+.*$', na=False)]
        
        for groupname in group_names:
            print(f"Processing sheet: {sheet_name}, Group Name: {groupname}")

            
            df_group = df.iloc[index:].reset_index(drop=True)
            group = extract_groups(df_group, groupname)
            json_data = convert_to_json(group, subject_mapping)

            json_string = json.dumps(json_data, indent=4)

            with open(f"{groupname}.json", 'w') as file:
                file.write(json_string)

            print(f"Data saved to '{groupname}.json'")
            sleep(5)