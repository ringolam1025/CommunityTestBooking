import requests

coming_date = 15
base_url = "https://booking.communitytest.gov.hk/form/"


def getCenterList():
    response = requests.get(base_url + "ct_center")
    center_list = response.json()['children']
    print(center_list)

def getCenterAvailable(center_id):
    data = {'center_id': center_id}

    response = requests.post(base_url + "api_center", data = data)
    print("center_id: " + response.json()['center_id'])

    for i in range(coming_date):
        timeslots = response.json()['avalible_timeslots'][i]['timeslots']
        print(response.json()['avalible_timeslots'][i]['date'])
        for j in range(len(timeslots)):
            if timeslots[j]['value']:
                print(timeslots[j]['time'])
            
        print("==========================")

getCenterList()
# getCenterAvailable(8)