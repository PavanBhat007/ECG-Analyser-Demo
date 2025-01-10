import os
from flask import Flask, render_template, request, redirect, url_for, flash

from paramex import extract_ecg_features
from predict import predict
from utils import extract_form_data

app = Flask(__name__)
app.secret_key = "JNBPRKS"
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = {'adicht'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    name, sex, age = extract_form_data(request)

    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        file_info, params = extract_ecg_features(filepath)
        params["age"] = age
        params["sex"] = sex
        
        prediction = predict(params)
        prediction = "Normal" if prediction == 0 else "Specimen"
        
        try:
            return render_template(
                'report.html',
                name=name,
                gender=sex,
                age=age,
                file_info=file_info,
                parameters=params,
                pred=prediction
            )
            
        except Exception as e:
            flash(f"Error processing file: {e}")
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an .adicht file.')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')