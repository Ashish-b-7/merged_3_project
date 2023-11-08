from flask import Flask, render_template
from Mapping_excel import mapping_app
from excel_with_hours_UI import excel_app
from flexi_hours import flexi_app
from Misceleneous_excel import misc_app

app = Flask(__name__)

# Set the UPLOAD_FOLDER configuration for the main app (Flask instance)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Register the Blueprints and pass the app configuration
app.register_blueprint(mapping_app, url_prefix='/mapping')
app.register_blueprint(excel_app, url_prefix='/excel')
app.register_blueprint(flexi_app, url_prefix='/flexi')
app.register_blueprint(misc_app,url_prefix='/misc')
@app.route('/')
def main_home():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True)
