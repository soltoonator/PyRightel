import requests
from . import data
import jwt
import logging
import json

log = logging.getLogger('PyRightel.data')
log.debug("setting up communications module")

#allowed methods
#POST, OPTIONS, GET, PUT, DELETE

#used methods
#POST, GET, PUT


#TODO proper error handeling both in network errors and response errors from api
def get(session,endpoint)->dict:

    #possible errors by this point: 
    #invalid session object, invalid endpoint
    #endpoint should be string
    #session should have a token and not be expired

    # when requests.HTTPError /(means that the response was not 200)
    # log into console 
    # return error status or null

    #when (DONE)
    # requests.ConnectTimeout 
    # requests.ConnectionError
    # requests.ReadTimeout
    # requests.Timeout
    # should be handled by urllib3 and retry strategy in data.static

    #when requests.RequestException it was unknown error and should dump all and abort excution

    # as for these i dont know what to do yet. 
    # requests.TooManyRedirects (should not redirect at all, it must have failed)
    # requests.JSONDecodeError (DONE)
    # soft fail maybe? (not abort but return null data or error data)
    

    req = requests.Request('GET',endpoint,headers=session.headers)
    req = req.prepare()
    res = session.session.send(req,timeout=data.static.requestTimeout)
    if (res.status_code == 200):
        if (json.loads(res.text)):
            response = res.json()
            outdata = response["data"]
            message = response["message"]
            #TODO check for error messages here later. for now just pass them
            return data.response(data.responseStatus[message],outdata)

    elif (res.status_code == 403):
         return data.response(data.responseStatus["unauthenticated"],None)
    else:
        return data.response(data.responseStatus["unexpected"],None)

def post(session,endpoint,postData)->dict:
    req = requests.Request('POST',endpoint,data=postData,headers=session.headers)
    req = req.prepare()
    res = session.session.send(req,timeout=data.static.requestTimeout)
    return res

def put(session,endpoint,putData)->dict:
    req = requests.Request('PUT',endpoint,data=putData,headers=session.headers)
    req = req.prepare()
    res = session.session.send(req,timeout=data.static.requestTimeout)
    return res

log.debug("finished setting up communications module")