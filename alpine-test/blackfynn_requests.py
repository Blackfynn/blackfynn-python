import requests
import json

session = requests.session()
session.proxies = {'http':'127.0.0.1:8080', 'https':'127.0.0.1:8080'}
session.verify = False

# LOGIN
burp0_url = "https://api.blackfynn.net:443/account/api/session"
burp0_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*",
                 "User-Agent": "python-requests/2.21.0", "Authorization": "Bearer None",
                 "Content-Type": "application/json"}
burp0_json = {"secret": "512bc9e6-7d0d-4f6b-864b-7fa36e2706f3", "tokenId": "67edea75-b019-4623-a36c-e053a1eec8d9"}
resp = session.post(burp0_url, headers=burp0_headers, json=burp0_json)

# '{"session_token":"f516efea-d95e-4e66-b249-fc2bae5bda31","organization":"N:organization:7aae2bf7-ff15-4071-aa2a-e876ae609d3c","expires_in":7200}'
resp_json = json.loads(resp.content)
X_SESSION_ID = resp_json['session_token']
AUTHORIZATION_BEARER = "Bearer " + resp_json['session_token']
X_SESSION_ID = resp_json['session_token']
X_ORGANIZATION_ID = resp_json['organization']
JSESSIONID = "605BF9FC57BD59F87F22AD756BEC253B" #resp_json['JSESSIONID']
print ("JSESSIONID = %s" % JSESSIONID)
#exit(0)

# REPLACE ": []} with ": []}

# "Authorization": AUTHORIZATION_BEARER
# Search and replace on: "X-SESSION-ID": X_SESSION_ID
# Search and replace on: "X-ORGANIZATION-ID": X_ORGANIZATION_ID

# Capture responses
# Authorization: Bearer
# X-SESSION-ID:

burp1_url = "https://api.blackfynn.net:443/user/"
burp1_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID}
session.get(burp1_url, headers=burp1_headers)

burp2_url = "https://api.blackfynn.net:443/organizations/N%3Aorganization%3A7aae2bf7-ff15-4071-aa2a-e876ae609d3c"
burp2_cookies = {"scentry.auth.default.user": ""}
burp2_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp2_url, headers=burp2_headers, cookies=burp2_cookies)

burp3_url = "https://api.blackfynn.net:443/organizations?includeAdmins=false"
burp3_cookies = {"scentry.auth.default.user": ""}
burp3_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp3_url, headers=burp3_headers, cookies=burp3_cookies)

burp4_url = "https://api.blackfynn.net:443/datasets/"
burp4_cookies = {"scentry.auth.default.user": ""}
burp4_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp4_url, headers=burp4_headers, cookies=burp4_cookies)

burp5_url = "https://api.blackfynn.net:443/datasets"
burp5_cookies = {"scentry.auth.default.user": ""}
burp5_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp5_json={"automaticallyProcessPackages": False, "description": "", "name": "test_dataset_1560722459908", "properties": []}
session.post(burp5_url, headers=burp5_headers, cookies=burp5_cookies, json=burp5_json)

burp6_url = "https://api.blackfynn.net:443/datasets/"
burp6_cookies = {"scentry.auth.default.user": ""}
burp6_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp6_url, headers=burp6_headers, cookies=burp6_cookies)

burp7_url = "https://api.blackfynn.net:443/datasets/"
burp7_cookies = {"scentry.auth.default.user": ""}
burp7_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp7_url, headers=burp7_headers, cookies=burp7_cookies)

burp8_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp8_cookies = {"scentry.auth.default.user": ""}
burp8_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp8_json={"automaticallyProcessPackages": False, "description": "", "name": "Same Dataset, Different Name 2019-06-16 17:01:02.656173-9e95", "properties": []}
session.put(burp8_url, headers=burp8_headers, cookies=burp8_cookies, json=burp8_json)

burp9_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp9_cookies = {"scentry.auth.default.user": ""}
burp9_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp9_url, headers=burp9_headers, cookies=burp9_cookies)

burp10_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp10_cookies = {"scentry.auth.default.user": ""}
burp10_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp10_url, headers=burp10_headers, cookies=burp10_cookies)

burp11_url = "https://api.blackfynn.net:443/packages"
burp11_cookies = {"scentry.auth.default.user": ""}
burp11_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp11_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Child of Dataset", "packageType": "Text", "properties": []}
session.post(burp11_url, headers=burp11_headers, cookies=burp11_cookies, json=burp11_json)

burp12_url = "https://api.blackfynn.net:443/data/delete"
burp12_cookies = {"scentry.auth.default.user": ""}
burp12_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp12_json={"things": ["N:package:d333f0b1-3d2f-46f1-a5a0-6a1ac1728bf1"]}
session.post(burp12_url, headers=burp12_headers, cookies=burp12_cookies, json=burp12_json)

burp13_url = "https://api.blackfynn.net:443/datasets/"
burp13_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp13_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp13_url, headers=burp13_headers, cookies=burp13_cookies)

burp14_url = "https://api.blackfynn.net:443/packages"
burp14_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp14_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp14_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some MRI", "packageType": "MRI", "properties": []}
session.post(burp14_url, headers=burp14_headers, cookies=burp14_cookies, json=burp14_json)

burp15_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A40fddc01-938a-4ba3-b43a-ae595b399246"
burp15_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp15_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp15_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some Other MRI", "packageType": "MRI", "properties": [], "state": "UNAVAILABLE"}
session.put(burp15_url, headers=burp15_headers, cookies=burp15_cookies, json=burp15_json)

burp16_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A40fddc01-938a-4ba3-b43a-ae595b399246"
burp16_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp16_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp16_url, headers=burp16_headers, cookies=burp16_cookies)

burp17_url = "https://api.blackfynn.net:443/data/delete"
burp17_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp17_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp17_json={"things": ["N:package:40fddc01-938a-4ba3-b43a-ae595b399246"]}
session.post(burp17_url, headers=burp17_headers, cookies=burp17_cookies, json=burp17_json)

burp18_url = "https://api.blackfynn.net:443/packages"
burp18_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp18_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp18_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Something else", "packageType": "TimeSeries", "properties": []}
session.post(burp18_url, headers=burp18_headers, cookies=burp18_cookies, json=burp18_json)

burp19_url = "https://api.blackfynn.net:443/data/delete"
burp19_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp19_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp19_json={"things": ["N:package:f458f3aa-f8f4-45e6-8e7c-2385234315ee"]}
session.post(burp19_url, headers=burp19_headers, cookies=burp19_cookies, json=burp19_json)

burp20_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Af458f3aa-f8f4-45e6-8e7c-2385234315ee"
burp20_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp20_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp20_url, headers=burp20_headers, cookies=burp20_cookies)

burp21_url = "https://api.blackfynn.net:443/packages"
burp21_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp21_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp21_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "My Stateful Package", "packageType": "Slide", "properties": []}
session.post(burp21_url, headers=burp21_headers, cookies=burp21_cookies, json=burp21_json)

burp22_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Acfe8bbe8-b259-4022-8b69-3a0ab3dd56c1"
burp22_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp22_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp22_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "My Stateful Package", "packageType": "Slide", "properties": [], "state": "READY"}
session.put(burp22_url, headers=burp22_headers, cookies=burp22_cookies, json=burp22_json)

burp23_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Acfe8bbe8-b259-4022-8b69-3a0ab3dd56c1"
burp23_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp23_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp23_url, headers=burp23_headers, cookies=burp23_cookies)

burp24_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Acfe8bbe8-b259-4022-8b69-3a0ab3dd56c1"
burp24_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp24_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp24_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "My Stateful Package", "packageType": "Slide", "properties": [], "state": "ERROR"}
session.put(burp24_url, headers=burp24_headers, cookies=burp24_cookies, json=burp24_json)

burp25_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Acfe8bbe8-b259-4022-8b69-3a0ab3dd56c1"
burp25_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp25_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp25_url, headers=burp25_headers, cookies=burp25_cookies)

burp26_url = "https://api.blackfynn.net:443/data/delete"
burp26_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp26_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp26_json={"things": ["N:package:cfe8bbe8-b259-4022-8b69-3a0ab3dd56c1"]}
session.post(burp26_url, headers=burp26_headers, cookies=burp26_cookies, json=burp26_json)

burp27_url = "https://api.blackfynn.net:443/packages"
burp27_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp27_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp27_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some Video", "packageType": "Video", "properties": []}
session.post(burp27_url, headers=burp27_headers, cookies=burp27_cookies, json=burp27_json)

burp28_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp28_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp28_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp28_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}]}
session.put(burp28_url, headers=burp28_headers, cookies=burp28_cookies, json=burp28_json)

burp29_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8"
burp29_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp29_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp29_url, headers=burp29_headers, cookies=burp29_cookies)

burp30_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp30_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp30_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp30_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}]}
session.put(burp30_url, headers=burp30_headers, cookies=burp30_cookies, json=burp30_json)

burp31_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp31_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp31_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp31_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}]}
session.put(burp31_url, headers=burp31_headers, cookies=burp31_cookies, json=burp31_json)

burp32_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp32_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp32_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp32_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}]}
session.put(burp32_url, headers=burp32_headers, cookies=burp32_cookies, json=burp32_json)

burp33_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp33_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp33_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp33_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}]}
session.put(burp33_url, headers=burp33_headers, cookies=burp33_cookies, json=burp33_json)

burp34_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp34_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp34_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp34_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp34_url, headers=burp34_headers, cookies=burp34_cookies, json=burp34_json)

burp35_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp35_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp35_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp35_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp35_url, headers=burp35_headers, cookies=burp35_cookies, json=burp35_json)

burp36_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp36_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp36_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp36_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp36_url, headers=burp36_headers, cookies=burp36_cookies, json=burp36_json)

burp37_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp37_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp37_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp37_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp37_url, headers=burp37_headers, cookies=burp37_cookies, json=burp37_json)

burp38_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp38_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp38_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp38_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp38_url, headers=burp38_headers, cookies=burp38_cookies, json=burp38_json)

burp39_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp39_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp39_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp39_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp39_url, headers=burp39_headers, cookies=burp39_cookies, json=burp39_json)

burp40_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp40_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp40_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp40_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp40_url, headers=burp40_headers, cookies=burp40_cookies, json=burp40_json)

burp41_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp41_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp41_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp41_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp41_url, headers=burp41_headers, cookies=burp41_cookies, json=burp41_json)

burp42_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp42_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp42_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp42_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "my-123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp42_url, headers=burp42_headers, cookies=burp42_cookies, json=burp42_json)

burp43_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp43_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp43_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp43_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp43_url, headers=burp43_headers, cookies=burp43_cookies, json=burp43_json)

burp44_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp44_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp44_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp44_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp44_url, headers=burp44_headers, cookies=burp44_cookies, json=burp44_json)

burp45_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp45_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp45_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp45_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp45_url, headers=burp45_headers, cookies=burp45_cookies, json=burp45_json)

burp46_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp46_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp46_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp46_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1560704474316"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp46_url, headers=burp46_headers, cookies=burp46_cookies, json=burp46_json)

burp47_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp47_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp47_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp47_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1560704474316"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float1", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp47_url, headers=burp47_headers, cookies=burp47_cookies, json=burp47_json)

burp48_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp48_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp48_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp48_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": "my-value"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1560704474316"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float1", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp48_url, headers=burp48_headers, cookies=burp48_cookies, json=burp48_json)

burp49_url = "https://api.blackfynn.net:443/data/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8/properties"
burp49_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp49_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp49_json={"properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string2", "value": "#1231"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string3", "value": "123123.123"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date3", "value": "1560704470653"}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date2", "value": "1488847449697"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string4", "value": "According to plants, humans are blurry."}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-string", "value": "i123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int1", "value": "123123"}, {"category": "Blackfynn", "dataType": "integer", "fixed": False, "hidden": False, "key": "my-int2", "value": "123123"}, {"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "my-key", "value": ""}, {"category": "Blackfynn", "dataType": "date", "fixed": False, "hidden": False, "key": "my-date", "value": "1560704474316"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float1", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float2", "value": "123.123"}, {"category": "Blackfynn", "dataType": "double", "fixed": False, "hidden": False, "key": "my-float3", "value": "123123.0"}]}
session.put(burp49_url, headers=burp49_headers, cookies=burp49_cookies, json=burp49_json)

burp50_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Ad0278eee-7ddc-4825-b182-af453a035ee8"
burp50_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp50_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp50_url, headers=burp50_headers, cookies=burp50_cookies)

burp51_url = "https://api.blackfynn.net:443/packages"
burp51_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp51_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp51_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some MRI", "packageType": "MRI", "properties": []}
session.post(burp51_url, headers=burp51_headers, cookies=burp51_cookies, json=burp51_json)

burp52_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A4c8c4e9a-5033-40b0-b55b-a70813b3ddb8"
burp52_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp52_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp52_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some MRI", "packageType": "MRI", "properties": [], "state": "UNAVAILABLE"}
session.put(burp52_url, headers=burp52_headers, cookies=burp52_cookies, json=burp52_json)

burp53_url = "https://api.blackfynn.net:443/packages"
burp53_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp53_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp53_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some Video", "packageType": "Video", "properties": []}
session.post(burp53_url, headers=burp53_headers, cookies=burp53_cookies, json=burp53_json)

burp54_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Afb26ffb3-70f0-4817-85d1-9bea8e479b4f"
burp54_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp54_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp54_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some Video (1)", "packageType": "Video", "properties": [], "state": "UNAVAILABLE"}
session.put(burp54_url, headers=burp54_headers, cookies=burp54_cookies, json=burp54_json)

burp55_url = "https://api.blackfynn.net:443/data/delete"
burp55_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp55_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp55_json={"things": ["N:package:4c8c4e9a-5033-40b0-b55b-a70813b3ddb8"]}
session.post(burp55_url, headers=burp55_headers, cookies=burp55_cookies, json=burp55_json)

burp56_url = "https://api.blackfynn.net:443/data/delete"
burp56_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp56_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp56_json={"things": ["N:package:fb26ffb3-70f0-4817-85d1-9bea8e479b4f"]}
session.post(burp56_url, headers=burp56_headers, cookies=burp56_cookies, json=burp56_json)

