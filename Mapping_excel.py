from flask import Blueprint, render_template
import os
from flask import Flask, render_template, request, send_file
import pandas as pd
import re

mapping_app = Blueprint("mapping_app", __name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

UPLOAD_FOLDER = 'uploads'

def process_files(normal_file_path, mapping_file_path,filename):
    Upload_file = pd.read_excel(normal_file_path)
    Mapping_file = pd.read_excel(mapping_file_path, sheet_name=None)

    sheet1_data = Mapping_file['Sheet1']
    sheet2_data = Mapping_file['Sheet2']
    sheet3_data = Mapping_file['Sheet3']

    merged_data1 = Upload_file.merge(sheet1_data, on='Project', how='left')
    merged_data1['Log Description'] = merged_data1['Log Description'].fillna('')

    condition = (merged_data1['Project'].str.lower() == 'pathquest - ap')
    merged_data1.loc[condition, 'Productive/Non Productive'] = 'Productive'
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Billable'
    merged_data1.loc[condition, 'Billing Head'] = 'PQ'
    
    condition = (merged_data1['Project'].str.lower() == 'pathquest ap')
    merged_data1.loc[condition, 'Productive/Non Productive'] = 'Productive'
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Billable'
    merged_data1.loc[condition, 'Billing Head'] = 'PQ'

    condition = (merged_data1['Project'].str.lower() == 'pathquest - bi')
    merged_data1.loc[condition, 'Productive/Non Productive'] = 'Productive'
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Billable'
    merged_data1.loc[condition, 'Billing Head'] = 'PQ'

    condition = (merged_data1['Project'].str.lower() == 'pathquest bi')
    merged_data1.loc[condition, 'Productive/Non Productive'] = 'Productive'
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Billable'
    merged_data1.loc[condition, 'Billing Head'] = 'PQ'

    condition = (merged_data1['Item Type'] == 'Bug')
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Non Billable'

    condition = (merged_data1['Item Type'] == 'Defects')
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Non Billable'

    # Define regular expression pattern to match variations of 'issue'
    pattern = re.compile(r'issue[\/,]*', flags=re.IGNORECASE)
    
    # Use the pattern to find matching rows in 'Log Description' column
    condition = merged_data1['Log Description'].str.contains(pattern)

    # Update 'Billable/Non Billable' for matching rows
    merged_data1.loc[condition, 'Billable/Non Billable'] = 'Non Billable'
    
    # Define regular expression patterns for different terms
    pattern1 = re.compile(r'R&R[\/,]*', flags=re.IGNORECASE)
    pattern2 = re.compile(r'Celebration[\/,]*', flags=re.IGNORECASE)
    pattern3 = re.compile(r'HRMS[\/,]*', flags=re.IGNORECASE)
    pattern4 = re.compile(r'Activity[\/,]*', flags=re.IGNORECASE)
    pattern5 = re.compile(r'Birthday[\/,]*', flags=re.IGNORECASE)
    pattern6 = re.compile(r'Game[\/,]*', flags=re.IGNORECASE)
    pattern7 = re.compile(r'KRA[\/,]*', flags=re.IGNORECASE)
    pattern8 = re.compile(r'Training[\/,]*', flags=re.IGNORECASE)
    pattern9 = re.compile(r'KT[\/,]*', flags=re.IGNORECASE)
    pattern10 = re.compile(r'Learning[\/,]*', flags=re.IGNORECASE)
    pattern11 = re.compile(r'Interview[\/,]*', flags=re.IGNORECASE)
    pattern12 = re.compile(r'Practical[\/,]*', flags=re.IGNORECASE)
    pattern13 = re.compile(r'Bugs[\/,]*', flags=re.IGNORECASE)
    pattern14 = re.compile(r'R&D[\/,]*', flags=re.IGNORECASE)
    
    merged_data1['Log Description'] = merged_data1['Log Description'].fillna('')
    
    # Use the patterns to find matching rows in 'Log Description' column
    condition1 = merged_data1['Log Description'].str.contains(pattern1)
    condition2 = merged_data1['Log Description'].str.contains(pattern2)
    condition3 = merged_data1['Log Description'].str.contains(pattern3)
    condition4 = merged_data1['Log Description'].str.contains(pattern4)
    condition5 = merged_data1['Log Description'].str.contains(pattern5)
    condition6 = merged_data1['Log Description'].str.contains(pattern6)
    condition7 = merged_data1['Log Description'].str.contains(pattern7)
    condition8 = merged_data1['Log Description'].str.contains(pattern8)
    condition9 = merged_data1['Log Description'].str.contains(pattern9)
    condition10 = merged_data1['Log Description'].str.contains(pattern10)
    condition11 = merged_data1['Log Description'].str.contains(pattern11)
    condition12 = merged_data1['Log Description'].str.contains(pattern12)
    condition13 = merged_data1['Log Description'].str.contains(pattern13)
    condition14 = merged_data1['Log Description'].str.contains(pattern14)

    # Update 'Productive/Non Productive', 'Billable/Non Billable', and 'Billing Head' for matching rows
    merged_data1.loc[condition1, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Non Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition2, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Non Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition3, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Non Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition4, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Non Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition5, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Non Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition6, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Non Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition7, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition8, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition9, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition10, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition11, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition12, ['Productive/Non Productive', 'Billable/Non Billable', 'Billing Head']] = ['Productive', 'Non Billable', 'Internal']
    merged_data1.loc[condition13, ['Productive/Non Productive', 'Billable/Non Billable']] = ['Productive', 'Non Billable']
    merged_data1.loc[condition14, ['Productive/Non Productive', 'Billable/Non Billable']] = ['Productive', 'Non Billable']


    merged_data2 = merged_data1.merge(sheet2_data, on='Log Date', how='left')
    merged_data3 = merged_data2.merge(sheet3_data, on='Owner', how='left')

    #Save the merged data to a new Excel file
    output_path = os.path.join(UPLOAD_FOLDER, filename)
    merged_data3.to_excel(output_path, index=False)
    return output_path

@mapping_app.route('/', methods=['GET'])
def index():
    return render_template('button.html')

@mapping_app.route('/upload', methods=['POST'])
@mapping_app.route('/upload', methods=['POST'])
def upload():

    normal_file = request.files['normal_file']
    mapping_file = request.files['mapping_file']
    # print(normal_file)
    # exit()
    normal_file_path = os.path.join(UPLOAD_FOLDER, 'normal_file.xlsx')
    mapping_file_path = os.path.join(UPLOAD_FOLDER, 'mapping_file.xlsx')

    normal_file.save(normal_file_path)
    mapping_file.save(mapping_file_path)

    output_path = process_files(normal_file_path, mapping_file_path,normal_file.filename)

    return send_file(output_path, as_attachment=True)
