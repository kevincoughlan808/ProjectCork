# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 13:54:12 2021

@author: yea-b
"""
import os
import csv
from pathlib import Path
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime

# Function to read file into data frame and append a new data column
def open_file(file, script_dir):
    rel_path = "Glassdoor Data\\" + file
    abs_file_path = os.path.join(script_dir, rel_path)
    
    print(abs_file_path)
    
    with open(abs_file_path, newline='') as f:
        reader = csv.reader(f)
        
        data = list(reader)
        
        
        
    column_names = data[0]
    
    del data[0]
    
    file_name = file.replace(".csv", "")
    
    #data['Date'] = file_name
    return data, column_names, file_name



def remove_symbols(input_string):
    
    output_string = re.sub(r'\W+', '', input_string)
    
    return output_string


    
# Takes the infor from the current list and sorts it into the appropriate one
def organise_data(current_List, quick_facts_List, job_title_List, company_List, industry_List, timeseries_List):
    
    for elem in current_List:
        
        if elem[1] == 'Quick Facts':
            quick_facts_List.append(elem)
        elif elem[1] == 'Job Title':
            job_title_List.append(elem)
        elif elem[1] == 'Company Size':
            company_List.append(elem)
        elif elem[1] == 'Industry':
            industry_List.append(elem)
        elif elem[1] == 'Timeseries':
            timeseries_List.append(elem)

    return quick_facts_List, job_title_List, company_List, industry_List, timeseries_List



# Checks if new files have already been created if yes-> no need to sort data again
def check_for_files():
    control = False
    
    try:
        os.makedirs('sorted_data_files')
    except OSError as e:
        print(e)
        control = False
        
    try:
        files = os.listdir('sorted_data_files')
    except OSError as e:
        print(e)
        control = True
    
    if(len(files) > 0 ):
        control = True
    
    return control



def print_sorted_files(quick_facts_DF, job_title_DF, company_DF, industry_DF, timeseries_DF, script_dir):
    os.makedirs('sorted_data_files')
    
    rel_path = "sorted_data_files"
    abs_file_path = os.path.join(script_dir, rel_path)
    
    quick_facts_DF.to_csv(abs_file_path,'quick_facts.csv',index=False)
    job_title_DF.to_csv(abs_file_path,'job_title.csv',index=False)
    company_DF.to_csv(abs_file_path,'company.csv',index=False)
    industry_DF.to_csv(abs_file_path,'industry.csv',index=False)
    timeseries_DF.to_csv(abs_file_path,'timeseries.csv',index=False)



def trend_graph(df, col, var1):
    
    dates = sorted(df["Date"].unique(),reverse=False)
    
    places = sorted(df["Metro"].unique())
    
    for place in places:
        if(place != "National"):
            df_filter = df[(df["Metro"] == place) & (df[col] ==var1)]
        
            print(df_filter)

            rate = list(df_filter["Value"])
        
            index = 0 
            for elem in rate:
                elem = elem.replace("$", "")
                elem = elem.replace(" ", "")
                elem = elem.replace(",", "")
                elem = elem.replace("%", "")
            
                rate[index] = int(elem)
                index = index + 1
        
        
        
            sns.lineplot(x=dates, y=rate, label=place, linestyle='-')
        
    plt.ylabel(var1)
    plt.xlabel("Date")
    plt.title(var1)
    plt.legend(title="City",loc="upper left", bbox_to_anchor=(1.05, 1), fontsize='x-small')
    plt.show()
        
   
def main():
    script_dir = os.path.dirname(__file__)
    
    control = False #check_for_files()
    
    if (control == False):
    
        folder = os.listdir('Glassdoor Data')
        
        final_column_names = []
        
        quick_facts_List =    []
        job_title_List =      []
        company_List =        []
        industry_List =       []
        timeseries_List =     []
        
        print(folder)
        
        for file in folder:
            current_List, column_names, file_name = open_file(file, script_dir)
            
            column_names.append("Date")
            column_names[0] = remove_symbols(column_names[0])
            
            if(column_names[0] == "Metro"):
                final_column_names = column_names
            
            file_name = datetime.strptime(file_name, '%m-%Y')
            
            for elem in current_List:
                
                elem.append(file_name)
            
        
            quick_facts_List, job_title_List, company_List, industry_List, timeseries_List = organise_data(current_List, quick_facts_List, job_title_List, company_List, industry_List, timeseries_List)
        
        quick_facts_DF =    pd.DataFrame(quick_facts_List, columns=final_column_names)
        job_title_DF =      pd.DataFrame(job_title_List, columns=final_column_names)
        company_DF =        pd.DataFrame(company_List, columns=final_column_names)
        industry_DF =       pd.DataFrame(industry_List, columns=final_column_names)
        timeseries_DF =     pd.DataFrame(timeseries_List, columns=final_column_names)
        
        #print_sorted_files(quick_facts_DF, job_title_DF, company_DF, industry_DF, timeseries_DF, script_dir)
    
    #   Don't Work
    # try:
    #     trend_graph(quick_facts_DF, "Dimension", "Labor Force Size")
    # except:
    #     print("ERRROR ---- Graph not generated for: " + "Labor Force Size")
       
    # try:
    #     trend_graph(quick_facts_DF, "Dimension", "Total Employment")
    # except:
    #     print("ERRROR ---- Graph not generated for: " + "Total Employment")
        
    # try:
    #     trend_graph(quick_facts_DF, "Dimension", "Unemployment Rate")
    # except:
    #     print("ERRROR ---- Graph not generated for: " + "Unemployment Rate")
    
    #   Work
    trend_graph(quick_facts_DF, "Dimension", "Job Openings")
    trend_graph(quick_facts_DF, "Dimension", "Metro Median Pay")
    
    
    industries = sorted(industry_DF["Dimension"].unique())
    for industry in industries:
        trend_graph(industry_DF, "Dimension", industry)
    
        
if __name__ == '__main__':
    main()