#burp57_url = "https://api.blackfynn.net:443/account/api/session"
#burp57_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": #AUTHORIZATION_BEARER, "Content-Type": "application/json"}
#burp57_json={"secret": "512bc9e6-7d0d-4f6b-864b-7fa36e2706f3", "tokenId": "67edea75-b019-4623-a36c-e053a1eec8d9"}
#session.post(burp57_url, headers=burp57_headers, json=burp57_json)

burp58_url = "https://api.blackfynn.net:443/user/"
burp58_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID}
session.get(burp58_url, headers=burp58_headers)

burp59_url = "https://api.blackfynn.net:443/organizations/N%3Aorganization%3A7aae2bf7-ff15-4071-aa2a-e876ae609d3c"
burp59_cookies = {"scentry.auth.default.user": ""}
burp59_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp59_url, headers=burp59_headers, cookies=burp59_cookies)

#burp60_url = "https://api.blackfynn.net:443/account/api/session"
#burp60_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": #AUTHORIZATION_BEARER, "Content-Type": "application/json"}
#burp60_json={"secret": "512bc9e6-7d0d-4f6b-864b-7fa36e2706f3", "tokenId": "67edea75-b019-4623-a36c-e053a1eec8d9"}
#session.post(burp60_url, headers=burp60_headers, json=burp60_json)

burp61_url = "https://api.blackfynn.net:443/user/"
burp61_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID}
session.get(burp61_url, headers=burp61_headers)

burp62_url = "https://api.blackfynn.net:443/organizations/N%3Aorganization%3A7aae2bf7-ff15-4071-aa2a-e876ae609d3c"
burp62_cookies = {"scentry.auth.default.user": ""}
burp62_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp62_url, headers=burp62_headers, cookies=burp62_cookies)

burp63_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp63_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp63_json={"description": "a new model", "displayName": "A New Model", "locked": False, "name": "New_Model_1560722483303", "schema": [{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": None, "locked": False, "name": "an_integer", "required": False}]}
session.post(burp63_url, headers=burp63_headers, json=burp63_json)

burp64_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/bde9c7f2-7718-494b-9465-b33fb3681d66/properties"
burp64_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp64_json=[{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": None, "locked": False, "name": "an_integer", "required": False}]
session.put(burp64_url, headers=burp64_headers, json=burp64_json)

burp65_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp65_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp65_url, headers=burp65_headers)

burp66_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/bde9c7f2-7718-494b-9465-b33fb3681d66/properties"
burp66_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp66_url, headers=burp66_headers)

burp67_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp67_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp67_json={"description": "a new model", "displayName": "A New Model", "locked": False, "name": "New_Model_1560722484777", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": None, "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": None, "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": None, "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": None, "locked": False, "name": "a_string", "required": False}]}
session.post(burp67_url, headers=burp67_headers, json=burp67_json)

burp68_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp68_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp68_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": None, "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": None, "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": None, "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": None, "locked": False, "name": "a_string", "required": False}]
session.put(burp68_url, headers=burp68_headers, json=burp68_json)

burp69_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp69_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp69_url, headers=burp69_headers)

burp70_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp70_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp70_url, headers=burp70_headers)

burp71_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/bde9c7f2-7718-494b-9465-b33fb3681d66/properties"
burp71_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp71_url, headers=burp71_headers)

burp72_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f"
burp72_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp72_url, headers=burp72_headers)

burp73_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp73_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp73_url, headers=burp73_headers)

burp74_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777"
burp74_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp74_url, headers=burp74_headers)

burp75_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/properties"
burp75_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp75_url, headers=burp75_headers)

burp76_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f"
burp76_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp76_json={"description": "a new model", "displayName": "A New Model", "id": "d45851b2-c606-4c52-9cf2-11c11f12952f", "locked": False, "name": "New_Model_1560722484777", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": "f65ab8c9-3876-41d3-b6b1-0e2cab215653", "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "d168e4f3-b531-46c6-8e0e-26a90d51b933", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "534b3850-24a2-4023-9403-74b83df206fd", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "A New Property", "id": None, "locked": False, "name": "a_new_property", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "59da95ed-90a8-4276-84c8-948918a42b96", "locked": False, "name": "a_string", "required": False}]}
session.put(burp76_url, headers=burp76_headers, json=burp76_json)

burp77_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp77_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp77_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": "f65ab8c9-3876-41d3-b6b1-0e2cab215653", "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "d168e4f3-b531-46c6-8e0e-26a90d51b933", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "534b3850-24a2-4023-9403-74b83df206fd", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "A New Property", "id": None, "locked": False, "name": "a_new_property", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "59da95ed-90a8-4276-84c8-948918a42b96", "locked": False, "name": "a_string", "required": False}]
session.put(burp77_url, headers=burp77_headers, json=burp77_json)

burp78_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f"
burp78_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp78_json={"description": "a new description", "displayName": "A New Model", "id": "d45851b2-c606-4c52-9cf2-11c11f12952f", "locked": False, "name": "New_Model_1560722484777", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": "f65ab8c9-3876-41d3-b6b1-0e2cab215653", "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "d168e4f3-b531-46c6-8e0e-26a90d51b933", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "59da95ed-90a8-4276-84c8-948918a42b96", "locked": False, "name": "a_string", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "534b3850-24a2-4023-9403-74b83df206fd", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "A New Property", "id": "8ec6c74b-45b4-4e3a-a1bc-22a87d99de1d", "locked": False, "name": "a_new_property", "required": False}]}
session.put(burp78_url, headers=burp78_headers, json=burp78_json)

burp79_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp79_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp79_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": "f65ab8c9-3876-41d3-b6b1-0e2cab215653", "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "d168e4f3-b531-46c6-8e0e-26a90d51b933", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "59da95ed-90a8-4276-84c8-948918a42b96", "locked": False, "name": "a_string", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "534b3850-24a2-4023-9403-74b83df206fd", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "A New Property", "id": "8ec6c74b-45b4-4e3a-a1bc-22a87d99de1d", "locked": False, "name": "a_new_property", "required": False}]
session.put(burp79_url, headers=burp79_headers, json=burp79_json)

burp80_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f"
burp80_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp80_url, headers=burp80_headers)

burp81_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp81_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp81_url, headers=burp81_headers)

burp82_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f"
burp82_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp82_json={"description": "a new description", "displayName": "A New Model", "id": "d45851b2-c606-4c52-9cf2-11c11f12952f", "locked": False, "name": "New_Model_1560722484777", "schema": [{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "a_new_int", "id": None, "locked": False, "name": "a_new_int", "required": False}, {"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": "f65ab8c9-3876-41d3-b6b1-0e2cab215653", "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "534b3850-24a2-4023-9403-74b83df206fd", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "59da95ed-90a8-4276-84c8-948918a42b96", "locked": False, "name": "a_string", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "d168e4f3-b531-46c6-8e0e-26a90d51b933", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "a_new_float", "id": None, "locked": False, "name": "a_new_float", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "A New Property", "id": "8ec6c74b-45b4-4e3a-a1bc-22a87d99de1d", "locked": False, "name": "a_new_property", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_new_string", "id": None, "locked": False, "name": "a_new_string", "required": False}]}
session.put(burp82_url, headers=burp82_headers, json=burp82_json)

burp83_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/properties"
burp83_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp83_json=[{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "a_new_int", "id": None, "locked": False, "name": "a_new_int", "required": False}, {"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_datetime", "id": "f65ab8c9-3876-41d3-b6b1-0e2cab215653", "locked": False, "name": "a_datetime", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "534b3850-24a2-4023-9403-74b83df206fd", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "59da95ed-90a8-4276-84c8-948918a42b96", "locked": False, "name": "a_string", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "d168e4f3-b531-46c6-8e0e-26a90d51b933", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "a_new_float", "id": None, "locked": False, "name": "a_new_float", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "A New Property", "id": "8ec6c74b-45b4-4e3a-a1bc-22a87d99de1d", "locked": False, "name": "a_new_property", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_new_string", "id": None, "locked": False, "name": "a_new_string", "required": False}]
session.put(burp83_url, headers=burp83_headers, json=burp83_json)

burp84_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp84_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp84_json={"values": [{"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:01:24.113149+00:00"}, {"dataType": "boolean", "name": "a_bool", "value": True}, {"dataType": "long", "name": "an_integer", "value": 100}, {"dataType": "string", "name": "a_string", "value": "fnsdlkn#$#42nlfds$3nlds$#@$23fdsnfkls"}]}
session.post(burp84_url, headers=burp84_headers, json=burp84_json)

burp85_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp85_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp85_json={"values": [{"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:01:30.821186+00:00"}, {"dataType": "boolean", "name": "a_bool", "value": False}, {"dataType": "long", "name": "an_integer", "value": 1}, {"dataType": "string", "name": "a_string", "value": ""}]}
session.post(burp85_url, headers=burp85_headers, json=burp85_json)

burp86_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp86_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp86_json={"values": [{"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:01:31.184194+00:00"}, {"dataType": "boolean", "name": "a_bool", "value": False}, {"dataType": "long", "name": "an_integer", "value": 10000}, {"dataType": "string", "name": "a_string", "value": "43132312"}]}
session.post(burp86_url, headers=burp86_headers, json=burp86_json)

burp87_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp87_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp87_json={"values": [{"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:01:31.541126+00:00"}]}
session.post(burp87_url, headers=burp87_headers, json=burp87_json)

burp88_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp88_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp88_json={"values": [{"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:01:31.905693+00:00"}]}
session.post(burp88_url, headers=burp88_headers, json=burp88_json)

burp89_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp89_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp89_json={"values": [{"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:01:32.257671+00:00"}]}
session.post(burp89_url, headers=burp89_headers, json=burp89_json)

burp90_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp90_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp90_url, headers=burp90_headers)

burp91_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=1&offset=0"
burp91_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp91_url, headers=burp91_headers)

burp92_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=2&offset=2"
burp92_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp92_url, headers=burp92_headers)

burp93_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d45851b2-c606-4c52-9cf2-11c11f12952f/instances"
burp93_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp93_json=["20b5b127-9efb-341c-84b0-aec8195bf5b4", "38b5b127-9fb0-9884-8b04-afc7bb1293b7"]
session.delete(burp93_url, headers=burp93_headers, json=burp93_json)

burp94_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp94_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp94_url, headers=burp94_headers)

burp95_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777"
burp95_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp95_url, headers=burp95_headers)

burp96_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/properties"
burp96_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp96_url, headers=burp96_headers)

burp97_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed"
burp97_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp97_json={"values": [{"dataType": "long", "name": "a_new_int", "value": None}, {"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:10:32.126000+00:00"}, {"dataType": "long", "name": "an_integer", "value": None}, {"dataType": "string", "name": "a_string", "value": "hello"}, {"dataType": "boolean", "name": "a_bool", "value": None}, {"dataType": "double", "name": "a_new_float", "value": None}, {"dataType": "string", "name": "a_new_property", "value": None}, {"dataType": "string", "name": "a_new_string", "value": None}]}
session.put(burp97_url, headers=burp97_headers, json=burp97_json)

burp98_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed"
burp98_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp98_url, headers=burp98_headers)

burp99_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed"
burp99_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp99_json={"values": [{"dataType": "long", "name": "a_new_int", "value": None}, {"dataType": "date", "name": "a_datetime", "value": "2019-06-16T17:12:38.000000+00:00"}, {"dataType": "long", "name": "an_integer", "value": 10}, {"dataType": "string", "name": "a_string", "value": "hello"}, {"dataType": "boolean", "name": "a_bool", "value": None}, {"dataType": "double", "name": "a_new_float", "value": None}, {"dataType": "string", "name": "a_new_property", "value": None}, {"dataType": "string", "name": "a_new_string", "value": None}]}
session.put(burp99_url, headers=burp99_headers, json=burp99_json)

burp100_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances"
burp100_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp100_json={"values": [{"dataType": "string", "name": "a_string", "value": "delete me"}]}
session.post(burp100_url, headers=burp100_headers, json=burp100_json)

burp101_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp101_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp101_url, headers=burp101_headers)

burp102_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/a4b5b127-a723-54b9-42a2-d10c8610eca0"
burp102_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.delete(burp102_url, headers=burp102_headers)

burp103_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp103_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp103_url, headers=burp103_headers)

burp104_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp104_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp104_url, headers=burp104_headers)

burp105_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp105_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp105_url, headers=burp105_headers)

burp106_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp106_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp106_url, headers=burp106_headers)

burp107_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp107_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp107_url, headers=burp107_headers)

burp108_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp108_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp108_url, headers=burp108_headers)

burp109_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances?limit=100&offset=0"
burp109_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp109_url, headers=burp109_headers)

burp110_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp110_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp110_url, headers=burp110_headers)

burp111_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp111_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp111_json={"description": "a new relationship", "displayName": "New_Relationship_1560722499974", "locked": False, "name": "New_Relationship_1560722499974", "schema": [], "type": "relationship"}
session.post(burp111_url, headers=burp111_headers, json=burp111_json)

burp112_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp112_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp112_url, headers=burp112_headers)

burp113_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/c706342c-872c-4b13-8a7e-a988f1c13c2a"
burp113_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp113_url, headers=burp113_headers)

burp114_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974"
burp114_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp114_url, headers=burp114_headers)

burp115_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances"
burp115_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp115_json={"from": "36b5b127-9c27-2ee5-effe-4b13e05352cb", "to": "d8b5b127-9ce3-0a93-468f-5b474ba06169", "values": []}
session.post(burp115_url, headers=burp115_headers, json=burp115_json)

