from . import data
from . import communications as c
import time
import requests
import jwt
import logging 

log = logging.getLogger('PyRightel.main')
log.debug("setting up main module")

#get session object (phone number and account password is required)
def getSession(phoneNumber:str,password:str)-> data.session:
    session = data.session()
    session.phoneNumber = phoneNumber
    session.password = password
    result = authenticate (session)
    if (result is True):
        return session
    elif (result is False or result is None):
        #TODO log error
        return None
    else:
        #unknown error 
        return None

def authenticate(session):
    #TODO add checks to see what fields of a session object is populated
    if (session.token == None or not isAuthenticated(session)):

        if (type(session.phoneNumber) is str and type(session.password) is str):

            if ((len(session.phoneNumber)>=9 and len(session.phoneNumber)<=13)or(len(session.password)>=8 and en(session.password)<=12)):

                if(session.phoneNumber.isnumeric()):

                    try:
                        del session.headers["Authorization"]
                    except KeyError:
                        pass
                    post=f'{{"msisdn":"{session.phoneNumber}","password":"{session.password}"}}'
                    req = requests.Request('POST',data.static.endpoints.LoginUsingPassword,data=post,headers=session.headers)
                    #TODO proper connection error handeling
                    req = req.prepare()
                    res = session.session.send(req)
                    if (res.status_code == 200):
                        session.token = res.json()["data"][0]["accessToken"]
                        session.headers["Authorization"] = f"Bearer {session.token}"
                        session.authExpirey = jwt.decode(session.token,options={"verify_signature": False})["expireAt"]
                        return True
                    elif (res.status_code == 401):
                        #bad login creds
                        raise authException(f"invalid login, check phone number or password\nResponse: {res.reason}-({res.status_code})\n{res.url}")
                        return False
                    elif (res.status_code != 200 and res.status_code != 401):
                        raise authException(f"unexpected status while authenticating, is Rightel service available?\nResponse: {res.reason}-({res.status_code})\n{res.url}")
                        return None
                    else:
                        raise authException(f"unknown error while authenticating, check internet connection perhaps?\nResponse: {res.reason}-({res.status_code})\n{res.url}")
                        return None

                elif(not session.phoneNumber.isnumeric()):
                    raise authException("phone number has invalid characters")
                    return None

            elif (len(session.phoneNumber)<9 or len(session.phoneNumber)>13):
                raise authException("phone number has invalid length")
                return None

            elif (len(session.password)<8 or en(session.password)>12):
                raise authException("password has invalid length")
                return None

            elif ((len(session.password)<8 or en(session.password)>12) and (len(session.phoneNumber)<9 or len(session.phoneNumber)>13)):
                raise authException("phone number and password are a valid lenght")
                return None

        elif (type(session.phoneNumber) is not str):
            raise authException("phone number is not a string")

        elif (type(session.password) is not str):
            raise authException("password is not a string")

        elif (type(session.phoneNumber) is not str and type(session.password) is not str):
            raise authException("phone number and password are not a string, have you forgotten setting them?")
    else:
        return isAuthenticated(session)

def isAuthenticated(session) -> bool:
    log.debug(f"checking authentication status for session ({session.phoneNumber})")
    req = requests.Request('POST',data.static.endpoints.verifyToken,headers=session.headers)
    req = req.prepare()
    res = session.session.send(req)
    if (res.status_code==200):
        #success, authenticated
        if (session.token != res.json()["data"]["accessToken"]):
            session.token = res.json()["data"]["accessToken"]
            session.headers["Authorization"] = f"Bearer {session.token}"
            session.authExpirey = jwt.decode(session.token,options={"verify_signature": False})["expireAt"]
        return True
    elif(res.status_code==401):
        #success, unauthenticated
        return False
    else:
        #failed
        raise authException(f"unexpected status code while checking, is Rightel service available?\nResponse: {res.reason}-({res.status_code})\n{res.url}")
        return None

def ImportToken(session,tokenString): #debug function (not gonna work in future i think)
    session.token = tokenString
    session.headers["Authorization"] = f"Bearer {session.token}"
    session.authExpirey = jwt.decode(session.token,options={"verify_signature": False})["expireAt"]
    #check if the token is valid (maybe?)
    #return session.isAuthenticated()

def isSessionExpired (session) -> bool:
    if (session.authExpirey is not None):
        if session.authExpirey > time.time():
            return False
        else:
            return True
    else:
        return True

def listPackages (session) -> list[data.package]:  
    log.debug(f"asking for a list of packages for ({session.phoneNumber})")
    res = c.get (session,data.static.endpoints.listPackages)
    if (res.status == data.responseStatus["OK"]):
        packagelist = []
        outdata = res.data
        if (len(outdata)>0):
            for packageType in outdata["balance"]:
                for package in outdata["balance"][packageType]:
                    newPackage = data.package()
                    newPackage.packageName = package["name"]
                    newPackage.packageType = data.packageType[package["type"]]
                    newPackage.unit = data.packageUnit[package["unit"]]
                    newPackage.isLocalCurrency = package["isLocalCurrency"]
                    newPackage.remain = package["remain"]
                    newPackage.balance = package["balance"]
                    # first /1000 to convert to seconds from miliseconds then - 12600 to convert from local (rightel time) to GMT
                    newPackage.startTimestamp =  int ( package["startTimestamp"]  / 1000 ) - 12600
                    newPackage.endTimestamp = int (package["endTimestamp"] / 1000 ) - 12600
                    packagelist.append(newPackage)

        return packagelist
    else:
        return None

log.debug("finished setting up main module")