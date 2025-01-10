def extract_form_data(req):
    name = req.form.get('name', '')
    gender = req.form.get('gender', '')
    age = req.form.get('age', '')

    gender = 0 if gender == 'Male' else 1
    
    if (not name or not gender or not age) and ('file' not in req.files):
        return 0

    else:
        return name, gender, age
    
    
def update_col_names(params):
    temp_dict = {
        'Average Heart Rate': params['avg_heart_rate'],
        'Mean of RR Intervals': params['mean_rr'],
        'Standard Deviation of RR Intervals': params['std_rr'],
        'SDNN': params['sdnn'],
        'SDNN Index': params['sdnni'],
        'RMSSD': params['rmssd'],
        'HRV Triangular Index': params['hrv_triangular_index'],
        'TINN': params['tinn'],
        'Low Frequency Power': params['lf_power'],
        'High Frequency Power': params['hf_power'],
        'LF/HF Ratio': params['lf_hf_ratio'],
        'SD1': params['sd1'],
        'SD2': params['sd2']
    }
    
    return temp_dict