burp116_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances"
burp116_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp116_json={"from": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed", "to": "36b5b127-9c27-2ee5-effe-4b13e05352cb", "values": []}
session.post(burp116_url, headers=burp116_headers, json=burp116_json)

burp117_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances"
burp117_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp117_json={"from": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed", "to": "d8b5b127-9ce3-0a93-468f-5b474ba06169", "values": []}
session.post(burp117_url, headers=burp117_headers, json=burp117_json)

burp118_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances/batch"
burp118_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp118_json=[{"from": "d8b5b127-9ce3-0a93-468f-5b474ba06169", "to": "9eb5b127-9d94-471a-db0e-97dfa84c4d3d", "values": []}]
session.post(burp118_url, headers=burp118_headers, json=burp118_json)

burp119_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances/batch"
burp119_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp119_json=[{"from": "9eb5b127-9d94-471a-db0e-97dfa84c4d3d", "to": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed", "values": []}]
session.post(burp119_url, headers=burp119_headers, json=burp119_json)

burp120_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances/batch"
burp120_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp120_json=[{"from": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed", "to": "9eb5b127-9d94-471a-db0e-97dfa84c4d3d", "values": []}]
session.post(burp120_url, headers=burp120_headers, json=burp120_json)

burp121_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp121_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp121_url, headers=burp121_headers)

burp122_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777"
burp122_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp122_url, headers=burp122_headers)

burp123_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/properties"
burp123_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp123_url, headers=burp123_headers)

burp124_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777"
burp124_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp124_url, headers=burp124_headers)

burp125_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/properties"
burp125_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp125_url, headers=burp125_headers)

burp126_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp126_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp126_json={"description": "goes_to", "displayName": "goes_to", "from": "d45851b2-c606-4c52-9cf2-11c11f12952f", "locked": False, "name": "goes_to", "schema": [], "to": "d45851b2-c606-4c52-9cf2-11c11f12952f", "type": "relationship"}
session.post(burp126_url, headers=burp126_headers, json=burp126_json)

burp127_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/goes_to/instances/batch"
burp127_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp127_json=[{"from": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed", "to": "36b5b127-9c27-2ee5-effe-4b13e05352cb", "values": []}]
session.post(burp127_url, headers=burp127_headers, json=burp127_json)

burp128_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed/relations/New_Model_1560722484777?limit=100&offset=0"
burp128_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp128_url, headers=burp128_headers)

burp129_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed/relations/New_Model_1560722484777?limit=100&offset=100"
burp129_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp129_url, headers=burp129_headers)

burp130_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777"
burp130_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp130_url, headers=burp130_headers)

burp131_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/properties"
burp131_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp131_url, headers=burp131_headers)

burp132_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/c706342c-872c-4b13-8a7e-a988f1c13c2a/instances"
burp132_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp132_url, headers=burp132_headers)

burp133_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances"
burp133_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp133_json={"from": "36b5b127-9c27-2ee5-effe-4b13e05352cb", "to": "d8b5b127-9ce3-0a93-468f-5b474ba06169", "values": []}
session.post(burp133_url, headers=burp133_headers, json=burp133_json)

burp134_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/c706342c-872c-4b13-8a7e-a988f1c13c2a/instances"
burp134_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp134_url, headers=burp134_headers)

burp135_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722499974/instances/feb5b127-be22-f5e1-5d73-5f0506682b7e"
burp135_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.delete(burp135_url, headers=burp135_headers)

burp136_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/c706342c-872c-4b13-8a7e-a988f1c13c2a/instances"
burp136_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp136_url, headers=burp136_headers)

burp137_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/c706342c-872c-4b13-8a7e-a988f1c13c2a/instances"
burp137_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp137_url, headers=burp137_headers)

burp138_url = "https://api.blackfynn.net:443/packages"
burp138_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp138_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp138_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "test-csv", "packageType": "Tabular", "properties": []}
session.post(burp138_url, headers=burp138_headers, cookies=burp138_cookies, json=burp138_json)

burp139_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp139_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp139_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp139_json={"automaticallyProcessPackages": False, "description": "", "name": "Same Dataset, Different Name 2019-06-16 17:01:02.656173-9e95", "properties": []}
session.put(burp139_url, headers=burp139_headers, cookies=burp139_cookies, json=burp139_json)

burp140_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp140_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp140_url, headers=burp140_headers)

burp141_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp141_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp141_json={"description": "belongs_to", "displayName": "belongs_to", "locked": False, "name": "belongs_to", "schema": [], "type": "relationship"}
session.post(burp141_url, headers=burp141_headers, json=burp141_json)

burp142_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/proxy/package/instances"
burp142_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp142_json={"conceptInstanceId": "36b5b127-9c27-2ee5-effe-4b13e05352cb", "conceptType": "New_Model_1560722484777", "externalId": "N:package:2008f939-95b7-4793-9870-60c1786e535e", "targets": [{"direction": "ToTarget", "linkTarget": {"ConceptInstance": {"id": "36b5b127-9c27-2ee5-effe-4b13e05352cb"}}, "relationshipData": [], "relationshipType": "belongs_to"}]}
session.post(burp142_url, headers=burp142_headers, json=burp142_json)

burp143_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp143_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp143_url, headers=burp143_headers)

burp144_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/proxy/package/instances"
burp144_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp144_json={"conceptInstanceId": "d8b5b127-9ce3-0a93-468f-5b474ba06169", "conceptType": "New_Model_1560722484777", "externalId": "N:package:2008f939-95b7-4793-9870-60c1786e535e", "targets": [{"direction": "ToTarget", "linkTarget": {"ConceptInstance": {"id": "d8b5b127-9ce3-0a93-468f-5b474ba06169"}}, "relationshipData": [], "relationshipType": "belongs_to"}]}
session.post(burp144_url, headers=burp144_headers, json=burp144_json)

burp145_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/proxy/package/instances"
burp145_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp145_json={"conceptInstanceId": "9eb5b127-9d94-471a-db0e-97dfa84c4d3d", "conceptType": "New_Model_1560722484777", "externalId": "N:package:2008f939-95b7-4793-9870-60c1786e535e", "targets": [{"direction": "FromTarget", "linkTarget": {"ConceptInstance": {"id": "9eb5b127-9d94-471a-db0e-97dfa84c4d3d"}}, "relationshipData": [], "relationshipType": "New_Relationship_1560722499974"}]}
session.post(burp145_url, headers=burp145_headers, json=burp145_json)

burp146_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/proxy/package/instances"
burp146_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp146_json={"conceptInstanceId": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed", "conceptType": "New_Model_1560722484777", "externalId": "N:package:2008f939-95b7-4793-9870-60c1786e535e", "targets": [{"direction": "FromTarget", "linkTarget": {"ConceptInstance": {"id": "f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed"}}, "relationshipData": [], "relationshipType": "New_Relationship_1560722499974"}]}
session.post(burp146_url, headers=burp146_headers, json=burp146_json)

burp147_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed/relations/New_Model_1560722484777?limit=100&offset=0"
burp147_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp147_url, headers=burp147_headers)

burp148_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/instances/f0b5b127-9e4c-492f-9ad9-a92cfef0e4ed/relations/New_Model_1560722484777?limit=100&offset=100"
burp148_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp148_url, headers=burp148_headers)

burp149_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777"
burp149_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp149_url, headers=burp149_headers)

burp150_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/New_Model_1560722484777/properties"
burp150_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp150_url, headers=burp150_headers)

burp151_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp151_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp151_json={"description": "a new description", "displayName": "Basic_Props_1", "locked": False, "name": "Basic_Props_1", "schema": [{"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": None, "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": None, "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_date", "id": None, "locked": False, "name": "a_date", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": None, "locked": False, "name": "a_string", "required": False}]}
session.post(burp151_url, headers=burp151_headers, json=burp151_json)

burp152_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4/properties"
burp152_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp152_json=[{"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": None, "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": None, "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_date", "id": None, "locked": False, "name": "a_date", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": None, "locked": False, "name": "a_string", "required": False}]
session.put(burp152_url, headers=burp152_headers, json=burp152_json)

burp153_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4"
burp153_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp153_url, headers=burp153_headers)

burp154_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4/properties"
burp154_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp154_url, headers=burp154_headers)

burp155_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4"
burp155_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp155_json={"description": "a new description", "displayName": "Basic_Props_1", "id": "4330a0f7-ce11-4b00-bcca-cac2175198a4", "locked": False, "name": "Basic_Props_1", "schema": [{"conceptTitle": False, "dataType": "double", "default": True, "description": "some metric", "displayName": "Weight", "id": None, "locked": False, "name": "a_new_property", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "2514e3f5-9148-4406-a008-43039470dd7d", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "ab827323-adc2-40b3-8eea-26f523398176", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_date", "id": "96ae7049-127c-4fdb-8f9e-5b66b69ab9b9", "locked": False, "name": "a_date", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "007f73af-2049-4ae5-aeb4-d18ea63717f7", "locked": False, "name": "a_string", "required": False}]}
session.put(burp155_url, headers=burp155_headers, json=burp155_json)

burp156_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4/properties"
burp156_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp156_json=[{"conceptTitle": False, "dataType": "double", "default": True, "description": "some metric", "displayName": "Weight", "id": None, "locked": False, "name": "a_new_property", "required": False}, {"conceptTitle": False, "dataType": "boolean", "default": True, "description": "", "displayName": "a_bool", "id": "2514e3f5-9148-4406-a008-43039470dd7d", "locked": False, "name": "a_bool", "required": False}, {"conceptTitle": True, "dataType": "long", "default": True, "description": "", "displayName": "An Integer", "id": "ab827323-adc2-40b3-8eea-26f523398176", "locked": False, "name": "an_integer", "required": False}, {"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "a_date", "id": "96ae7049-127c-4fdb-8f9e-5b66b69ab9b9", "locked": False, "name": "a_date", "required": False}, {"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "a_string", "id": "007f73af-2049-4ae5-aeb4-d18ea63717f7", "locked": False, "name": "a_string", "required": False}]
session.put(burp156_url, headers=burp156_headers, json=burp156_json)

burp157_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4"
burp157_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp157_url, headers=burp157_headers)

burp158_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/4330a0f7-ce11-4b00-bcca-cac2175198a4/properties"
burp158_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp158_url, headers=burp158_headers)

burp159_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp159_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp159_json={"description": "a new description", "displayName": "Basic_Props_2", "locked": False, "name": "Basic_Props_2", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": None, "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": True}]}
session.post(burp159_url, headers=burp159_headers, json=burp159_json)

burp160_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c/properties"
burp160_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp160_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": None, "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": True}]
session.put(burp160_url, headers=burp160_headers, json=burp160_json)

burp161_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c"
burp161_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp161_url, headers=burp161_headers)

burp162_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c/properties"
burp162_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp162_url, headers=burp162_headers)

burp163_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c"
burp163_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp163_json={"description": "a new description", "displayName": "Basic_Props_2", "id": "8db9fa1d-8711-4453-beb1-8c81e69c6e1c", "locked": False, "name": "Basic_Props_2", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": "0a88c109-2795-4a97-9b38-4ddfd52c494c", "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "24ea0f89-a38f-4795-9333-c5a7d8c7c68b", "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "6610f6f0-1e1f-4e48-93d0-86246ef4f4fa", "locked": False, "name": "name", "required": True}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight2", "required": False}]}
session.put(burp163_url, headers=burp163_headers, json=burp163_json)

burp164_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c/properties"
burp164_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp164_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": "0a88c109-2795-4a97-9b38-4ddfd52c494c", "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "24ea0f89-a38f-4795-9333-c5a7d8c7c68b", "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "6610f6f0-1e1f-4e48-93d0-86246ef4f4fa", "locked": False, "name": "name", "required": True}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight2", "required": False}]
session.put(burp164_url, headers=burp164_headers, json=burp164_json)

burp165_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c"
burp165_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp165_url, headers=burp165_headers)

burp166_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/8db9fa1d-8711-4453-beb1-8c81e69c6e1c/properties"
burp166_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp166_url, headers=burp166_headers)

burp167_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp167_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp167_json={"description": "a new description", "displayName": "Basic_Props_3", "locked": False, "name": "Basic_Props_3", "schema": [{"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "DOB", "id": None, "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}]}
session.post(burp167_url, headers=burp167_headers, json=burp167_json)

burp168_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b/properties"
burp168_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp168_json=[{"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "DOB", "id": None, "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}]
session.put(burp168_url, headers=burp168_headers, json=burp168_json)

burp169_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b"
burp169_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp169_url, headers=burp169_headers)

burp170_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b/properties"
burp170_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp170_url, headers=burp170_headers)

burp171_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b"
burp171_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp171_json={"description": "a new description", "displayName": "Basic_Props_3", "id": "62e13cff-a038-4512-9df9-481a106ae92b", "locked": False, "name": "Basic_Props_3", "schema": [{"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "DOB", "id": "64694190-6572-469d-90f8-6919a1844b10", "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "ac7c91cb-1b62-4b41-9fd2-59e103a44170", "locked": False, "name": "age", "required": False}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight3", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "82dc0e0a-c8e4-4db1-bdea-46fbb0eea4cd", "locked": False, "name": "name", "required": False}]}
session.put(burp171_url, headers=burp171_headers, json=burp171_json)

burp172_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b/properties"
burp172_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp172_json=[{"conceptTitle": False, "dataType": "string", "default": True, "description": "", "displayName": "DOB", "id": "64694190-6572-469d-90f8-6919a1844b10", "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "ac7c91cb-1b62-4b41-9fd2-59e103a44170", "locked": False, "name": "age", "required": False}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight3", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "82dc0e0a-c8e4-4db1-bdea-46fbb0eea4cd", "locked": False, "name": "name", "required": False}]
session.put(burp172_url, headers=burp172_headers, json=burp172_json)

burp173_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b"
burp173_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp173_url, headers=burp173_headers)

burp174_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/62e13cff-a038-4512-9df9-481a106ae92b/properties"
burp174_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp174_url, headers=burp174_headers)

burp175_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp175_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp175_json={"description": "a new description", "displayName": "Basic_Props_4", "locked": False, "name": "Basic_Props_4", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": None, "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": True}]}
session.post(burp175_url, headers=burp175_headers, json=burp175_json)

burp176_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061/properties"
burp176_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp176_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": None, "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": True}]
session.put(burp176_url, headers=burp176_headers, json=burp176_json)

burp177_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061"
burp177_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp177_url, headers=burp177_headers)

burp178_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061/properties"
burp178_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp178_url, headers=burp178_headers)

