import requests
from flask import Flask, render_template, request
from flask import jsonify
from markupsafe import escape

app = Flask(__name__)

coming_date = 15
base_url = "https://booking.communitytest.gov.hk/form/"

def getCenterList():
    response = requests.get(base_url + "ct_center")
    center_list = response.json()['children']
    return jsonify(center_list)

def getCenterAvailableByID(centerArr):
    coming_date = 15  
    center = ""
    res = []

    for i in range(len(centerArr)):
        data = {'center_id': centerArr[i]}
        response = requests.post(base_url + "api_center", data = data)
        center = response.json()['center_id']

        for i in range(coming_date):
            tmp = []
            date = ""
            timeslots = response.json()['avalible_timeslots'][i]['timeslots']            
            for j in range(len(timeslots)):
                if timeslots[j]['value']:
                   date = response.json()['avalible_timeslots'][i]['date']
                   tmp.append(timeslots[j]['time'])
            if date != "":
                res.append({"date":date, "timeslot":tmp})

    return {"center":center, "res":res}

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/getCenterList", methods=['GET', 'POST'])
def showCenterList():
    return getCenterList()

@app.route("/getCenterAvailable", methods=['GET', 'POST'])
def showCenterAvailable():
    if request.method=='POST':
        centerArr = request.form.getlist("centerArr[]")        
        return getCenterAvailableByID(centerArr)

@app.route("/getCenterAvailable/<int:center_id>")
def getCenterAvailable(center_id): 
    return 'The center ID is: {}'.format(escape(center_id))
    
 

if __name__ == "__main__":
    app.run()