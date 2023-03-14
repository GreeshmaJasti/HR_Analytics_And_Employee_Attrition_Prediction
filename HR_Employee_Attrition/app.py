from flask import Flask, render_template, send_file, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
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

@app.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template('nav.html')

@app.route('/back', methods=['GET', 'POST'])
def back():
    return render_template('choose.html')

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

def process_file(save_location, empID):
    data = pd.read_csv(save_location)
    empName = data['EmployeeName'].tolist()
    empNameList = []
    for name in empName:
        lst=[]
        lst.append(name)
        empNameList.append(lst)
    Age = data['Age'].tolist()
    DailyRate = data['DailyRate'].tolist()
    DistanceFromHome = data['DistanceFromHome'].tolist()
    HourlyRate = data['HourlyRate'].tolist()
    MonthlyIncome = data['MonthlyIncome'].tolist()
    MonthlyRate = data['MonthlyRate'].tolist()
    NumCompaniesWorked = data['NumCompaniesWorked'].tolist()
    PercentSalaryHike = data['PercentSalaryHike'].tolist()
    PerformanceRating = data['PerformanceRating'].tolist()
    TotalWorkingYears = data['TotalWorkingYears'].tolist()
    WorkLifeBalance = data['WorkLifeBalance'].tolist()
    YearsAtCompany = data['YearsAtCompany'].tolist()
    YearsInCurrentRole = data['YearsInCurrentRole'].tolist()
    YearsSinceLastPromotion = data['YearsSinceLastPromotion'].tolist()
    YearsWithCurrManager = data['YearsWithCurrManager'].tolist()
    print(empNameList)
    if empID == '':
        data = data.drop('EmployeeName', axis=1)
        # dataset = pd.read_csv("HR_Model_Processed.csv")
        data = pd.get_dummies(data)
        data.to_csv("processed HR.csv")
        lr_from_pickle = pickle.load(open('model.pkl', 'rb'))
        with open('processed HR.csv') as file_obj:
            reader_obj = csv.reader(file_obj)
        res = []
        res = lr_from_pickle.predict(data)
        df = pd.read_csv("processed HR.csv")
        empId = df['EmployeeNumber'].tolist()
        #preparing list of lists of employee IDs
        empIdList = []
        for id in empId:
            lst = []
            lst.append(id)
            empIdList.append(lst)
        print('Employee Details: ')
        print(empIdList)
        print('Employee Names: ')
        print(empNameList)
        with open('Employee_Details.csv', 'w', newline='') as csvfile:
            header = ['Employee_Number','Employee_Name','Attrition(Stay/Leave)', 'TimeSpan']
            writer = csv.DictWriter(csvfile, fieldnames=header)
            writer.writeheader()
            print('Result')
            print(res)
            idx1 = 0
            for item in res:
                model1 = pickle.load(open('model1.pkl', 'rb'))
                x1 = pd.DataFrame({"Age": [Age[idx1]], "DailyRate": [DailyRate[idx1]], "DistanceFromHome":[DistanceFromHome[idx1]], "HourlyRate":[HourlyRate[idx1]],"MonthlyIncome":[MonthlyIncome[idx1]],"MonthlyRate":[MonthlyRate[idx1]],"NumCompaniesWorked":[NumCompaniesWorked[idx1]], "PercentSalaryHike":[PercentSalaryHike[idx1]],
                "PerformanceRating":[PerformanceRating[idx1]],"TotalWorkingYears": [TotalWorkingYears[idx1]],"WorkLifeBalance":[WorkLifeBalance[idx1]], "YearsInCurrentRole" : [YearsInCurrentRole[idx1]], "YearsSinceLastPromotion": [YearsSinceLastPromotion[idx1]], "YearsWithCurrManager" : [YearsWithCurrManager[idx1]]})
                ml1 = model1.predict(x1)
                print('ml1 value')
                print(ml1)
                k = ml1-YearsAtCompany[idx1]
                print('k value')
                print(k)
                print('No of years')
                print(YearsAtCompany[idx1])
                k = k.item()
                k = round(k)
                if k<=0:
                    t="immediately"
                else:
                    t="within "+ str(k) + " year(s)"
                if item == 1:
                    if k <= 0:
                        t="will leave immediately"
                    else:
                        t="will leave within "+ str(k) + " year(s)"
                    writer.writerow({'Employee_Number': empIdList[idx1][0], 'Employee_Name': empNameList[idx1][0], 'Attrition(Stay/Leave)' : 'Will Leave', 'TimeSpan' : t})
                else:
                    if k <= 0:
                        k = "1"
                    t = "will stay for " + str(k) + " year(s)"
                    writer.writerow({'Employee_Number': empIdList[idx1][0], 'Employee_Name': empNameList[idx1][0], 'Attrition(Stay/Leave)' : 'Stay', 'TimeSpan' : t})
                idx1 = idx1 + 1
            csvfile.close()
        return 1
    else:
        data = pd.read_csv(save_location)
        empNumber = data['EmployeeNumber'].tolist()
        print(empNumber)
        empNumberList = []
        cnt = 0
        rowcnt = 0
        flag = 0
        for num in empNumber:
            lst=[]
            if num == int(empID):
                flag = 1
                rowcnt = cnt
                print(rowcnt)
            cnt = cnt + 1
            lst.append(num)
            empNumberList.append(lst)
        print(empNumberList)
        test = []
        with open(save_location) as file_obj:
            reader_obj = csv.reader(file_obj)
            idx = 0
            for row in reader_obj:
                if idx == rowcnt:
                    test = row
                idx = idx + 1
        model1 = pickle.load(open('model1.pkl', 'rb'))
        x1 = pd.DataFrame({"Age": [Age[rowcnt]], "DailyRate": [DailyRate[rowcnt]], "DistanceFromHome":[DistanceFromHome[rowcnt]], "HourlyRate":[HourlyRate[rowcnt]],"MonthlyIncome":[MonthlyIncome[rowcnt]],"MonthlyRate":[MonthlyRate[rowcnt]],"NumCompaniesWorked":[NumCompaniesWorked[rowcnt]], "PercentSalaryHike":[PercentSalaryHike[rowcnt]],
        "PerformanceRating":[PerformanceRating[rowcnt]],"TotalWorkingYears": [TotalWorkingYears[rowcnt]],"WorkLifeBalance":[WorkLifeBalance[rowcnt]], "YearsInCurrentRole" : [YearsInCurrentRole[rowcnt]], "YearsSinceLastPromotion": [YearsSinceLastPromotion[rowcnt]], "YearsWithCurrManager" : [YearsWithCurrManager[rowcnt]]})
        ml1 = model1.predict(x1)
        print('ml1 value')
        print(ml1)
        print('Years at company')
        print(YearsAtCompany[rowcnt])
        k = ml1-YearsAtCompany[rowcnt]
        print('k value')
        print(k)
        k = ml1-YearsAtCompany[rowcnt]
        k = k.item()
        k = round(k)
        if k<=0:
            t="will leave immediately"
        else:
            t="will leave within "+ str(k) + " year(s)"
        res = 0
        if flag == 1:
            if int(test[2]) >= 25 and int(test[2]) <= 45 and (test[8] == "Marketing" or test[8] == "Technical Degree") and test[9] < 3 and test[12] < 2 and test[13] < 2 and test[15] < 2:
                res = 1
            else:
                res = 0
        if flag == 1:
            with open('Employee_Details.csv', 'w', newline='') as csvfile:
                header = ['Employee_Number','Employee_Name','Attrition(Stay/Leave)', 'TimeSpan']
                writer = csv.DictWriter(csvfile, fieldnames=header)
                writer.writeheader()
                print('Result')
                print(res)
                if res == 1:
                    if k <= 0:
                        t="immediately"
                    else:
                        t="within "+ str(k) + " year(s)"
                    writer.writerow({'Employee_Number': empNumberList[rowcnt][0], 'Employee_Name': empNameList[rowcnt][0], 'Attrition(Stay/Leave)' : 'Will Leave', 'TimeSpan' : t})
                else:
                    if k <= 0:
                        k = "1"
                    t = "will stay for " + str(k) + " year(s)"
                    writer.writerow({'Employee_Number': empNumberList[rowcnt][0], 'Employee_Name': empNameList[rowcnt][0], 'Attrition(Stay/Leave)' : 'Stay', 'TimeSpan' : t})
                csvfile.close()
        return flag