burp179_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061"
burp179_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp179_json={"description": "a new description", "displayName": "Basic_Props_4", "id": "a2acf9b3-0765-49ef-8473-476f4bf45061", "locked": False, "name": "Basic_Props_4", "schema": [{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": "56de5bb0-f743-4b73-8dcd-d3c644eb084b", "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "2f055d18-2a45-4815-bf49-f155bc880eba", "locked": False, "name": "age", "required": False}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight4", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "fb5633ab-2239-4ba4-bae6-ec27ea23f686", "locked": False, "name": "name", "required": True}]}
session.put(burp179_url, headers=burp179_headers, json=burp179_json)

burp180_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061/properties"
burp180_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp180_json=[{"conceptTitle": False, "dataType": "date", "default": True, "description": "", "displayName": "DOB", "id": "56de5bb0-f743-4b73-8dcd-d3c644eb084b", "locked": False, "name": "DOB", "required": False}, {"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "2f055d18-2a45-4815-bf49-f155bc880eba", "locked": False, "name": "age", "required": False}, {"conceptTitle": False, "dataType": "double", "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight4", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "fb5633ab-2239-4ba4-bae6-ec27ea23f686", "locked": False, "name": "name", "required": True}]
session.put(burp180_url, headers=burp180_headers, json=burp180_json)

burp181_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061"
burp181_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp181_url, headers=burp181_headers)

burp182_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/a2acf9b3-0765-49ef-8473-476f4bf45061/properties"
burp182_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp182_url, headers=burp182_headers)

burp183_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp183_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp183_json={"description": "a new description", "displayName": "Complex_Props", "locked": False, "name": "Complex_Props", "schema": [{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}, {"conceptTitle": False, "dataType": {"format": "email", "type": "string", "unit": None}, "default": True, "description": "", "displayName": "email", "id": None, "locked": False, "name": "email", "required": False}]}
session.post(burp183_url, headers=burp183_headers, json=burp183_json)

burp184_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5/properties"
burp184_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp184_json=[{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": None, "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}, {"conceptTitle": False, "dataType": {"format": "email", "type": "string", "unit": None}, "default": True, "description": "", "displayName": "email", "id": None, "locked": False, "name": "email", "required": False}]
session.put(burp184_url, headers=burp184_headers, json=burp184_json)

burp185_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5"
burp185_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp185_url, headers=burp185_headers)

burp186_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5/properties"
burp186_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp186_url, headers=burp186_headers)

burp187_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5"
burp187_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp187_json={"description": "a new description", "displayName": "Complex_Props", "id": "dc05231e-a384-41bb-8e1a-10e8af025cc5", "locked": False, "name": "Complex_Props", "schema": [{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "ee51aa1d-e0c7-4b56-8f6c-e98d98226478", "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "34b2adfa-99a7-4bc8-9536-17cf2b743112", "locked": False, "name": "name", "required": False}, {"conceptTitle": False, "dataType": {"format": None, "type": "double", "unit": "kg"}, "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight", "required": False}, {"conceptTitle": False, "dataType": {"format": "Email", "type": "string", "unit": None}, "default": True, "description": "", "displayName": "email", "id": "10627ed4-5b77-400b-9d36-035972e446c3", "locked": False, "name": "email", "required": False}]}
session.put(burp187_url, headers=burp187_headers, json=burp187_json)

burp188_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5/properties"
burp188_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp188_json=[{"conceptTitle": False, "dataType": "long", "default": True, "description": "", "displayName": "age", "id": "ee51aa1d-e0c7-4b56-8f6c-e98d98226478", "locked": False, "name": "age", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": "34b2adfa-99a7-4bc8-9536-17cf2b743112", "locked": False, "name": "name", "required": False}, {"conceptTitle": False, "dataType": {"format": None, "type": "double", "unit": "kg"}, "default": True, "description": "", "displayName": "Weight", "id": None, "locked": False, "name": "weight", "required": False}, {"conceptTitle": False, "dataType": {"format": "Email", "type": "string", "unit": None}, "default": True, "description": "", "displayName": "email", "id": "10627ed4-5b77-400b-9d36-035972e446c3", "locked": False, "name": "email", "required": False}]
session.put(burp188_url, headers=burp188_headers, json=burp188_json)

burp189_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5"
burp189_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp189_url, headers=burp189_headers)

burp190_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/dc05231e-a384-41bb-8e1a-10e8af025cc5/properties"
burp190_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp190_url, headers=burp190_headers)

burp191_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/Complex_Props/instances"
burp191_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp191_json={"values": [{"dataType": "long", "name": "age", "value": 1}, {"dataType": "string", "name": "name", "value": "Bob"}, {"dataType": "double", "name": "weight", "value": 10.0}, {"dataType": "string", "name": "email", "value": "test@test.com"}]}
session.post(burp191_url, headers=burp191_headers, json=burp191_json)

burp192_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/Complex_Props/instances"
burp192_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp192_json={"values": [{"dataType": "long", "name": "age", "value": 1}, {"dataType": "string", "name": "name", "value": "Bob"}, {"dataType": "double", "name": "weight", "value": 10.0}, {"dataType": "string", "name": "email", "value": "123455"}]}
session.post(burp192_url, headers=burp192_headers, json=burp192_json)

burp193_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp193_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp193_json={"description": "model a", "displayName": "Model_A", "locked": False, "name": "Model_A", "schema": [{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]}
session.post(burp193_url, headers=burp193_headers, json=burp193_json)

burp194_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/properties"
burp194_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp194_json=[{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]
session.put(burp194_url, headers=burp194_headers, json=burp194_json)

burp195_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/related"
burp195_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp195_url, headers=burp195_headers)

burp196_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp196_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp196_json={"description": "model b", "displayName": "Model_B", "locked": False, "name": "Model_B", "schema": [{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]}
session.post(burp196_url, headers=burp196_headers, json=burp196_json)

burp197_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/properties"
burp197_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp197_json=[{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]
session.put(burp197_url, headers=burp197_headers, json=burp197_json)

burp198_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp198_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp198_json={"description": "a new relationship", "displayName": "New_Relationship_1560722530285", "locked": False, "name": "New_Relationship_1560722530285", "schema": [], "type": "relationship"}
session.post(burp198_url, headers=burp198_headers, json=burp198_json)

burp199_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/Model_A/instances"
burp199_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp199_json={"values": [{"dataType": "string", "name": "prop1", "value": "val1"}]}
session.post(burp199_url, headers=burp199_headers, json=burp199_json)

burp200_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/Model_B/instances"
burp200_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp200_json={"values": [{"dataType": "string", "name": "prop1", "value": "val1"}]}
session.post(burp200_url, headers=burp200_headers, json=burp200_json)

burp201_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/New_Relationship_1560722530285/instances/batch"
burp201_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp201_json=[{"from": "f2b5b127-ea98-09fe-3544-fdf5540ca554", "to": "7cb5b127-eb47-bf88-9fe3-fdfd99052f60", "values": []}]
session.post(burp201_url, headers=burp201_headers, json=burp201_json)

burp202_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/related"
burp202_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp202_url, headers=burp202_headers)

burp203_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/properties"
burp203_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp203_url, headers=burp203_headers)

burp204_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/properties"
burp204_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp204_url, headers=burp204_headers)

burp205_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/related"
burp205_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp205_url, headers=burp205_headers)

burp206_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/properties"
burp206_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp206_url, headers=burp206_headers)

burp207_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/properties"
burp207_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp207_url, headers=burp207_headers)

burp208_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/related"
burp208_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp208_url, headers=burp208_headers)

burp209_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/properties"
burp209_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp209_url, headers=burp209_headers)

burp210_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/properties"
burp210_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp210_url, headers=burp210_headers)

burp211_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/related"
burp211_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp211_url, headers=burp211_headers)

burp212_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/77f557b5-a6c9-4e3b-960e-e405b2f80d2d/properties"
burp212_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp212_url, headers=burp212_headers)

burp213_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/d623ab20-3216-435a-b735-7dd37f7e3939/properties"
burp213_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp213_url, headers=burp213_headers)

burp214_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp214_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp214_json={"description": "a new description", "displayName": "Enum_Props", "locked": False, "name": "Enum_Props", "schema": [{"conceptTitle": False, "dataType": {"items": {"enum": ["foo", "bar", "baz"], "format": None, "type": "string", "unit": None}, "type": "array"}, "default": True, "description": "", "displayName": "some_array", "id": None, "locked": False, "name": "some_array", "required": False}, {"conceptTitle": False, "dataType": {"items": {"enum": [1.0, 2.0, 3.0], "format": None, "type": "double", "unit": "cm"}, "type": "enum"}, "default": True, "description": "", "displayName": "some_enum", "id": None, "locked": False, "name": "some_enum", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}, {"conceptTitle": False, "dataType": {"items": {"enum": None, "format": None, "type": "long", "unit": None}, "type": "array"}, "default": True, "description": "", "displayName": "non_enum_array", "id": None, "locked": False, "name": "non_enum_array", "required": False}]}
session.post(burp214_url, headers=burp214_headers, json=burp214_json)

burp215_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/68dc2d5f-9f84-4624-a3bc-23b91a70863d/properties"
burp215_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp215_json=[{"conceptTitle": False, "dataType": {"items": {"enum": ["foo", "bar", "baz"], "format": None, "type": "string", "unit": None}, "type": "array"}, "default": True, "description": "", "displayName": "some_array", "id": None, "locked": False, "name": "some_array", "required": False}, {"conceptTitle": False, "dataType": {"items": {"enum": [1.0, 2.0, 3.0], "format": None, "type": "double", "unit": "cm"}, "type": "enum"}, "default": True, "description": "", "displayName": "some_enum", "id": None, "locked": False, "name": "some_enum", "required": False}, {"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}, {"conceptTitle": False, "dataType": {"items": {"enum": None, "format": None, "type": "long", "unit": None}, "type": "array"}, "default": True, "description": "", "displayName": "non_enum_array", "id": None, "locked": False, "name": "non_enum_array", "required": False}]
session.put(burp215_url, headers=burp215_headers, json=burp215_json)

burp216_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/68dc2d5f-9f84-4624-a3bc-23b91a70863d"
burp216_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp216_url, headers=burp216_headers)

burp217_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/68dc2d5f-9f84-4624-a3bc-23b91a70863d/properties"
burp217_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp217_url, headers=burp217_headers)

burp218_url = "https://api.blackfynn.net:443/datasets/"
burp218_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp218_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp218_url, headers=burp218_headers, cookies=burp218_cookies)

burp219_url = "https://api.blackfynn.net:443/datasets"
burp219_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp219_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp219_json={"automaticallyProcessPackages": False, "description": "", "name": "test_dataset_1560722537165", "properties": []}
session.post(burp219_url, headers=burp219_headers, cookies=burp219_cookies, json=burp219_json)

burp220_url = "https://api.blackfynn.net:443/datasets/"
burp220_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp220_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp220_url, headers=burp220_headers, cookies=burp220_cookies)

