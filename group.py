import datetime
import pandas as pd
import json

excel_file_path = 'timetable.xlsx'
sheet_name = '2ND YEAR B'  
groupname='2 CO 3'
df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)  
def extract_groups(df):
    desired_row_index = None
    for i, row in df.iterrows():
        if isinstance(row[0], str) and any(char.isdigit() for char in row[0]) and any(char.isalpha() for char in row[0]) and any(char == '-' for char in row[0]):
            desired_row_index = i
            break


    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=desired_row_index)
    df = df.iloc[3:]

    group = df.loc[:, df.eq(groupname).any()]
    classtime=df.loc[:, df.eq('HOURS').any()]


    # for index, (group_value, classtime_value) in enumerate(zip(group.iterrows(), classtime.iterrows())):
    #     group_index, group_row = group_value
    #     classtime_index, classtime_row = classtime_value
        
    #     if not group_row.isnull().all()  and not classtime_row.values[1]=='HOURS':
    #         print(f"Row {index + 1}:")
    #         print(f"Group: {group_row.values[0]}")
    #         print(f"Class Time: {classtime_row.values[1]}")
    #         print()

    classgroup = None
    for col in df.columns[:df.columns.get_loc(group.columns[0])+1]:

        if any(isinstance(cell, str) and len(cell) == 8 and cell.endswith(' L') for cell in df[col]):
            classgroup = col

    print(f"Found column: {classgroup}")

    class_group=df[classgroup].to_frame()
    # for index, (class_group_value, classtime_value) in enumerate(zip(class_group.iterrows(), classtime.iterrows())):
    #     group_index, group_row = class_group_value
    #     classtime_index, classtime_row = classtime_value
        
    #     if not group_row.isnull().all()  and not classtime_row.values[1]=='HOURS' and (group_row.values[0].endswith(' L') or group_row.values[0]=='UTA026 P') and len(group_row.values[0]) == 8:
    #         print(f"Row {index + 1}:")
    #         print(f"Group: {group_row.values[0]}")
    #         print(f"Class Time: {classtime_row.values[1]}")
           
    #         print()
    if classgroup==df.columns.get_loc(group.columns[0]):
        print("They are same ",classgroup,df.columns.get_loc(group.columns[0]))
    else:
        print("not same ",classgroup,df.columns.get_loc(group.columns[0]))
        group_col_index = df.columns.get_loc(group.columns[0])

        # Iterate over the rows to fill empty cells in 'group' column
        class_group.reset_index(drop=True, inplace=True)
        for index, row in df.iterrows():
            if type(df.at[index, class_group.columns[0]])==str and (df.at[index, class_group.columns[0]].endswith(' L') or df.at[index, class_group.columns[0]]=='UTA026 P') :
                # Assuming 'classgroup' dataframe has the same index as 'df'
                df.at[index, group.columns[0]] = df.at[index, class_group.columns[0]]
                df.at[index+1, group.columns[0]] = df.at[index+1, class_group.columns[0]]
                # print(df.at[index, group.columns[0]],type(df.at[index, group.columns[0]]))
                # print(df.at[index+1, group.columns[0]],type(df.at[index+1, group.columns[0]]))

    group = df.loc[:, df.eq('2 CO 25').any()]
    days = []
    current_day = []
    specific_time = datetime.time(hour=8, minute=0, second=0)

    for index, (group_value, classtime_value) in enumerate(zip(group.iterrows(), classtime.iterrows())):
        group_index, group_row = group_value
        classtime_index, classtime_row = classtime_value
        
        if not group_row.isnull().all()  and not classtime_row.values[1]=='HOURS':
            if group_row.values[0].endswith(' L') or group_row.values[0].endswith(' P') or group_row.values[0].endswith(' T'):
                if classtime_row.values[1]<specific_time:
                    days.append(current_day)
                    current_day=[]
                current_day.append({"class":group_row.values[0],
                                    "time":str(classtime),
                                    "venue":"",
                                    })
                specific_time=classtime_row.values[1]
            elif current_day and current_day[-1]["venue"] == "":
                current_day[-1]["venue"] = group_row.values[0]

    days.append(current_day)
                
    # print(days)
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
            # Extract subject code and suffix
            subject_code = slot["class"].split()[0]
            suffix = slot["class"].split()[-1] if slot["class"].split()[-1] != "L" else ""

            # Replace subject code with name and reattach the suffix
            slot["class"] = str(mapping.get(subject_code, subject_code)["name"]) + " " + suffix
            modified_day.append(slot)

        json_structure[weekdays[index]] = modified_day

    return json_structure



group=extract_groups(df)
with open('subjects.json', 'r') as file:
    subject_mapping = json.load(file)
json_data = convert_to_json(group,subject_mapping)

json_string = json.dumps(json_data, indent=4)

with open(groupname+'file.json', 'w') as file:
    file.write(json_string)

print("Data saved to 'schedule.json'")