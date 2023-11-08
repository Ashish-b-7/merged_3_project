import pandas as pd
from flask import Flask, render_template, request, send_file
from flask import Blueprint, render_template

misc_app = Blueprint("misc_app", __name__)

@misc_app.route('/')
def index():
    return render_template('Misc_index.html')

@misc_app.route('/process_data', methods=['POST'])
def process_data():
    try:
        file = request.files['file']
        if file:
            df = pd.read_excel(file)

            agg_results = df.groupby(['Project', 'RV', 'Mapping Dates'])[' Hours'].agg(['sum']).reset_index()

            agg_results.columns = ['Project', 'RV', 'Mapping Dates', 'Total Hours']

            agg_results = agg_results['Project', 'Mapping Dates', 'RV', 'Total Hours']

            transformed_data = agg_results.pivot(index='Project', columns=['Mapping Dates', 'RV'], values='Total Hours').reset_index()

            writer = pd.ExcelWriter('transformed_results.xlsx')
            transformed_data.to_excel(writer, sheet_name='Transformed Results', index=True)
            writer.save()

            return 'Data processed and saved to transformed_results.xlsx'
        else:
            return 'No file provided.'
    except Exception as e:
        return f'An error occurred: {str(e)}'

@misc_app.route('/download')
def download():
    return send_file('transformed_results.xlsx', as_attachment=True)