burp221_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts"
burp221_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp221_json={"description": "model a", "displayName": "Model_A", "locked": False, "name": "Model_A", "schema": [{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]}
session.post(burp221_url, headers=burp221_headers, json=burp221_json)

burp222_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/62946296-0b69-47b6-819e-bbd06270d7cb/properties"
burp222_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp222_json=[{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]
session.put(burp222_url, headers=burp222_headers, json=burp222_json)

burp223_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts"
burp223_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp223_json={"description": "model b", "displayName": "Model_B", "locked": False, "name": "Model_B", "schema": [{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]}
session.post(burp223_url, headers=burp223_headers, json=burp223_json)

burp224_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/4f2ad7c5-6503-4741-b54a-404e650e68e2/properties"
burp224_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp224_json=[{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "prop1", "id": None, "locked": False, "name": "prop1", "required": False}]
session.put(burp224_url, headers=burp224_headers, json=burp224_json)

burp225_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/relationships"
burp225_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp225_json={"description": "a new relationship", "displayName": "New_Relationship_1560722540398", "locked": False, "name": "New_Relationship_1560722540398", "schema": [], "type": "relationship"}
session.post(burp225_url, headers=burp225_headers, json=burp225_json)

burp226_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/Model_A/instances"
burp226_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp226_json={"values": [{"dataType": "string", "name": "prop1", "value": "val1"}]}
session.post(burp226_url, headers=burp226_headers, json=burp226_json)

burp227_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/Model_B/instances"
burp227_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp227_json={"values": [{"dataType": "string", "name": "prop1", "value": "val1"}]}
session.post(burp227_url, headers=burp227_headers, json=burp227_json)

burp228_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/relationships/New_Relationship_1560722540398/instances/batch"
burp228_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp228_json=[{"from": "8ab5b127-fe78-e082-48a9-f9f8f6c996b7", "to": "92b5b127-ff27-eba3-56c3-03fb82091013", "values": []}]
session.post(burp228_url, headers=burp228_headers, json=burp228_json)

burp229_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/62946296-0b69-47b6-819e-bbd06270d7cb/topology"
burp229_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp229_url, headers=burp229_headers)

burp230_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/4f2ad7c5-6503-4741-b54a-404e650e68e2/properties"
burp230_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp230_url, headers=burp230_headers)

burp231_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp231_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp231_json={"description": "patient", "displayName": "patient", "locked": False, "name": "patient", "schema": [{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}]}
session.post(burp231_url, headers=burp231_headers, json=burp231_json)

burp232_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/767f8f43-a74f-4b9e-9a13-7ed3eb7b832b/properties"
burp232_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp232_json=[{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "name", "id": None, "locked": False, "name": "name", "required": False}]
session.put(burp232_url, headers=burp232_headers, json=burp232_json)

burp233_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts"
burp233_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp233_json={"description": "visit", "displayName": "visit", "locked": False, "name": "visit", "schema": [{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "field", "id": None, "locked": False, "name": "field", "required": False}]}
session.post(burp233_url, headers=burp233_headers, json=burp233_json)

burp234_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/e4ebb347-6d06-4849-a413-fe68e7452394/properties"
burp234_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp234_json=[{"conceptTitle": True, "dataType": "string", "default": True, "description": "", "displayName": "field", "id": None, "locked": False, "name": "field", "required": False}]
session.put(burp234_url, headers=burp234_headers, json=burp234_json)

burp235_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships"
burp235_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp235_json={"description": "an attendance", "displayName": "attends", "locked": False, "name": "attends", "schema": [], "type": "relationship"}
session.post(burp235_url, headers=burp235_headers, json=burp235_json)

burp236_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/patient/instances"
burp236_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp236_json={"values": [{"dataType": "string", "name": "name", "value": "Fred"}]}
session.post(burp236_url, headers=burp236_headers, json=burp236_json)

burp237_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/visit/instances/batch"
burp237_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp237_json=[{"values": [{"dataType": "string", "name": "field", "value": "0"}]}, {"values": [{"dataType": "string", "name": "field", "value": "1"}]}, {"values": [{"dataType": "string", "name": "field", "value": "2"}]}, {"values": [{"dataType": "string", "name": "field", "value": "3"}]}, {"values": [{"dataType": "string", "name": "field", "value": "4"}]}, {"values": [{"dataType": "string", "name": "field", "value": "5"}]}, {"values": [{"dataType": "string", "name": "field", "value": "6"}]}, {"values": [{"dataType": "string", "name": "field", "value": "7"}]}, {"values": [{"dataType": "string", "name": "field", "value": "8"}]}, {"values": [{"dataType": "string", "name": "field", "value": "9"}]}, {"values": [{"dataType": "string", "name": "field", "value": "10"}]}, {"values": [{"dataType": "string", "name": "field", "value": "11"}]}, {"values": [{"dataType": "string", "name": "field", "value": "12"}]}, {"values": [{"dataType": "string", "name": "field", "value": "13"}]}, {"values": [{"dataType": "string", "name": "field", "value": "14"}]}, {"values": [{"dataType": "string", "name": "field", "value": "15"}]}, {"values": [{"dataType": "string", "name": "field", "value": "16"}]}, {"values": [{"dataType": "string", "name": "field", "value": "17"}]}, {"values": [{"dataType": "string", "name": "field", "value": "18"}]}, {"values": [{"dataType": "string", "name": "field", "value": "19"}]}, {"values": [{"dataType": "string", "name": "field", "value": "20"}]}, {"values": [{"dataType": "string", "name": "field", "value": "21"}]}, {"values": [{"dataType": "string", "name": "field", "value": "22"}]}, {"values": [{"dataType": "string", "name": "field", "value": "23"}]}, {"values": [{"dataType": "string", "name": "field", "value": "24"}]}, {"values": [{"dataType": "string", "name": "field", "value": "25"}]}, {"values": [{"dataType": "string", "name": "field", "value": "26"}]}, {"values": [{"dataType": "string", "name": "field", "value": "27"}]}, {"values": [{"dataType": "string", "name": "field", "value": "28"}]}, {"values": [{"dataType": "string", "name": "field", "value": "29"}]}, {"values": [{"dataType": "string", "name": "field", "value": "30"}]}, {"values": [{"dataType": "string", "name": "field", "value": "31"}]}, {"values": [{"dataType": "string", "name": "field", "value": "32"}]}, {"values": [{"dataType": "string", "name": "field", "value": "33"}]}, {"values": [{"dataType": "string", "name": "field", "value": "34"}]}, {"values": [{"dataType": "string", "name": "field", "value": "35"}]}, {"values": [{"dataType": "string", "name": "field", "value": "36"}]}, {"values": [{"dataType": "string", "name": "field", "value": "37"}]}, {"values": [{"dataType": "string", "name": "field", "value": "38"}]}, {"values": [{"dataType": "string", "name": "field", "value": "39"}]}, {"values": [{"dataType": "string", "name": "field", "value": "40"}]}, {"values": [{"dataType": "string", "name": "field", "value": "41"}]}, {"values": [{"dataType": "string", "name": "field", "value": "42"}]}, {"values": [{"dataType": "string", "name": "field", "value": "43"}]}, {"values": [{"dataType": "string", "name": "field", "value": "44"}]}, {"values": [{"dataType": "string", "name": "field", "value": "45"}]}, {"values": [{"dataType": "string", "name": "field", "value": "46"}]}, {"values": [{"dataType": "string", "name": "field", "value": "47"}]}, {"values": [{"dataType": "string", "name": "field", "value": "48"}]}, {"values": [{"dataType": "string", "name": "field", "value": "49"}]}, {"values": [{"dataType": "string", "name": "field", "value": "50"}]}, {"values": [{"dataType": "string", "name": "field", "value": "51"}]}, {"values": [{"dataType": "string", "name": "field", "value": "52"}]}, {"values": [{"dataType": "string", "name": "field", "value": "53"}]}, {"values": [{"dataType": "string", "name": "field", "value": "54"}]}, {"values": [{"dataType": "string", "name": "field", "value": "55"}]}, {"values": [{"dataType": "string", "name": "field", "value": "56"}]}, {"values": [{"dataType": "string", "name": "field", "value": "57"}]}, {"values": [{"dataType": "string", "name": "field", "value": "58"}]}, {"values": [{"dataType": "string", "name": "field", "value": "59"}]}, {"values": [{"dataType": "string", "name": "field", "value": "60"}]}, {"values": [{"dataType": "string", "name": "field", "value": "61"}]}, {"values": [{"dataType": "string", "name": "field", "value": "62"}]}, {"values": [{"dataType": "string", "name": "field", "value": "63"}]}, {"values": [{"dataType": "string", "name": "field", "value": "64"}]}, {"values": [{"dataType": "string", "name": "field", "value": "65"}]}, {"values": [{"dataType": "string", "name": "field", "value": "66"}]}, {"values": [{"dataType": "string", "name": "field", "value": "67"}]}, {"values": [{"dataType": "string", "name": "field", "value": "68"}]}, {"values": [{"dataType": "string", "name": "field", "value": "69"}]}, {"values": [{"dataType": "string", "name": "field", "value": "70"}]}, {"values": [{"dataType": "string", "name": "field", "value": "71"}]}, {"values": [{"dataType": "string", "name": "field", "value": "72"}]}, {"values": [{"dataType": "string", "name": "field", "value": "73"}]}, {"values": [{"dataType": "string", "name": "field", "value": "74"}]}, {"values": [{"dataType": "string", "name": "field", "value": "75"}]}, {"values": [{"dataType": "string", "name": "field", "value": "76"}]}, {"values": [{"dataType": "string", "name": "field", "value": "77"}]}, {"values": [{"dataType": "string", "name": "field", "value": "78"}]}, {"values": [{"dataType": "string", "name": "field", "value": "79"}]}, {"values": [{"dataType": "string", "name": "field", "value": "80"}]}, {"values": [{"dataType": "string", "name": "field", "value": "81"}]}, {"values": [{"dataType": "string", "name": "field", "value": "82"}]}, {"values": [{"dataType": "string", "name": "field", "value": "83"}]}, {"values": [{"dataType": "string", "name": "field", "value": "84"}]}, {"values": [{"dataType": "string", "name": "field", "value": "85"}]}, {"values": [{"dataType": "string", "name": "field", "value": "86"}]}, {"values": [{"dataType": "string", "name": "field", "value": "87"}]}, {"values": [{"dataType": "string", "name": "field", "value": "88"}]}, {"values": [{"dataType": "string", "name": "field", "value": "89"}]}, {"values": [{"dataType": "string", "name": "field", "value": "90"}]}, {"values": [{"dataType": "string", "name": "field", "value": "91"}]}, {"values": [{"dataType": "string", "name": "field", "value": "92"}]}, {"values": [{"dataType": "string", "name": "field", "value": "93"}]}, {"values": [{"dataType": "string", "name": "field", "value": "94"}]}, {"values": [{"dataType": "string", "name": "field", "value": "95"}]}, {"values": [{"dataType": "string", "name": "field", "value": "96"}]}, {"values": [{"dataType": "string", "name": "field", "value": "97"}]}, {"values": [{"dataType": "string", "name": "field", "value": "98"}]}, {"values": [{"dataType": "string", "name": "field", "value": "99"}]}, {"values": [{"dataType": "string", "name": "field", "value": "100"}]}, {"values": [{"dataType": "string", "name": "field", "value": "101"}]}, {"values": [{"dataType": "string", "name": "field", "value": "102"}]}, {"values": [{"dataType": "string", "name": "field", "value": "103"}]}, {"values": [{"dataType": "string", "name": "field", "value": "104"}]}, {"values": [{"dataType": "string", "name": "field", "value": "105"}]}, {"values": [{"dataType": "string", "name": "field", "value": "106"}]}, {"values": [{"dataType": "string", "name": "field", "value": "107"}]}, {"values": [{"dataType": "string", "name": "field", "value": "108"}]}, {"values": [{"dataType": "string", "name": "field", "value": "109"}]}, {"values": [{"dataType": "string", "name": "field", "value": "110"}]}, {"values": [{"dataType": "string", "name": "field", "value": "111"}]}, {"values": [{"dataType": "string", "name": "field", "value": "112"}]}, {"values": [{"dataType": "string", "name": "field", "value": "113"}]}, {"values": [{"dataType": "string", "name": "field", "value": "114"}]}, {"values": [{"dataType": "string", "name": "field", "value": "115"}]}, {"values": [{"dataType": "string", "name": "field", "value": "116"}]}, {"values": [{"dataType": "string", "name": "field", "value": "117"}]}, {"values": [{"dataType": "string", "name": "field", "value": "118"}]}, {"values": [{"dataType": "string", "name": "field", "value": "119"}]}, {"values": [{"dataType": "string", "name": "field", "value": "120"}]}, {"values": [{"dataType": "string", "name": "field", "value": "121"}]}, {"values": [{"dataType": "string", "name": "field", "value": "122"}]}, {"values": [{"dataType": "string", "name": "field", "value": "123"}]}, {"values": [{"dataType": "string", "name": "field", "value": "124"}]}, {"values": [{"dataType": "string", "name": "field", "value": "125"}]}, {"values": [{"dataType": "string", "name": "field", "value": "126"}]}, {"values": [{"dataType": "string", "name": "field", "value": "127"}]}, {"values": [{"dataType": "string", "name": "field", "value": "128"}]}, {"values": [{"dataType": "string", "name": "field", "value": "129"}]}, {"values": [{"dataType": "string", "name": "field", "value": "130"}]}, {"values": [{"dataType": "string", "name": "field", "value": "131"}]}, {"values": [{"dataType": "string", "name": "field", "value": "132"}]}, {"values": [{"dataType": "string", "name": "field", "value": "133"}]}, {"values": [{"dataType": "string", "name": "field", "value": "134"}]}, {"values": [{"dataType": "string", "name": "field", "value": "135"}]}, {"values": [{"dataType": "string", "name": "field", "value": "136"}]}, {"values": [{"dataType": "string", "name": "field", "value": "137"}]}, {"values": [{"dataType": "string", "name": "field", "value": "138"}]}, {"values": [{"dataType": "string", "name": "field", "value": "139"}]}, {"values": [{"dataType": "string", "name": "field", "value": "140"}]}, {"values": [{"dataType": "string", "name": "field", "value": "141"}]}, {"values": [{"dataType": "string", "name": "field", "value": "142"}]}, {"values": [{"dataType": "string", "name": "field", "value": "143"}]}, {"values": [{"dataType": "string", "name": "field", "value": "144"}]}, {"values": [{"dataType": "string", "name": "field", "value": "145"}]}, {"values": [{"dataType": "string", "name": "field", "value": "146"}]}, {"values": [{"dataType": "string", "name": "field", "value": "147"}]}, {"values": [{"dataType": "string", "name": "field", "value": "148"}]}, {"values": [{"dataType": "string", "name": "field", "value": "149"}]}, {"values": [{"dataType": "string", "name": "field", "value": "150"}]}, {"values": [{"dataType": "string", "name": "field", "value": "151"}]}, {"values": [{"dataType": "string", "name": "field", "value": "152"}]}, {"values": [{"dataType": "string", "name": "field", "value": "153"}]}, {"values": [{"dataType": "string", "name": "field", "value": "154"}]}, {"values": [{"dataType": "string", "name": "field", "value": "155"}]}, {"values": [{"dataType": "string", "name": "field", "value": "156"}]}, {"values": [{"dataType": "string", "name": "field", "value": "157"}]}, {"values": [{"dataType": "string", "name": "field", "value": "158"}]}, {"values": [{"dataType": "string", "name": "field", "value": "159"}]}, {"values": [{"dataType": "string", "name": "field", "value": "160"}]}, {"values": [{"dataType": "string", "name": "field", "value": "161"}]}, {"values": [{"dataType": "string", "name": "field", "value": "162"}]}, {"values": [{"dataType": "string", "name": "field", "value": "163"}]}, {"values": [{"dataType": "string", "name": "field", "value": "164"}]}, {"values": [{"dataType": "string", "name": "field", "value": "165"}]}, {"values": [{"dataType": "string", "name": "field", "value": "166"}]}, {"values": [{"dataType": "string", "name": "field", "value": "167"}]}, {"values": [{"dataType": "string", "name": "field", "value": "168"}]}, {"values": [{"dataType": "string", "name": "field", "value": "169"}]}, {"values": [{"dataType": "string", "name": "field", "value": "170"}]}, {"values": [{"dataType": "string", "name": "field", "value": "171"}]}, {"values": [{"dataType": "string", "name": "field", "value": "172"}]}, {"values": [{"dataType": "string", "name": "field", "value": "173"}]}, {"values": [{"dataType": "string", "name": "field", "value": "174"}]}, {"values": [{"dataType": "string", "name": "field", "value": "175"}]}, {"values": [{"dataType": "string", "name": "field", "value": "176"}]}, {"values": [{"dataType": "string", "name": "field", "value": "177"}]}, {"values": [{"dataType": "string", "name": "field", "value": "178"}]}, {"values": [{"dataType": "string", "name": "field", "value": "179"}]}, {"values": [{"dataType": "string", "name": "field", "value": "180"}]}, {"values": [{"dataType": "string", "name": "field", "value": "181"}]}, {"values": [{"dataType": "string", "name": "field", "value": "182"}]}, {"values": [{"dataType": "string", "name": "field", "value": "183"}]}, {"values": [{"dataType": "string", "name": "field", "value": "184"}]}, {"values": [{"dataType": "string", "name": "field", "value": "185"}]}, {"values": [{"dataType": "string", "name": "field", "value": "186"}]}, {"values": [{"dataType": "string", "name": "field", "value": "187"}]}, {"values": [{"dataType": "string", "name": "field", "value": "188"}]}, {"values": [{"dataType": "string", "name": "field", "value": "189"}]}, {"values": [{"dataType": "string", "name": "field", "value": "190"}]}, {"values": [{"dataType": "string", "name": "field", "value": "191"}]}, {"values": [{"dataType": "string", "name": "field", "value": "192"}]}, {"values": [{"dataType": "string", "name": "field", "value": "193"}]}, {"values": [{"dataType": "string", "name": "field", "value": "194"}]}, {"values": [{"dataType": "string", "name": "field", "value": "195"}]}, {"values": [{"dataType": "string", "name": "field", "value": "196"}]}, {"values": [{"dataType": "string", "name": "field", "value": "197"}]}, {"values": [{"dataType": "string", "name": "field", "value": "198"}]}, {"values": [{"dataType": "string", "name": "field", "value": "199"}]}]
session.post(burp237_url, headers=burp237_headers, json=burp237_json)

burp238_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/relationships/attends/instances/batch"
burp238_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp238_json=[{"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6cb5b128-05b3-3699-02bd-753b5ff8dc86", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "78b5b128-05c2-45a8-b22f-f6b1a201d998", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "dcb5b128-05d1-6618-92a3-0e13bb30ad23", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "78b5b128-05df-3e3d-02a3-41d8fb871ec3", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1eb5b128-05ed-399c-782b-9761c409f385", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5ab5b128-05fa-f2fc-0b95-041c8d985c05", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "7cb5b128-0607-8ba5-427b-4bb38bb6f1d6", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "36b5b128-0615-9005-b0e5-9bd0926a2a2e", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "56b5b128-0623-30f2-a684-b14106c4cf9d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "aeb5b128-0630-d755-57d3-2be3b97309f8", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "d6b5b128-063e-aa6f-3ea6-82d1613f9b47", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "8ab5b128-064c-37ba-903a-b4409ca3ddd1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "16b5b128-0659-9ce2-8185-16a6e7f2326a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b2b5b128-0668-c1ea-e3fc-8d331d5828c9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1cb5b128-0676-ff70-5e10-e9d5b384f070", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f0b5b128-0684-03fb-7132-72e11702c78d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "bab5b128-0693-5695-8ec1-b76276e3952d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "0eb5b128-06a0-9f3d-a24a-b4ac4e135877", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5cb5b128-06af-f128-947a-83dc3fa5413d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "70b5b128-06bd-1534-89d5-21b961c8de87", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5cb5b128-06cb-d7cd-045c-4e4b98a2f7f7", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a4b5b128-06d9-b2ef-80a3-150f5fd6332a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "86b5b128-06e9-e7bb-fa36-11f17f834c26", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "7eb5b128-06fb-f733-e099-cc49bcc63761", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "64b5b128-0709-766a-fda1-55f93da62a4c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "38b5b128-0715-c4ca-7d06-9f4821049759", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4ab5b128-0724-dd2c-e813-a08786002ddc", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a6b5b128-0734-7c8d-a60c-f6bfc9902617", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "66b5b128-0741-8bc4-a164-13cce7350b7f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a6b5b128-074f-fc2c-cdf5-763527638592", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "60b5b128-075e-3fbd-8a49-cd663e482df7", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "64b5b128-076c-31fc-f039-b9bd833f35c9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "28b5b128-077a-00f3-2c57-826e0663ce30", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "52b5b128-078b-c45a-417f-ff54a156eb2f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "84b5b128-07a2-55bf-019d-0dd53126703f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "feb5b128-07b5-0dd6-c36e-37716f523b8a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4cb5b128-07c4-23d8-d07e-e3f1ff60c40d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c0b5b128-07d1-d06a-2632-ad973f88402d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "18b5b128-07df-2367-7e4e-5ffc9b2c80d1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "ccb5b128-07ed-f7d6-1855-e35785f2711d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "00b5b128-07fa-ddb8-78da-7bc774318bb1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "bcb5b128-0808-ad03-9f46-086ded19b888", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c4b5b128-0816-5613-70c1-a4d776b32728", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a0b5b128-0824-4b1a-8e69-5bf36c405484", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b6b5b128-0832-0261-8208-c59dab95cec2", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1ab5b128-0840-8fa4-dda0-5a22a4c50b99", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b0b5b128-084e-25e2-1d74-87c6b01765da", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b8b5b128-085c-a411-2c09-e79de27ab069", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5cb5b128-0869-e190-5634-7fd4ab24c0d8", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "76b5b128-0877-7979-4784-179d1f853e03", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "36b5b128-0885-3573-c6e6-e4bd6785cd73", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6ab5b128-0892-11d2-500c-5d607dcf52ff", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "d0b5b128-089f-d6d6-2291-674b1e6e53d7", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "0cb5b128-08ad-07ee-ccab-927d331b09aa", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c4b5b128-08bb-5262-f6c7-febe5f422186", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "48b5b128-08ce-f7ea-7571-e818144ed2f0", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c8b5b128-08e1-30a4-79f6-22456e86bce9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "8cb5b128-08ef-dbfd-beeb-fe18f3b440a0", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1cb5b128-08fd-8b68-9b60-1d7cc13c7783", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "beb5b128-090a-f180-fe66-8463c590b02a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "14b5b128-0918-9ce2-cf70-171717d9c537", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "cab5b128-0926-3d3f-523d-097145539460", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "d8b5b128-0933-eb44-27b1-3b38559c2788", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b6b5b128-0941-ae85-441c-4c71e0c4c588", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "3eb5b128-094f-c6b1-e4ef-3f3ea14c7a75", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b2b5b128-095d-a65e-1a66-b912b6d8fc39", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "70b5b128-096a-cf72-98fa-a334e82380f4", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "aab5b128-097c-3943-d44a-0f1b65facc3e", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "20b5b128-098e-d215-371e-daa93d00fefb", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "16b5b128-09a0-5ec3-0e7f-0848e4ee441d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "0eb5b128-09b2-ede4-7290-a8374346e66b", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a4b5b128-09c5-fe5d-4cc0-a2eead27360f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f6b5b128-09d8-3519-d6f3-0e5c91121066", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "9eb5b128-09ea-665c-04c5-04075af5867c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "70b5b128-09fc-2065-0e53-3e1207cc16ff", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6eb5b128-0a0e-af0c-8e4e-6ebf1aaf92a1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "24b5b128-0a1f-a948-630f-0c22b4e23bfa", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "e0b5b128-0a30-d456-9175-23cd5238194f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "eab5b128-0a41-4270-aab6-274159653905", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "9eb5b128-0a56-56d9-adab-2be9939ce02c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a0b5b128-0a68-0a19-89df-878d800824e2", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "ccb5b128-0a7b-6c32-dfaf-c89c9ec34bc8", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "48b5b128-0a8d-6a89-4cb6-b2002b4f7ec3", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "52b5b128-0a9e-3b98-e91c-fefc55399015", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a4b5b128-0ab0-dc2a-d035-c1a7fb7e8709", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "e6b5b128-0ac4-0d15-3766-87bbb0aaf5ca", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "82b5b128-0ad7-0956-61dc-70bfec152dd1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "46b5b128-0aea-15b2-c537-15113b41d4ba", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4ab5b128-0af9-a725-c6b5-24d48c71930f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a4b5b128-0b07-8918-f341-f08d68a7cad2", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "3cb5b128-0b17-540a-902e-a9f0ba4408fc", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "d8b5b128-0b28-daa3-12ce-b107ee1d9f66", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "50b5b128-0b39-2e11-2c7c-a1a785142f6c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "86b5b128-0b47-9883-e562-384de0a65fcb", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "28b5b128-0b55-e7b7-1c59-252805de6b0d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f8b5b128-0b63-8011-4dfb-4273d3848007", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "74b5b128-0b75-114a-1f71-a987f2a35271", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a0b5b128-0b82-d244-f814-e6dfffeeac23", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "aab5b128-0b91-651c-d266-4f04222482c5", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "eeb5b128-0b9f-5dc4-8a53-61c27298258f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "e4b5b128-0bac-c1ed-61b2-85948200d69c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "7cb5b128-0bbb-fd2f-15c0-e9b09598b43c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4ab5b128-0bca-5674-5479-5057b7f629dd", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "7cb5b128-0bd7-e617-a5ac-37b5c093246f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a6b5b128-0be5-4bf2-6c2d-521c3c8e5b36", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c4b5b128-0bf2-c5e7-739c-952b7396d445", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "ccb5b128-0bff-9067-d029-fd3b7f4ec558", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "3ab5b128-0c0c-f7c5-f957-3238139bc96f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "deb5b128-0c1a-4f79-2353-22e11078b553", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "aab5b128-0c28-73f4-3c0f-4b3b3678456b", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "24b5b128-0c37-4c68-93f0-bcaaa4ea2263", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "0cb5b128-0c45-9a06-acb9-47ba17b5e289", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "50b5b128-0c53-18c5-2826-1a5449d9f70d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "88b5b128-0c61-0a8a-6d4c-a26b245506a9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1cb5b128-0c6e-4b2c-a1f5-375b0c270737", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f0b5b128-0c7c-02fa-8cff-d7ecea19a855", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "90b5b128-0c8a-1992-36f1-4321c940be74", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "64b5b128-0c98-2bdc-ff33-2ce950ce42b8", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4cb5b128-0ca6-6777-aca9-551df3fcf8bf", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "e6b5b128-0cb3-c249-707c-28d6cfd9aa5a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "78b5b128-0cc1-13c4-3444-5634ae4aa9dc", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5ab5b128-0cce-8de3-ab44-4d84975e9df4", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "52b5b128-0cdd-43fe-e92a-22dd7b3b7229", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "62b5b128-0ceb-3f70-5846-6609370e407a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "04b5b128-0cf8-25ca-d355-1e71b67794ce", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f8b5b128-0d06-1667-2d3d-59f7e4c2acfb", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b2b5b128-0d14-3fdd-618f-9d5210e14610", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6ab5b128-0d24-2819-1729-56cbdd8f4e49", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "e6b5b128-0d33-22d4-49b1-0b2c890bc836", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a4b5b128-0d43-7a3e-687f-cb7ab9626ec5", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "10b5b128-0d51-d1ed-ee0f-be5baf521e51", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "0ab5b128-0d5f-bff5-e33b-e33f7da5336d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "14b5b128-0d70-c129-dbc9-1b41febb8280", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "04b5b128-0d7e-f16d-f027-8c3e0f463a5a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "dcb5b128-0d8d-6bc5-065a-d73bd1af09d9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "94b5b128-0d9b-f560-78d4-781f704e7ea2", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "32b5b128-0da9-e585-6879-7f465df9075c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "72b5b128-0db8-f357-cc71-c5e3084a7531", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5ab5b128-0dca-9848-ed09-b71014ff8621", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "e2b5b128-0ddb-2572-be64-efd4b051bd3b", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "3ab5b128-0dea-a84b-d385-a3040ecaad0f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "74b5b128-0dfa-f484-a765-8d17c8297367", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "7ab5b128-0e07-894c-7b18-74242d977c39", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "7cb5b128-0e15-31c0-72fb-c8ad75a8ba71", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "fcb5b128-0e22-12d2-f5b0-f41f9459da77", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "36b5b128-0e2f-be88-9db9-8965d6dc0594", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "22b5b128-0e42-638e-d769-6ebce042ca59", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6eb5b128-0e50-38cd-95c2-151562dd4f06", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "36b5b128-0e5e-7fc3-9cc6-14e715373e47", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "cab5b128-0e6c-2a3d-90eb-7170162cf153", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "30b5b128-0e79-ee7a-549b-180f33083ad5", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6ab5b128-0e87-c4b7-ec47-bac1fe7bb38e", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "00b5b128-0e95-6990-c1c3-9f1f253e44da", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "68b5b128-0ea4-3251-7cf9-b39b595e7083", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "0cb5b128-0eb8-4589-5c45-3feee5d584d5", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c0b5b128-0ec9-7c6f-1f8f-09050e595f65", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "02b5b128-0ed9-965d-12cf-25cd385cdde6", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6eb5b128-0ee8-a581-d9bc-dd7afbab6ecd", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "04b5b128-0ef7-ed56-1820-2eb2b1bec761", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "44b5b128-0f05-690d-799e-94d0d6999178", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "acb5b128-0f15-94ae-9541-050724ade5ba", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "2cb5b128-0f25-a46f-1b49-3c7a610cf06c", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "54b5b128-0f33-e5d1-1676-222b14fbcfba", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "02b5b128-0f42-35ee-c80b-8db222406ce9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f0b5b128-0f50-6ee4-2ff5-206d5b64caf8", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f4b5b128-0f60-a0ee-eade-ebe30d959299", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a2b5b128-0f6f-d237-e4bc-98132566192e", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "12b5b128-0f7e-d11d-edd8-f324da3121bc", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "cab5b128-0f8b-8d2b-74bc-a15b0496bf48", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "04b5b128-0f99-09af-34f6-2a4bd576bfcd", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "8eb5b128-0fa6-ed30-98bc-96f26992c2df", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "44b5b128-0fb4-8bdf-b23a-706ccf8091dd", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6ab5b128-0fc3-61ac-e030-8a4bc9b80cb1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "3eb5b128-0fd1-a59d-56be-312379ca8d29", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "9ab5b128-0fdf-b95c-eb64-75395e201d16", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "d6b5b128-0fed-b0ec-3371-b7278e93d560", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "d8b5b128-0ffc-6465-0bc7-ebedc5f81d80", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "8cb5b128-100b-bb73-e6b5-a983073a9b82", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1eb5b128-101a-0740-ea6f-6b80e1b1e95b", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4eb5b128-1027-b16a-6016-e93ddae2a5ce", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4ab5b128-1034-e7a6-fd3b-5b88844e4a06", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "66b5b128-1042-5e8a-a5b8-474247b9f4ed", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "5eb5b128-1050-0c2c-9292-328494dbbcfc", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b0b5b128-105e-223e-4bf8-12250d2f5b06", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "34b5b128-106b-4a0b-12e2-61e80ad0798d", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "4ab5b128-107c-b48b-265c-917e0fb86bed", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b0b5b128-108a-6844-24ba-74a036b120d1", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "22b5b128-1098-6275-6d21-03b5a4b9e740", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "6ab5b128-10a5-9886-d359-6f531b54838f", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "c4b5b128-10b4-27d7-e0be-f9cee3450d0a", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "9eb5b128-10c3-be55-bf3d-c6b1901559bd", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "f0b5b128-10d3-3d07-f2e3-2b7f7e0e83eb", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "1ab5b128-10e3-309b-98f3-0c371192c317", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "9eb5b128-10f1-aca2-ed73-ac9ac483e84e", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "44b5b128-1100-8f35-b252-48d1a940fda2", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "30b5b128-110e-3e79-52b5-e8092ee5d2ac", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "aeb5b128-111a-9f88-df2c-2fb4f9f15527", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "2ab5b128-112a-72e2-f2cc-874dea81d4d9", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "b2b5b128-1137-e36b-d79f-ecacc07c12c0", "values": []}, {"from": "c2b5b128-0518-c672-d450-2d7611db6c9e", "to": "a0b5b128-1145-15e7-d182-94009a2add04", "values": []}]
session.post(burp238_url, headers=burp238_headers, json=burp238_json)

burp239_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/patient/instances/c2b5b128-0518-c672-d450-2d7611db6c9e/relationCounts"
burp239_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp239_url, headers=burp239_headers)

burp240_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/patient/instances/c2b5b128-0518-c672-d450-2d7611db6c9e/relations/visit?limit=100&offset=0"
burp240_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp240_url, headers=burp240_headers)

burp241_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/patient/instances/c2b5b128-0518-c672-d450-2d7611db6c9e/relations/visit?limit=100&offset=100"
burp241_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp241_url, headers=burp241_headers)

