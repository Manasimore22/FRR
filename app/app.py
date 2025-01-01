# Importing essential libraries and modules
from flask import Flask, render_template, request, redirect
from markupsafe import Markup
import pandas as pd
import os

# Dictionary for fertilizer suggestions
from utils.fertilizer import fertilizer_dic

app = Flask(__name__)

@app.route('/')
def home():
    """Render the home page."""
    return render_template('index.html', title='KrishiSutra - Fertilizer Suggestion')


# Route for rendering fertilizer recommendation form
@app.route('/fertilizer')
def fertilizer_recommendation():
    title = 'KrishiSutra - Fertilizer Suggestion'
    return render_template('fertilizer.html', title=title)


# Route for fertilizer recommendation results
@app.route('/fertilizer-predict', methods=['POST'])
def fert_recommend():
    title = 'KrishiSutra - Fertilizer Suggestion'

    crop_name = str(request.form['cropname'])
    N = int(request.form['nitrogen'])
    P = int(request.form['phosphorous'])
    K = int(request.form['pottasium'])

    # Get the absolute path of the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))
    # Create the absolute path to the fertilizer.csv file
    file_path = os.path.join(current_directory, 'Data', 'fertilizer.csv')

    # Check if the file exists
    if not os.path.exists(file_path):
        return f"Error: {file_path} does not exist."

    # Read the fertilizer.csv file
    df = pd.read_csv(file_path)

    try:
        nr = df[df['Crop'] == crop_name]['N'].iloc[0]
        pr = df[df['Crop'] == crop_name]['P'].iloc[0]
        kr = df[df['Crop'] == crop_name]['K'].iloc[0]
    except IndexError:
        return f"Error: Crop '{crop_name}' not found in the database."

    n = nr - N
    p = pr - P
    k = kr - K
    temp = {abs(n): "N", abs(p): "P", abs(k): "K"}
    max_value = temp[max(temp.keys())]

    if max_value == "N":
        if n < 0:
            key = 'NHigh'
        else:
            key = "Nlow"
    elif max_value == "P":
        if p < 0:
            key = 'PHigh'
        else:
            key = "Plow"
    else:
        if k < 0:
            key = 'KHigh'
        else:
            key = "Klow"

    # Retrieve the recommendation from the dictionary
    response = Markup(str(fertilizer_dic[key]))

    return render_template('fertilizer-result.html', recommendation=response, title=title)

if __name__ == '__main__':
    app.run(debug=True)
