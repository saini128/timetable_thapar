import pandas as pd


excel_file_path = 'timetable.xlsx'
sheet_name = '2ND YEAR B'  
df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=None)  

def extract_groups(df):
    desired_row_index = None
    for i, row in df.iterrows():
        if isinstance(row[0], str) and any(char.isdigit() for char in row[0]) and any(char.isalpha() for char in row[0]) and any(char == '-' for char in row[0]):
            desired_row_index = i
            break


    df = pd.read_excel(excel_file_path, sheet_name=sheet_name, header=desired_row_index)
    df = df.iloc[3:]

    group = df.loc[:, df.eq('2 CO 14').any()]
    classtime=df.loc[:, df.eq('HOURS').any()]


    for index, (group_value, classtime_value) in enumerate(zip(group.iterrows(), classtime.iterrows())):
        group_index, group_row = group_value
        classtime_index, classtime_row = classtime_value
        
        if not group_row.isnull().all()  and not classtime_row.values[1]=='HOURS':
            print(f"Row {index + 1}:")
            print(f"Group: {group_row.values[0]}")
            print(f"Class Time: {classtime_row.values[1]}")
            print()

    classgroup = None
    for col in df.columns[:df.columns.get_loc(group.columns[0])+1]:

        if any(isinstance(cell, str) and len(cell) == 8 and cell.endswith(' L') for cell in df[col]):
            classgroup = col

    print(f"Found column: {classgroup}")

    group=df[classgroup].to_frame()
    for index, (group_value, classtime_value) in enumerate(zip(group.iterrows(), classtime.iterrows())):
        group_index, group_row = group_value
        classtime_index, classtime_row = classtime_value
        
        if not group_row.isnull().all()  and not classtime_row.values[1]=='HOURS' and group_row.values[0].endswith(' L') and len(group_row.values[0]) == 8:
            print(f"Row {index + 1}:")
            print(f"Group: {group_row.values[0]}")
            print(f"Class Time: {classtime_row.values[1]}")
            instructor_column = None
            print(f"Column: {col}")
            group_index=group_index+1
            # df.to_csv('output_file.csv', index=False)
            for col in df.columns[df.columns.get_loc(group_index):]:
                print(f"value: { group_index,col}")
                if isinstance(df.at[group_index, col], str):
                    
                    # Keep moving forward until a non-null value is found
                    
                    instructor_column = col
                    
                    while pd.isnull(df.at[group_index, instructor_column]):
                        
                        instructor_column = df.columns[df.columns.get_loc(instructor_column) + 1]
                    print(f"value: { group_index,instructor_column}")
                    # Print the instructor name/code
                    print(f"Instructor: {df.at[group_index, instructor_column]}")
                    break
            print()

extract_groups(df)