burp242_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/patient/instances/c2b5b128-0518-c672-d450-2d7611db6c9e/relations/visit?limit=100&offset=200"
burp242_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp242_url, headers=burp242_headers)

burp243_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/visit"
burp243_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp243_url, headers=burp243_headers)

burp244_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516/concepts/visit/properties"
burp244_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp244_url, headers=burp244_headers)

burp245_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/schema/graph"
burp245_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp245_url, headers=burp245_headers)

burp246_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/4f2ad7c5-6503-4741-b54a-404e650e68e2/properties"
burp246_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp246_url, headers=burp246_headers)

burp247_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/62946296-0b69-47b6-819e-bbd06270d7cb/properties"
burp247_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp247_url, headers=burp247_headers)

burp248_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/graph/summary"
burp248_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp248_url, headers=burp248_headers)

burp249_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/Model_A"
burp249_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp249_url, headers=burp249_headers)

burp250_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/Model_A/properties"
burp250_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp250_url, headers=burp250_headers)

burp251_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/Model_B"
burp251_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp251_url, headers=burp251_headers)

burp252_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/concepts/Model_B/properties"
burp252_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp252_url, headers=burp252_headers)

burp253_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp253_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp253_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "joins": [], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp253_url, headers=burp253_headers, json=burp253_json)

