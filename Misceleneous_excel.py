import pandas as pd
from flask import Flask, render_template, request, send_file
from flask import Blueprint, render_template
import os

misc_app = Blueprint("misc_app", __name__)

if not os.path.exists('uploads'):
    os.makedirs('uploads')

UPLOAD_FOLDER = 'uploads'

@misc_app.route('/')
def index():
    return render_template('Misc_index.html')

@misc_app.route('/process_excel', methods=['POST'])
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

        # Use 'Hours' if present, otherwise use ' Hours'
        column_name = 'Hours' if 'Hours' in pd.read_excel(input_file_path, nrows=1).columns else ' Hours'
        df = pd.read_excel(input_file_path, usecols=['Project', 'RV', 'Mapping Dates', column_name])

        res = df.groupby(['Project', 'RV', 'Mapping Dates'])[column_name].sum().reset_index()

        columns_order = ['Project', 'Mapping Dates', 'RV', column_name]

        transformed_data = res.pivot_table(index='Project', columns=['Mapping Dates', 'RV'], values=column_name, fill_value=0).reset_index()

        output_file_name = f"output_{file.filename}"
        output_file_path = os.path.join(UPLOAD_FOLDER, output_file_name)

        # Save the result to the output Excel file
        with pd.ExcelWriter(output_file_path) as writer:
            transformed_data.to_excel(writer, sheet_name="Transform_Results", index=True)
        
        return send_file(output_file_path, as_attachment=True)
    else:
        return "Invalid file format. Please upload an Excel file."
