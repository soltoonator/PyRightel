# a list of discovered and working API endpoints 
(this list will be updated as more enpoints are tested and discovered)

root: ``https://myrightel-api.rightel.ir/``




| Endpoint | url | Methods | Data sent | Data recived | Response codes | Required headers | Behaviour |
| :---- | :----: | :----: | :----: | :----: | :----: | :----: | :----: |
||**Authentication** |
| login using password | ``/v2/auth/login/password/`` | post | ``{"msisdn":"09####","password":"####"}`` | accessToken, refreshToken, phone number, meli code, simcard type, owners first name | 200,401 | "version" | if login succeeds the response will be 200 with an access token and if it failes it returns 401 with a message on why it failed |
| verify token | ``/v2/auth/`` | post | empty | same accessToken, refreshToken, phone number, meli code | 200,401 | "version","Authorization" | if the fed Authorization header is valid the result will be 200 and the same auth is returned back with a refresh token in the response data and if its not valid or expired it returns 401 |
||**Account balance** |
| balance | ``/v2/balance/`` | get | none | available to spend internet, sms, phone and wallet credit | 200,401 | "version","Authorization" |  |
| credit | ``/v2/credit/`` | get | none | info about the credit available in wallet, limits and billing | 200,401 | "version","Authorization" |  |
| active packages | ``/v2/balance/list/`` | get | none | active packages and credit | 200,401 | "version","Authorization" |  |
||**Account information**|
| owner info | ``/v2/profile/`` | get | none | info about simcard owner | 200,401 | "version","Authorization" | WARNING - outputs personal data | 
| simcard info |``/v2/sim/info/``| get | none |phone number, simcard enabled status, ICCID|200,401|"version","Authorization"| WARNING - outputs personal data |
||**Account history**|
| package usage | ``/v2/balance/usage/`` | get | none | untested | untested | untested | untested |
| package history | ``/v2/package/history/`` | get | none | untested | untested | untested | untested | 
| payment history | ``/v2/payment/history/`` | get | none | untested | untested | untested | untested | 
||**Settings**|
| change password | ``/v2/auth/password/`` | post | ``{"password":"####","repeatPassword":"####"}`` | untested | untested | untested | untested | 
| show sms setting | ``/v2/setting/vas/all/`` | get | none | untested | untested | untested | untested | 
| set sms setting | ``/v2/setting/vas/`` | put | ``{"type":"###","status":false/true}`` | untested | untested | untested | untested | 
| show service settings | ``/v2/setting/service/all/`` | untested | untested | untested | untested | untested | untested | 
| set service settings | ``/v2/setting/service/`` | untested | untested | untested | untested | untested | untested |
||**Available packages and services**|
| lists all packages | ``/v2/package/`` | get | none | untested | untested | untested | untested | 
| lists all ussd codes | ``/v2/app/ussd/code/`` | get | none | untested | untested | untested | untested | 
||**Others**|
| loyalty perks | ``/v2/loyalty/purple-chance/`` | untested | untested | untested | untested | untested | untested | 
| lists city names | ``/v2/profile/address/`` | untested | untested | untested | untested | untested | probably used to get updated names about city names and proprovinces | 
||**Untested**|
| untested | ``/v2/app/psp/`` |  untested | untested | untested | untested | untested | untested |
| untested | ``/v2/payment/tax/package/`` | untested | ``{"msisdn":"{phone number}","offerCode":"{package ID}"}`` | untested | untested | untested | untested | 