burp254_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp254_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp254_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "not-present"}}], "joins": [], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp254_url, headers=burp254_headers, json=burp254_json)

burp255_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp255_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp255_json={"filters": [], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp255_url, headers=burp255_headers, json=burp255_json)

burp256_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp256_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp256_json={"filters": [], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val2"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp256_url, headers=burp256_headers, json=burp256_json)

burp257_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp257_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp257_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "joins": [], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp257_url, headers=burp257_headers, json=burp257_json)

burp258_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp258_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp258_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "not-present"}}], "joins": [], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp258_url, headers=burp258_headers, json=burp258_json)

burp259_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp259_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp259_json={"filters": [], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp259_url, headers=burp259_headers, json=burp259_json)

burp260_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp260_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp260_json={"filters": [], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val2"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp260_url, headers=burp260_headers, json=burp260_json)

burp261_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp261_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp261_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 50, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "select": {"Concepts": {"joinKeys": ["Model_B"]}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp261_url, headers=burp261_headers, json=burp261_json)

burp262_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp262_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp262_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 50, "offset": 1, "orderBy": {"Ascending": {"field": "$createdAt"}}, "select": {"Concepts": {"joinKeys": ["Model_B"]}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp262_url, headers=burp262_headers, json=burp262_json)

burp263_url = "https://concepts.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b/query/run"
burp263_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp263_json={"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "joins": [{"filters": [{"key": "prop1", "predicate": {"operation": "eq", "value": "val1"}}], "key": "Model_B", "targetType": {"concept": {"type": "Model_B"}}}], "limit": 0, "offset": 0, "orderBy": {"Ascending": {"field": "$createdAt"}}, "select": {"Concepts": {"joinKeys": ["Model_B"]}}, "type": {"concept": {"type": "Model_A"}}}
session.post(burp263_url, headers=burp263_headers, json=burp263_json)

burp264_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A7f79faea-7015-41fe-bc86-4e9e2f15fb8b"
burp264_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp264_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.delete(burp264_url, headers=burp264_headers, cookies=burp264_cookies)

burp265_url = "https://api.blackfynn.net:443/datasets/"
burp265_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp265_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp265_url, headers=burp265_headers, cookies=burp265_cookies)

burp266_url = "https://api.blackfynn.net:443/files/upload/preview?append=False"
burp266_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp266_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp266_json={"files": [{"fileName": "test-upload.txt", "size": 13, "uploadId": 0}]}
session.post(burp266_url, headers=burp266_headers, cookies=burp266_cookies, json=burp266_json)

burp267_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp267_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp267_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp267_url, headers=burp267_headers, cookies=burp267_cookies)

burp268_url = "https://api.blackfynn.net:443/files/upload/preview?append=False"
burp268_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp268_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp268_json={"files": [{"fileName": "test-upload.txt", "size": 13, "uploadId": 0}, {"fileName": "test-upload-2.txt", "size": 14, "uploadId": 1}]}
session.post(burp268_url, headers=burp268_headers, cookies=burp268_cookies, json=burp268_json)

burp269_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp269_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp269_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp269_url, headers=burp269_headers, cookies=burp269_cookies)

burp270_url = "https://api.blackfynn.net:443/files/upload/preview?append=False"
burp270_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp270_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp270_json={"files": [{"fileName": "test-upload.txt", "size": 13, "uploadId": 0}, {"fileName": "test-upload-2.txt", "size": 14, "uploadId": 1}]}
session.post(burp270_url, headers=burp270_headers, cookies=burp270_cookies, json=burp270_json)

burp271_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp271_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp271_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp271_url, headers=burp271_headers, cookies=burp271_cookies)

burp272_url = "https://api.blackfynn.net:443/packages"
burp272_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp272_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp272_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Rando Thing", "packageType": "MRI", "properties": []}
session.post(burp272_url, headers=burp272_headers, cookies=burp272_cookies, json=burp272_json)

burp273_url = "https://api.blackfynn.net:443/packages"
burp273_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp273_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp273_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Rando Timeseries", "packageType": "TimeSeries", "properties": []}
session.post(burp273_url, headers=burp273_headers, cookies=burp273_cookies, json=burp273_json)

burp274_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp274_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp274_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp274_url, headers=burp274_headers, cookies=burp274_cookies)

burp275_url = "https://api.blackfynn.net:443/files/upload/preview?append=True"
burp275_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp275_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp275_json={"files": [{"fileName": "test-upload.txt", "size": 13, "uploadId": 0}]}
session.post(burp275_url, headers=burp275_headers, cookies=burp275_cookies, json=burp275_json)

burp276_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp276_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp276_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp276_url, headers=burp276_headers, cookies=burp276_cookies)

burp277_url = "https://api.blackfynn.net:443/packages"
burp277_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp277_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp277_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Rando Timeseries", "packageType": "TimeSeries", "properties": []}
session.post(burp277_url, headers=burp277_headers, cookies=burp277_cookies, json=burp277_json)

burp278_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp278_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp278_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp278_url, headers=burp278_headers, cookies=burp278_cookies)

burp279_url = "https://api.blackfynn.net:443/files/upload/preview?append=True"
burp279_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp279_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp279_json={"files": [{"fileName": "test-upload.txt", "size": 13, "uploadId": 0}, {"fileName": "test-upload-2.txt", "size": 14, "uploadId": 1}]}
session.post(burp279_url, headers=burp279_headers, cookies=burp279_cookies, json=burp279_json)

burp280_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp280_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp280_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp280_url, headers=burp280_headers, cookies=burp280_cookies)

burp281_url = "https://api.blackfynn.net:443/packages"
burp281_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp281_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp281_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Rando Timeseries", "packageType": "TimeSeries", "properties": []}
session.post(burp281_url, headers=burp281_headers, cookies=burp281_cookies, json=burp281_json)

burp282_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp282_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp282_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp282_url, headers=burp282_headers, cookies=burp282_cookies)

burp283_url = "https://api.blackfynn.net:443/files/upload/preview?append=True"
burp283_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp283_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp283_json={"files": [{"fileName": "test-upload.txt", "size": 13, "uploadId": 0}, {"fileName": "test-upload-2.txt", "size": 14, "uploadId": 1}]}
session.post(burp283_url, headers=burp283_headers, cookies=burp283_cookies, json=burp283_json)

burp284_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp284_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp284_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp284_url, headers=burp284_headers, cookies=burp284_cookies)

burp285_url = "https://api.blackfynn.net:443/files/upload/preview?append=False"
burp285_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp285_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp285_json={"files": [{"fileName": "empty.txt", "size": 0, "uploadId": 0}]}
session.post(burp285_url, headers=burp285_headers, cookies=burp285_cookies, json=burp285_json)

burp286_url = "https://api.blackfynn.net:443/security/user/credentials/upload/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp286_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp286_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp286_url, headers=burp286_headers, cookies=burp286_cookies)

burp287_url = "https://api.blackfynn.net:443/packages"
burp287_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp287_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp287_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Some tabular data", "packageType": "Tabular", "properties": []}
session.post(burp287_url, headers=burp287_headers, cookies=burp287_cookies, json=burp287_json)

burp288_url = "https://api.blackfynn.net:443/tabular/N%3Apackage%3A56287006-396d-42f9-95f6-6f84de65e3ad/schema"
burp288_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp288_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp288_json={"schema": [{"datatype": "Integer", "displayName": "index", "internal": True, "name": "", "primaryKey": True}, {"datatype": "String", "displayName": "email", "internal": False, "name": "", "primaryKey": False}]}
session.post(burp288_url, headers=burp288_headers, cookies=burp288_cookies, json=burp288_json)

burp289_url = "https://api.blackfynn.net:443/tabular/N%3Apackage%3A56287006-396d-42f9-95f6-6f84de65e3ad/schema"
burp289_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp289_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp289_url, headers=burp289_headers, cookies=burp289_cookies)

burp290_url = "https://api.blackfynn.net:443/model-schema/validate"
burp290_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp290_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp290_json={"$schema": "http://schema.blackfynn.io/model/draft-01/schema", "category": "Person", "description": "This is a test", "name": "Test Template", "properties": {"DOB": {"description": "Date of Birth", "format": "date", "type": "string"}, "name": {"description": "Name", "type": "string"}, "Weight": {"description": "Weight", "type": "number", "unit": "lbs"}}, "required": ["name"]}
session.post(burp290_url, headers=burp290_headers, cookies=burp290_cookies, json=burp290_json)

burp291_url = "https://api.blackfynn.net:443/packages"
burp291_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp291_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp291_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Human EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp291_url, headers=burp291_headers, cookies=burp291_cookies, json=burp291_json)

burp292_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Aa4acc3d1-41f7-40e7-aeab-46a33379e8b4"
burp292_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp292_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp292_url, headers=burp292_headers, cookies=burp292_cookies)

burp293_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Aa4acc3d1-41f7-40e7-aeab-46a33379e8b4"
burp293_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp293_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp293_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Monkey EEG", "packageType": "TimeSeries", "properties": [], "state": "UNAVAILABLE"}
session.put(burp293_url, headers=burp293_headers, cookies=burp293_cookies, json=burp293_json)

burp294_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Aa4acc3d1-41f7-40e7-aeab-46a33379e8b4"
burp294_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp294_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp294_url, headers=burp294_headers, cookies=burp294_cookies)

burp295_url = "https://api.blackfynn.net:443/data/delete"
burp295_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp295_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp295_json={"things": ["N:package:a4acc3d1-41f7-40e7-aeab-46a33379e8b4"]}
session.post(burp295_url, headers=burp295_headers, cookies=burp295_cookies, json=burp295_json)

burp296_url = "https://api.blackfynn.net:443/packages"
burp296_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp296_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp296_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Human EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp296_url, headers=burp296_headers, cookies=burp296_cookies, json=burp296_json)

burp297_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980"
burp297_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp297_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp297_url, headers=burp297_headers, cookies=burp297_cookies)

burp298_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980"
burp298_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp298_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp298_url, headers=burp298_headers, cookies=burp298_cookies)

burp299_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp299_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp299_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp299_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-0", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp299_url, headers=burp299_headers, cookies=burp299_cookies, json=burp299_json)

burp300_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A6670ee8d-bbcb-4a11-ad23-4f0fb386096a/properties"
burp300_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp300_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp300_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp300_url, headers=burp300_headers, cookies=burp300_cookies, json=burp300_json)

burp301_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp301_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp301_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp301_url, headers=burp301_headers, cookies=burp301_cookies)

burp302_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A6670ee8d-bbcb-4a11-ad23-4f0fb386096a"
burp302_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp302_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp302_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-0-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp302_url, headers=burp302_headers, cookies=burp302_cookies, json=burp302_json)

burp303_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp303_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp303_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp303_url, headers=burp303_headers, cookies=burp303_cookies)

burp304_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp304_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp304_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp304_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-1", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp304_url, headers=burp304_headers, cookies=burp304_cookies, json=burp304_json)

burp305_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Aa10e669e-cb57-4ea8-86e4-d250a8fb64e7/properties"
burp305_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp305_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp305_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp305_url, headers=burp305_headers, cookies=burp305_cookies, json=burp305_json)

burp306_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp306_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp306_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp306_url, headers=burp306_headers, cookies=burp306_cookies)

burp307_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Aa10e669e-cb57-4ea8-86e4-d250a8fb64e7"
burp307_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp307_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp307_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-1-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp307_url, headers=burp307_headers, cookies=burp307_cookies, json=burp307_json)

burp308_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp308_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp308_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp308_url, headers=burp308_headers, cookies=burp308_cookies)

burp309_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp309_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp309_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp309_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-2", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp309_url, headers=burp309_headers, cookies=burp309_cookies, json=burp309_json)

burp310_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A6d07b90f-eb4b-4b4b-b253-665fe9c56575/properties"
burp310_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp310_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp310_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp310_url, headers=burp310_headers, cookies=burp310_cookies, json=burp310_json)

burp311_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp311_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp311_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp311_url, headers=burp311_headers, cookies=burp311_cookies)

burp312_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A6d07b90f-eb4b-4b4b-b253-665fe9c56575"
burp312_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp312_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp312_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-2-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp312_url, headers=burp312_headers, cookies=burp312_cookies, json=burp312_json)

burp313_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp313_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp313_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp313_url, headers=burp313_headers, cookies=burp313_cookies)