@app.route('/upload', methods=['GET', 'POST'])
def upload():
        if request.method == 'POST':
            file = request.files['csvfile']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(save_location)
                return render_template('choose.html')
        return render_template('incorrectDetails.html')


@app.route('/select', methods=['GET', 'POST'])
def select():
    if request.method == 'POST':
        empID = request.form['fname']
        filename = [i for i in os.listdir('static/input') if i.endswith('.csv')][0]
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print('fileName' + save_location)
        res = process_file(save_location, empID)
        if res == 1:
            return render_template('downloadDetails.html')
        else:
            return render_template('employeeDetailsNotFound.html')

@app.route('/allEmployees', methods=['GET', 'POST'])
def allEmployees():
    if request.method == 'POST':
        filename = [i for i in os.listdir('static/input') if i.endswith('.csv')][0]
        save_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        res = process_file(save_location, "")
        if res == 1:
            return render_template('downloadDetails.html')
        else:
            return render_template('incorrectDetails.html')   
    
@app.route('/Download_file', methods=['GET', 'POST'])
def Download_file():
    path = "Employee_Details.csv"
    return send_file(path, as_attachment=True)

@app.route('/attributes', methods=['GET', 'POST'])
def required_attributes():
    return render_template('requiredAttributes.html')

if __name__ == '__main__':
    app.run(debug=True)