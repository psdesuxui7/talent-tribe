from flask import Flask, render_template, send_from_directory
import os
import threading

# Initialize Flask app
app = Flask(__name__)

# Route for app (Main Page)
@app.route('/')
def page1():
    return render_template('welcome.html')

# Route for serving the HTML page with 5 images in app
@app.route('/profile')
def image_page():
    return render_template('profile.html')

# Static file serving for images in the static folder
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

# Function to run the Flask app
def run_app():
    app.run(debug=True, host='0.0.0.0', port=8080, use_reloader=False)

if __name__ == '__main__':
    run_app()