burp314_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp314_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp314_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp314_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-3", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp314_url, headers=burp314_headers, cookies=burp314_cookies, json=burp314_json)

burp315_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A25afe752-7e85-42b9-af71-99aac81535c0/properties"
burp315_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp315_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp315_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp315_url, headers=burp315_headers, cookies=burp315_cookies, json=burp315_json)

burp316_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp316_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp316_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp316_url, headers=burp316_headers, cookies=burp316_cookies)

burp317_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A25afe752-7e85-42b9-af71-99aac81535c0"
burp317_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp317_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp317_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-3-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp317_url, headers=burp317_headers, cookies=burp317_cookies, json=burp317_json)

burp318_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp318_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp318_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp318_url, headers=burp318_headers, cookies=burp318_cookies)

burp319_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp319_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp319_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp319_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-4", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp319_url, headers=burp319_headers, cookies=burp319_cookies, json=burp319_json)

burp320_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Af1cb528a-4724-4661-b557-33ea70e3f5e6/properties"
burp320_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp320_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp320_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp320_url, headers=burp320_headers, cookies=burp320_cookies, json=burp320_json)

burp321_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp321_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp321_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp321_url, headers=burp321_headers, cookies=burp321_cookies)

burp322_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Af1cb528a-4724-4661-b557-33ea70e3f5e6"
burp322_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp322_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp322_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-4-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp322_url, headers=burp322_headers, cookies=burp322_cookies, json=burp322_json)

burp323_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp323_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp323_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp323_url, headers=burp323_headers, cookies=burp323_cookies)

burp324_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp324_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp324_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp324_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-5", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp324_url, headers=burp324_headers, cookies=burp324_cookies, json=burp324_json)

burp325_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A5f54cc8c-8f17-4205-be75-a8713571d0bf/properties"
burp325_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp325_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp325_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp325_url, headers=burp325_headers, cookies=burp325_cookies, json=burp325_json)

burp326_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp326_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp326_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp326_url, headers=burp326_headers, cookies=burp326_cookies)

burp327_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A5f54cc8c-8f17-4205-be75-a8713571d0bf"
burp327_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp327_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp327_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-5-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp327_url, headers=burp327_headers, cookies=burp327_cookies, json=burp327_json)

burp328_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp328_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp328_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp328_url, headers=burp328_headers, cookies=burp328_cookies)

burp329_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp329_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp329_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp329_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-6", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp329_url, headers=burp329_headers, cookies=burp329_cookies, json=burp329_json)

burp330_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A4e8a8fc7-368e-4ea7-9ec4-f8f8befeeec6/properties"
burp330_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp330_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp330_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp330_url, headers=burp330_headers, cookies=burp330_cookies, json=burp330_json)

burp331_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp331_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp331_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp331_url, headers=burp331_headers, cookies=burp331_cookies)

burp332_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A4e8a8fc7-368e-4ea7-9ec4-f8f8befeeec6"
burp332_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp332_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp332_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-6-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp332_url, headers=burp332_headers, cookies=burp332_cookies, json=burp332_json)

burp333_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp333_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp333_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp333_url, headers=burp333_headers, cookies=burp333_cookies)

burp334_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp334_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp334_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp334_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-7", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp334_url, headers=burp334_headers, cookies=burp334_cookies, json=burp334_json)

burp335_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Abdcb0b78-9b24-40df-a31f-06db49d5f281/properties"
burp335_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp335_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp335_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp335_url, headers=burp335_headers, cookies=burp335_cookies, json=burp335_json)

burp336_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp336_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp336_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp336_url, headers=burp336_headers, cookies=burp336_cookies)

burp337_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Abdcb0b78-9b24-40df-a31f-06db49d5f281"
burp337_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp337_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp337_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-7-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp337_url, headers=burp337_headers, cookies=burp337_cookies, json=burp337_json)

burp338_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp338_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp338_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp338_url, headers=burp338_headers, cookies=burp338_cookies)

burp339_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp339_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp339_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp339_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-8", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp339_url, headers=burp339_headers, cookies=burp339_cookies, json=burp339_json)

burp340_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Ac81ed61d-ff58-48a4-b427-2d0956bf68f9/properties"
burp340_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp340_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp340_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp340_url, headers=burp340_headers, cookies=burp340_cookies, json=burp340_json)

burp341_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp341_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp341_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp341_url, headers=burp341_headers, cookies=burp341_cookies)

burp342_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Ac81ed61d-ff58-48a4-b427-2d0956bf68f9"
burp342_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp342_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp342_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-8-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp342_url, headers=burp342_headers, cookies=burp342_cookies, json=burp342_json)

burp343_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp343_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp343_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp343_url, headers=burp343_headers, cookies=burp343_cookies)

burp344_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp344_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp344_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp344_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-9", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp344_url, headers=burp344_headers, cookies=burp344_cookies, json=burp344_json)

burp345_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A97e21474-6a9c-4c57-9fe3-319f325566e9/properties"
burp345_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp345_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp345_json=[{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}]
session.put(burp345_url, headers=burp345_headers, cookies=burp345_cookies, json=burp345_json)

burp346_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp346_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp346_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp346_url, headers=burp346_headers, cookies=burp346_cookies)

burp347_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A97e21474-6a9c-4c57-9fe3-319f325566e9"
burp347_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp347_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp347_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "Channel-9-updated", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": False, "hidden": False, "key": "key", "value": "value"}, {"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 200, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp347_url, headers=burp347_headers, cookies=burp347_cookies, json=burp347_json)

burp348_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp348_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp348_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp348_url, headers=burp348_headers, cookies=burp348_cookies)

burp349_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp349_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp349_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp349_url, headers=burp349_headers, cookies=burp349_cookies)

burp350_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3Aa10e669e-cb57-4ea8-86e4-d250a8fb64e7"
burp350_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp350_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.delete(burp350_url, headers=burp350_headers, cookies=burp350_cookies)

burp351_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp351_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp351_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp351_url, headers=burp351_headers, cookies=burp351_cookies)

burp352_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels/N%3Achannel%3A6670ee8d-bbcb-4a11-ad23-4f0fb386096a"
burp352_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp352_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.delete(burp352_url, headers=burp352_headers, cookies=burp352_cookies)

burp353_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A9f8c119f-3df1-48be-93d3-1a4289517980/channels"
burp353_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp353_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp353_url, headers=burp353_headers, cookies=burp353_cookies)

burp354_url = "https://api.blackfynn.net:443/data/delete"
burp354_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp354_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp354_json={"things": ["N:package:9f8c119f-3df1-48be-93d3-1a4289517980"]}
session.post(burp354_url, headers=burp354_headers, cookies=burp354_cookies, json=burp354_json)

burp355_url = "https://api.blackfynn.net:443/packages"
burp355_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp355_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp355_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Human EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp355_url, headers=burp355_headers, cookies=burp355_cookies, json=burp355_json)

burp356_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Abc767cee-8a91-4856-b48c-bdd646154a34"
burp356_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp356_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp356_url, headers=burp356_headers, cookies=burp356_cookies)

burp357_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3Abc767cee-8a91-4856-b48c-bdd646154a34/layers"
burp357_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp357_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp357_url, headers=burp357_headers, cookies=burp357_cookies)

burp358_url = "https://api.blackfynn.net:443/data/delete"
burp358_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp358_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp358_json={"things": ["N:package:bc767cee-8a91-4856-b48c-bdd646154a34"]}
session.post(burp358_url, headers=burp358_headers, cookies=burp358_cookies, json=burp358_json)

burp359_url = "https://api.blackfynn.net:443/packages"
burp359_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp359_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp359_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Human EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp359_url, headers=burp359_headers, cookies=burp359_cookies, json=burp359_json)

burp360_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A46f5df4a-741e-45d8-9910-4fbc8737047d"
burp360_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp360_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp360_url, headers=burp360_headers, cookies=burp360_cookies)

burp361_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A46f5df4a-741e-45d8-9910-4fbc8737047d/channels"
burp361_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp361_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp361_json={"channelType": "CONTINUOUS", "end": 2000000, "group": "default", "lastAnnotation": 0, "name": "test_channel", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp361_url, headers=burp361_headers, cookies=burp361_cookies, json=burp361_json)

burp362_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A46f5df4a-741e-45d8-9910-4fbc8737047d/layers"
burp362_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp362_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp362_url, headers=burp362_headers, cookies=burp362_cookies)

burp363_url = "https://api.blackfynn.net:443/data/delete"
burp363_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp363_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp363_json={"things": ["N:package:46f5df4a-741e-45d8-9910-4fbc8737047d"]}
session.post(burp363_url, headers=burp363_headers, cookies=burp363_cookies, json=burp363_json)

burp364_url = "https://api.blackfynn.net:443/packages"
burp364_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp364_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp364_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Human EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp364_url, headers=burp364_headers, cookies=burp364_cookies, json=burp364_json)

burp365_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3A70bab718-a083-433f-8ebb-a1ac7722613a"
burp365_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp365_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp365_url, headers=burp365_headers, cookies=burp365_cookies)

burp366_url = "https://api.blackfynn.net:443/packages"
burp366_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp366_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp366_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Animal EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp366_url, headers=burp366_headers, cookies=burp366_cookies, json=burp366_json)

burp367_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A70bab718-a083-433f-8ebb-a1ac7722613a/channels"
burp367_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp367_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp367_json={"channelType": "CONTINUOUS", "end": 1000000, "group": "default", "lastAnnotation": 0, "name": "test_channel", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp367_url, headers=burp367_headers, cookies=burp367_cookies, json=burp367_json)

burp368_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3Ae3adb096-0890-4fa0-a1ce-18fd6787d3b4/channels"
burp368_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp368_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp368_json={"channelType": "CONTINUOUS", "end": 1000000, "group": "default", "lastAnnotation": 0, "name": "test_channel_2", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp368_url, headers=burp368_headers, cookies=burp368_cookies, json=burp368_json)

burp369_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3A70bab718-a083-433f-8ebb-a1ac7722613a/layers"
burp369_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp369_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp369_url, headers=burp369_headers, cookies=burp369_cookies)

burp370_url = "https://api.blackfynn.net:443/data/delete"
burp370_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp370_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp370_json={"things": ["N:package:e3adb096-0890-4fa0-a1ce-18fd6787d3b4"]}
session.post(burp370_url, headers=burp370_headers, cookies=burp370_cookies, json=burp370_json)

burp371_url = "https://api.blackfynn.net:443/data/delete"
burp371_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp371_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp371_json={"things": ["N:package:70bab718-a083-433f-8ebb-a1ac7722613a"]}
session.post(burp371_url, headers=burp371_headers, cookies=burp371_cookies, json=burp371_json)

burp372_url = "https://api.blackfynn.net:443/packages"
burp372_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp372_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp372_json={"dataset": "N:dataset:9113b642-a8a4-40da-96e2-27f69f20d516", "name": "Human EEG", "packageType": "TimeSeries", "properties": []}
session.post(burp372_url, headers=burp372_headers, cookies=burp372_cookies, json=burp372_json)

burp373_url = "https://api.blackfynn.net:443/packages/N%3Apackage%3Af818caa4-fadd-43a4-a56b-f922ffacab02"
burp373_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp373_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp373_url, headers=burp373_headers, cookies=burp373_cookies)

burp374_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3Af818caa4-fadd-43a4-a56b-f922ffacab02/channels"
burp374_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp374_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp374_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "ch 1", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp374_url, headers=burp374_headers, cookies=burp374_cookies, json=burp374_json)

burp375_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3Af818caa4-fadd-43a4-a56b-f922ffacab02/channels"
burp375_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp375_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp375_json={"channelType": "CONTINUOUS", "end": 0, "group": "default", "lastAnnotation": 0, "name": "ch 2", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 111.123, "spikeDuration": None, "start": 0, "unit": "uV"}
session.post(burp375_url, headers=burp375_headers, cookies=burp375_cookies, json=burp375_json)

burp376_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3Af818caa4-fadd-43a4-a56b-f922ffacab02/channels"
burp376_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp376_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp376_url, headers=burp376_headers, cookies=burp376_cookies)

burp377_url = "https://api.blackfynn.net:443/timeseries/N%3Apackage%3Af818caa4-fadd-43a4-a56b-f922ffacab02/channels/N%3Achannel%3A7e282be5-12cc-40f6-bc82-958214cd167e"
burp377_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp377_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp377_json={"channelType": "CONTINUOUS", "end": 5000000, "group": "default", "lastAnnotation": 0, "name": "ch 1", "properties": [{"category": "Blackfynn", "dataType": "string", "fixed": True, "hidden": True, "key": "Source Type", "value": "UNSPECIFIED"}], "rate": 256.0, "spikeDuration": None, "start": 0, "unit": "uV"}
session.put(burp377_url, headers=burp377_headers, cookies=burp377_cookies, json=burp377_json)

burp378_url = "https://streaming.blackfynn.io:443/ts/retrieve/segments?gapThreshold=2&session=db4ca39d-4218-41be-a240-60601eb54046&end=5000000&package=N%3Apackage%3Af818caa4-fadd-43a4-a56b-f922ffacab02&start=0&channel=N%3Achannel%3A7e282be5-12cc-40f6-bc82-958214cd167e"
burp378_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp378_url, headers=burp378_headers)

burp379_url = "https://api.blackfynn.net:443/data/delete"
burp379_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp379_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID, "Content-Type": "application/json"}
burp379_json={"things": ["N:package:f818caa4-fadd-43a4-a56b-f922ffacab02"]}
session.post(burp379_url, headers=burp379_headers, cookies=burp379_cookies, json=burp379_json)

burp380_url = "https://api.blackfynn.net:443/datasets/N%3Adataset%3A9113b642-a8a4-40da-96e2-27f69f20d516"
burp380_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp380_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.delete(burp380_url, headers=burp380_headers, cookies=burp380_cookies)

burp381_url = "https://api.blackfynn.net:443/datasets/"
burp381_cookies = {"scentry.auth.default.user": "", "JSESSIONID": "605BF9FC57BD59F87F22AD756BEC253B"}
burp381_headers = {"Connection": "close", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "User-Agent": "python-requests/2.21.0", "Authorization": AUTHORIZATION_BEARER, "X-SESSION-ID": X_SESSION_ID, "X-ORGANIZATION-ID": X_ORGANIZATION_ID}
session.get(burp381_url, headers=burp381_headers, cookies=burp381_cookies)
