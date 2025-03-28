import time
import os
import threading
import py532lib
import requests  # Import the requests library to make HTTP requests
import webbrowser
from flask import Flask, render_template, send_from_directory
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *

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

# Initialize PN532 NFC reader
pn532 = Pn532_i2c()
pn532.SAMconfigure()

# Define the target byte arrays to match
target_byte_arrays = [
    bytearray(b'K\x01\x01\x03D \x07\x04\x80T\xb2en\x80\x06uw\x81\x02\x80'),
    bytearray(b'K\x01\x01\x03D \x07\x04Q\x82\x9a6u\x80\x06uw\x81\x02\x80'),
    bytearray(b'K\x01\x01\x03D \x07\x04\x11PB:u\x80\x06uw\x81\x02\x80')
]

# Function to read the NFC card
def read_nfc_card():
    try:
        card_data = pn532.read_mifare().get_data()
        print(f"Read data from card: {card_data}")
        return card_data
    except Exception as e:
        print(f"Error reading from card: {e}")
        return None

# Function to check if the card data matches any of the target byte arrays
def check_byte_array_and_open_page(data):
    if data in target_byte_arrays:
        print("Byte array matched! Sending request to Flask server...")
        # Send a GET request to the Flask server to navigate to the profile page
        try: 
            webbrowser.open('http://127.0.0.1:8080/profile')
        except Exception as e:
            print(f"Error connecting to Flask server: {e}")
    else:
        print("No match found for the byte array.")

# Function to handle NFC reading and check for matches
def nfc_reader():
    while True:
        print("Place NFC card near the reader...")

        # Read the NFC card
        nfc_data = read_nfc_card()

        if nfc_data:
            # Check if the byte array matches any of the target byte arrays
            check_byte_array_and_open_page(nfc_data)

        # Wait for a while before reading again
        time.sleep(2)  # Adjust sleep time as needed

# Main function to run the Flask app and NFC reader
if __name__ == "__main__":
    # Start the Flask app in a separate thread
    flask_thread = threading.Thread(target=run_app)
    flask_thread.daemon = True  # Allow the thread to exit when the main program exits
    flask_thread.start()

    # Start the NFC reader
    nfc_reader()
