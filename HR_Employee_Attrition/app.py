from flask import Flask, render_template, send_file, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from sklearn.preprocessing import OneHotEncoder
from datetime import datetime
import pandas as pd
import pickle
import csv
import os

app = Flask(__name__)

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def nav():
    return render_template('nav.html')

@app.route('/home', methods=['GET', 'POST'])
def details():
    return render_template('index.html')

@app.route('/important_Attributes')
def Important_Attributes():
    image = [i for i in os.listdir('static/images') if i.endswith('.png')][1]
    return render_template('Important_Attributes.html', user_image = image)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return redirect(url_for(''))

inputfolder = os.path.join('static','input')
app.config['UPLOAD_FOLDER'] = inputfolder

def process_file(save_location):
    data = pd.read_csv(save_location)
    empName = data['Employee Name'].tolist()
    print(empName)
    data = data.drop('Employee Name', axis=1)
    dataset = pd.read_csv("HR_Model_Processed.csv")
    data = pd.get_dummies(data)
    data.to_csv("processed HR.csv")
    lr_from_pickle = pickle.load(open('model.pkl', 'rb'))
    with open('processed HR.csv') as file_obj:
        reader_obj = csv.reader(file_obj)
    # lr_from_pickle.predict(data)
    res = []
    res = lr_from_pickle.predict(data)
    df = pd.read_csv("processed HR.csv")
    empId = df['EmployeeNumber'].tolist()
    empIdList = []
    for id in empId:
        lst = []
        lst.append(id)
        empIdList.append(lst)
    print('Employee Details: ')
    print(empIdList)
    fields = ['Employee_Number']
    with open('new.csv', 'w') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(fields)
        print('Result')
        print(res)
        idx1 = 0
        for i in range(len(res)):
            if res[i] == 1:
                writer.writerow(empIdList[idx1])
            idx1 = idx1 + 1
        file.close()

@app.route('/upload', methods=['GET', 'POST'])
def upload():
        if request.method == 'POST':
            file = request.files['csvfile']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_location)
                process_file(save_location)
                return render_template('downloadDetails.html')
                
        return render_template('downloadDetails.html')
    
@app.route('/Download_file', methods=['GET', 'POST'])
def Download_file():
    path = "new.csv"
    return send_file(path, as_attachment=True)

@app.route('/attributes', methods=['GET', 'POST'])
def required_attributes():
    return render_template('requiredAttributes.html')

if __name__ == '__main__':
    app.run(debug=True)