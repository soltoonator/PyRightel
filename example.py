from PyRightel import main as Rightel
import pickle
import os.path

phoneNumber = "09876543210"
password = "**********"

session = None

#saving the authentication session into a file as a simple cache (proper chacing will be a part of the wrapper)
if (os.path.isfile('session.temp')):
    with open('session.temp', 'rb') as handle:
        session = pickle.load(handle)
else:
    session = Rightel.getSession(phoneNumber,password)
    with open('session.temp', 'wb') as handle:
        pickle.dump(session, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(f"is authenticated: {Rightel.isAuthenticated(session)}\n")

print("Here is a list of active packages and their properties:")
ls = Rightel.listPackages(session)
for package in ls:
    print(f"Package Type: {package.packageType.name} - name:{package.packageName} - remain: {package.remain} {package.unit.name} ({package.remainingBalancePercent}%) - remaining time:{package.remainingTimestamp} - is expired? ({package.isExpired}) - duration:{package.duration} - start:{package.startTimestamp} -> end:{package.endTimestamp}")