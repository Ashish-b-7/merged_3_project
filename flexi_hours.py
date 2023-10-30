from flask import Flask, render_template, request, send_file
import re
import pdfplumber
import pandas as pd
import io
from flask import Blueprint, render_template
flexi_app = Blueprint("flexi_app", __name__)

@flexi_app.route('/')
def index():
    return render_template('upload.html')

@flexi_app.route('/process', methods=['POST'])
def process_pdf():
    if 'pdf_file' not in request.files:
        return "No file part"

    pdf_file = request.files['pdf_file']

    if pdf_file.filename == '':
        return "No selected file"

    try:
        pdf_content = pdf_file.read()

        with io.BytesIO(pdf_content) as pdf_file:
            extracted_text = ""
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    extracted_text += page.extract_text()

            blocks = re.split(r"(\d+\s+\w+\s+\w+\s+Branch\s+:.*?Department\s+:\s+.*)", extracted_text)[1:]

            current_id = None
            current_name = None
            current_branch = None
            current_department = None
            time_list = []

            extracted_data = []

            for block in blocks:
                match = re.search(r"(\d+)\s+(.*?)\s+Branch\s+:\s+(.*?)\s+Department\s+:\s+(.*)", block)

                if match:
                    if current_id is not None:
                        time_list = filter_unwanted_values(time_list)
                        if time_list:
                            extracted_data.append([current_id, current_name, current_branch, current_department, time_list])
                        time_list = []

                    current_id = match.group(1)
                    current_name = match.group(2)
                    current_branch = match.group(3)
                    current_department = match.group(4)

                time_pattern = r"(\d+\.\d+)"
                time_matches = re.findall(time_pattern, block)
                time_values = [float(time) for time in time_matches if 0 <= float(time) <= 24]
                time_list.extend(time_values)

            if current_id is not None:
                time_list = filter_unwanted_values(time_list)
                if time_list:
                    extracted_data.append([current_id, current_name, current_branch, current_department, time_list])

            extracted_data_df = pd.DataFrame(extracted_data, columns=['ID', 'Name', 'Branch', 'Department', 'Time List'])

            extracted_data_df['Total Time'] = extracted_data_df['Time List'].apply(lambda x: round(sum(x), 2))

            # Save the data to Excel with the desired filename
            excel_filename = 'flexi_hours.xlsx'
            extracted_data_df.to_excel(excel_filename, index=False)

            result_html = extracted_data_df.to_html(classes='table table-bordered table-striped')

            # Provide a link to download the Excel file
            return f"Processing complete. Results have been saved. <a href='/flexi/download'>Download Excel</a>.<br>{result_html}"

    except Exception as e:
        return f"An error occurred: {str(e)}"

@flexi_app.route('/download')
def download_excel():
    excel_filename = 'flexi_hours.xlsx'
    return send_file(excel_filename, as_attachment=True)

# Function to remove unwanted values ('6.3', '10.0', '10.3', '0.5', '0.0') from the time list
def filter_unwanted_values(time_list):
    cleaned_time_list = []
    prev_value = None

    unwanted_values = [9.3, 6.3, 6.0, 10.0, 10.3, 7.0, 0.17, 0.5, 0.0]

    for time in time_list:
        if time not in unwanted_values:
            if time != prev_value:
                cleaned_time_list.append(time)
            prev_value = time

    return cleaned_time_list


