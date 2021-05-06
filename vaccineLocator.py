#!/usr/bin/env python3
import json
import requests
import os
import sys
import getopt
import hashlib
import time
production_server = "https://cdn-api.co-vin.in/api"
demo_server = "https://api.demo.co-vin.in/api"
ERROR_MSG = "Usage: cowin.py -m <mobile> -p <pin> -d <date>"

headers = {
    'content-type': 'application/json',
    # "x-api-key": "3sjOr2rmM52GzhpMHjDEE1kpQeRxwFDr4YcBEimi",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0",
    "Accept-Language": "en_US"
}
global otp, txnId, token

server = production_server


def validateArgs(argv):
    global mobile, pin, date, dist_id
    mobile = "9999999999"
    pin = "560003"
    date = "06-05-2021"
    dist_id = "294"  # 294 BBMP, 272 Bidar, 267 Gulbarga 265 BLR Urban

    try:
        opts, args = getopt.getopt(argv, "m:p:d:x:")
    except getopt.GetoptError:
        print(ERROR_MSG)
        sys.exit(2)

    for opt, arg in opts:
        if opt is None:
            print(ERROR_MSG)
            sys.exit(2)
        if opt in ("-m"):
            mobile = arg
        elif opt in ("-p"):
            pin = arg
        elif opt in ("-d"):
            date = arg
        elif opt in ("-x"):
            dist_id = arg
        else:
            print(ERROR_MSG)
            sys.exit(2)


def sendPostRequest(url, jd):
    fullUrl = server+url
    print(fullUrl)
    r = requests.post(server+url, jd, headers=headers)
    if r.status_code != 200:
        print("Error: ", r.status_code)
        return None
    return r.json()


def sendGetRequest(url, headers):
    # print(heads)
    fullUrl = server+url
    print(fullUrl)
    r = requests.get(fullUrl, headers=headers)
    if r.status_code != 200:
        print("Error: ", r.status_code)
        return None
    return r.json()


def generateOTP():
    url = "/v2/auth/public/generateOTP"
    data = {
        "mobile": mobile
    }
    jd = json.dumps(data)
    rd = sendPostRequest(url=url, jd=jd)
    if rd != None:
        return rd['txnId']
    return None


def confirmOTP():
    url = "/v2/auth/public/confirmOTP"
    data = {
        "otp": otp
    }
    data["txnId"] = txnId
    jd = json.dumps(data)
    rd = sendPostRequest(url=url, jd=jd)
    if rd != None:
        print(rd)
        return rd["token"]


def getBeneficiaries():
    heads = headers
    heads["Authorization"] = "Bearer " + token
    url = "/v2/appointment/beneficiaries"
    rd = sendGetRequest(url=url, headers=heads)
    if rd != None:
        print(rd)


def getListByPin(pin, date):
    heads = headers
    #heads["Authorization"] = "Bearer " + token
    url = "/v2/appointment/sessions/public/findByPin?pincode=" + pin + "&date=" + date
    rd = sendGetRequest(url=url, headers=heads)
    if rd != None:
        print(rd)


def getCalByPin():
    heads = headers
    #heads["Authorization"] = "Bearer " + token
    url = "/v2/appointment/sessions/public/calendarByPin?pincode=" + pin + "&date=" + date
    rd = sendGetRequest(url=url, headers=heads)
    if rd != None:
        return rd
    return None


def findAvailableHosp(centers):
    if centers != None:
        for k in centers:
            for y in centers[k]:
                sessions = y["sessions"]
                for session in sessions:
                    if session["available_capacity"] != 0 and session["min_age_limit"] != 45:
                        print("Available ", y["name"],
                              "on ", session["date"])
                        os.system('afplay -t 30 alarm.mp3')


def getStates():
    url = "/v2/admin/location/states"
    rd = sendGetRequest(url=url, headers=headers)
    if rd != None:
        print(rd)


def getDistricts():
    state_id = "16"  # Karnataka state_id 32 - Telangana
    url = "/v2/admin/location/districts/" + state_id
    rd = sendGetRequest(url=url, headers=headers)
    if rd != None:
        print(rd)


def getCalByDist():
    url = "/v2/appointment/sessions/public/calendarByDistrict?district_id=" + \
        dist_id + "&date=" + date
    rd = sendGetRequest(url=url, headers=headers)
    if rd != None:
        return rd
    return None


if __name__ == "__main__":
    validateArgs(sys.argv[1:])
    '''
    #txnId = generateOTP()
    print(txnId)
    otpPin = input("Enter OTP: ")
    otp = hashlib.sha256(otpPin.encode('utf-8')).hexdigest()
    print(otp)
    #token = confirmOTP()
    # print(token)
    # getBeneficiaries()
    '''
    #getListByPin(pin=pin, date=date)
    '''
    centers = getCalByPin()
    findAvailableHosp(centers)
    '''
    # getStates()
    # getDistricts()
    while True:
        centers = getCalByDist()
        findAvailableHosp(centers)
        time.sleep(10)