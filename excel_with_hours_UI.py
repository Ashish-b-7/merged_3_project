import os
import pandas as pd
from flask import render_template, request, send_file
from flask import Blueprint, render_template
from flask import current_app


excel_app = Blueprint("excel_app", __name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')
    
UPLOAD_FOLDER = 'uploads'

@excel_app.route('/')
def index():
    return render_template('index.html')

@excel_app.route('/process_excel', methods=['POST'])
def process_excel():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    
   
    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith('.xlsx'):
        # Save the uploaded file
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        
        input_file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        df = pd.read_excel(input_file_path, usecols=['Project', 'Owner', ' Hours'])

        df.columns = ['Project', 'Owner', 'Hours']

        grouped = df.groupby(['Owner', 'Project'])['Hours'].sum().reset_index()

        total_hours_per_owner = grouped.groupby('Owner')['Hours'].sum().reset_index()

        grouped['Project_Hours'] = grouped.apply(lambda x: f"{x['Project']} ({x['Hours']} hours)", axis=1)

        result = grouped.groupby('Owner')['Project_Hours'].apply(list).reset_index()


        result = pd.merge(result, total_hours_per_owner, on='Owner')

        result.columns = ['Owner', 'Projects', 'Total Hours']

        output_file_name = f"output_{file.filename}"
        output_file_path = os.path.join(UPLOAD_FOLDER, output_file_name)

        # Save the result to the output Excel file
        with pd.ExcelWriter(output_file_path) as writer:
            result.to_excel(writer, sheet_name="TotalHoursPerProject", index=False)
        
        return send_file(output_file_path, as_attachment=True)
    else:
        return "Invalid file format. Please upload an Excel file."


