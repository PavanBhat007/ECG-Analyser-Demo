def extract_form_data(req):
    name = req.form.get('name', '')
    gender = req.form.get('gender', '')
    age = req.form.get('age', '')

    gender = 0 if gender == 'Male' else 1
    
    if (not name or not gender or not age) and ('file' not in req.files):
        return 0

    else:
        return name, gender, age