# ECG-Analyser-Demo
Basic project demo for an ECG analyzer that takes .adicht ECG file as input, and displays ECG features and a prediction if the ECG is normal (Sinus Rhythm) or is specimen (has arrhythmias)

## Installing libraries
1. Open a terminal in the root level of the project directory.
2. Install required libraries using `pip install -r requirements.txt`

## Setting environment variables
1. `set FLASK_APP=app.py`
2. `set FLASK_ENV=development`

## Running the application
1. Run the flask app using `flask run`
2. Ctrl+Click in the URL. The app will run on localhost in the browser.

## Usage
1. Enter the user details -> name, age, gender.
2. Upload the ECG file. It must be a LabChart file having the extension `.adicht`.
3. Click submit, and the analysis report will be displayed.