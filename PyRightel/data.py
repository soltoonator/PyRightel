import requests
from dataclasses import dataclass
import platform
from enum import Enum
import logging
from urllib3.util.retry import Retry
import time

log = logging.getLogger('PyRightel.data')
log.debug("setting up data module")

class Endpoint(property):
    def __init__(self,getter):
        self.getter = getter
    def __get__(self,cls,owner):
        return self.getter(owner)


class session:
    def __init__(self):
        self.session = requests.session()
        if (static.httpAdapter is None):
            static.httpAdapter = requests.adapters.HTTPAdapter(max_retries=static.retryStrategy)
        self.session.mount(static.rootUrl,static.httpAdapter)
        self.authExpirey = None 
        self.headers = {"version": static.apiVersion, "User-Agent"  : static.userAgent, "os":platform.system()} 
        self.phoneNumber = None
        self.password = None
        self.token = None

class responseStatus(Enum):
    unspecified = 0
    OK = 1
    unauthenticated = 2
    unexpected = 3
    unknown = 99

class packageType(Enum):
    none = 0
    unspecified = 1
    CREDIT = 2
    CALL = 3
    INTERNET = 4
    SMS = 5

class packageUnit(Enum):
    none = 0
    unspecified = 1
    RIAL = 2
    GIGABYTE = 3
    MEGABYTE = 4
    #TODO add all units (i have to pay for some packages and sniff the api to see all of the units)

class package:
    def __init__(self):
        self.packageName : str #friendly name of the package when bought. not an id or unique name.
        self.packageType : packageType #the type of the balance held in package
        self.unit : packageUnit #string name of the unit of mesurement of the package
        self.isLocalCurrency : bool#true for the money wallet balance which is a package that everyone has in their account
        self.remain : float #remaining balance in package
        self.balance : float #total balance in package
        self.startTimestamp :int #both timestamps gotten from api is offset by 12600 seconds to convert the resulting time from gmt to local iran time
        self.endTimestamp : int


    @property    
    def remainingBalancePercent (self) -> int:
        if (self.balance != 0):
            return round(((self.remain*100)/self.balance),2)
        else:
            return 0

    @property
    def remainingTimestamp (self) -> int:
        return  int(self.endTimestamp - time.time())
    
    @property
    def duration (self) -> int:
        return int(self.endTimestamp - self.startTimestamp)

    @property
    def isExpired (self) -> bool:
        if (self.remainingTimestamp >= 0):
            return False
        else:
            return True

    
class response:
    def __init__(self,status:responseStatus,responseData):
        self.status = status
        self.data = responseData
         

class static:
    #all of the static data of the wrapper is stored here
    #TODO find a way to store these in a file and read from it properly
    globalHeaders = {"version": "0.13.0"} 
    rootUrl = "https://myrightel-api.rightel.ir" 
    endpointsList = {
        #TODO add all of the endpoints to this dict
        "PasswordLogin":"/v2/auth/login/password/",
        "verifyToken":"/v2/auth/",
        "listPackages":"/v2/balance/list/",
        "appAvailable":"/v2/app/available/"
    } 

    pyrVersion = "0.0.1-pa"
    apiVersion = "0.13.0"
    userAgent = f"PyRightel/{pyrVersion}"

    maxRetryOnError = 5
    requestTimeout = 4

    httpAdapter = None

    retryStrategy = Retry(
        total = maxRetryOnError,
        redirect = 0,
        backoff_factor = 1,
        backoff_max = 5
    )

    #TODO find a way to make these read only and not mutable (i hate python)
    #TODO this seems inefficent, cache or static? find a way to serve a premade list instead of adding strings for each read (but for now it works fine)
    class endpoints:
        @Endpoint
        def LoginUsingPassword(self):
            return static.rootUrl+static.endpointsList["PasswordLogin"]

        @Endpoint
        def verifyToken(self):
            return static.rootUrl+static.endpointsList["verifyToken"]

        @Endpoint
        def listPackages(self):
            return static.rootUrl+static.endpointsList["listPackages"]
        
        @Endpoint
        def appAvailable(self):
            return static.rootUrl+static.endpointsList["appAvailable"]

log.debug("finished setting up data module")
            