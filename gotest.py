import http.client
import ssl
import gzip
import re
import functools
import json

def getHeaders(indexes):
	headerDict = {}
	for row in indexes:
		headerDict.update({lookupHeaders[row][0]: lookupHeaders[row][1]})
	return headerDict

def makeRequest(conn, method, path, indexes, payload):
	print(path)
	conn.request(method, path, payload, getHeaders(indexes))
	res = conn.getresponse()
	# f.write(str(res.status) + ', ' + str(res.reason) + '\n')
	print(str(res.status) + ', ' + str(res.reason))
	data = res.read()
	try:
		return data.decode('utf-8'), res.headers
		 # f.write(method + " " + path + "\n" + data.decode('utf-8') + '\n')
		 # print(method + " " + path + "\n" + data.decode('utf-8'))
	except:
		return gzip.decompress(data).decode('utf-8'), res.headers
		 # f.write(method + " " + path + "\n" + gzip.decompress(data).decode('utf-8') + '\n')
		 # print(method + " " + path + "\n" + gzip.decompress(data).decode('utf-8'))

lookupHeaders = {
	0	: ('Host', '172.19.40.55'),
	1	: ('Connection', 'keep-alive'),
	2	: ('sec-ch-ua', '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'),
	3	: ('sec-ch-ua-mobile', '?0'),
	4	: ('sec-ch-ua-platform', '"Windows"'),
	5	: ('Upgrade-Insecure-Requests', '1'),
	6	: ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'),
	7	: ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
	8	: ('Sec-Fetch-Site', 'none'),
	9	: ('Sec-Fetch-Mode', 'navigate'),
	10	: ('Sec-Fetch-User', '?1'),
	11	: ('Sec-Fetch-Dest', 'document'),
	12	: ('Accept-Encoding', 'gzip, deflate, br'),
	13	: ('Accept-Language', 'en-US,en;q=0.9'),
	14	: ('Accept', 'text/css,*/*;q=0.1'),
	15	: ('Sec-Fetch-Site', 'same-origin'),
	16	: ('Sec-Fetch-Mode', 'no-cors'),
	17	: ('Sec-Fetch-Dest', 'style'),
	18	: ('Referer', 'htt/md/'),
	19	: ('Accept', '*/*'),
	20	: ('Sec-Fetch-Dest', 'script'),
	21	: ('Content-Length', '0'),
	22	: ('authentication-token', ''),
	23	: ('locale', 'en-us'),
	24	: ('content-type', 'application/json'),
	25	: ('accept', '*/*'),
	26	: ('Origin', 'https://172.19.40.55'),
	27	: ('Sec-Fetch-Mode', 'cors'),
	28	: ('Sec-Fetch-Dest', 'empty'),
	29	: ('Accept', 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'),
	30	: ('Sec-Fetch-Dest', 'image'),
	31	: ('Referer', 'https://172.19.40.55/md'),
	32	: ('Sec-Fetch-Dest', 'font'),
	33	: ('Referer', 'htt/md/css/app.4dd04ab2.css'),
	34	: ('Accept', 'application/json, text/plain, */*'),
	35	: ('Accept-Encoding', 'identity;q=1, *;q=0'),
	36	: ('Sec-Fetch-Dest', 'video'),
	37	: ('Range', 'bytes=0-'),
	38	: ('Referer', 'htt/md/css/vendor.22cd4147.css'),
	39	: ('authentication-token', '')
}

conn = http.client.HTTPSConnection("172.19.40.55", 443, context=ssl._create_unverified_context())

headers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
makeRequest(conn, "GET", "/md/", headers, None)
#
print('Sending POST request')
headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13]
params = '{"variables": {}, "operationName": "configuration", "query": "query configuration {\\n  configuration {\\n    tabs {\\n      key\\n      link\\n      label\\n      subTabs {\\n        key\\n        link\\n        label\\n      }\\n    }\\n    otherApps {\\n      key\\n      link\\n      label\\n      icon\\n    }\\n    systemInfo {\\n      homeUrl\\n      clientName\\n      bffVersion\\n      timezone\\n      matomoSiteId\\n      logoFileName\\n      reserveTagSupport\\n      bulkOrderLimit\\n    }\\n  }\\n}\\n"}'

lookupHeaders[21] = ('Content-Length', str(len(params)))
print(getHeaders(headers))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)
#
headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13]
params = '{"variables": {}, "operationName": "loginStatus", "query": "query loginStatus {\\n  loginStatus {\\n    user {\\n      name\\n      authorities {\\n        authority\\n      }\\n    }\\n    isLoggedIn\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
print(lookupHeaders[21])
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)
#
headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13]
params = '{"variables": {}, "operationName": "walkmeConfig", "query": "query walkmeConfig {\\n  walkmeConfig {\\n    snippetUrl\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
print(lookupHeaders[21])
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13]
params = '{"variables": {}, "operationName": "languageConfig", "query": "query languageConfig {\\n  languageConfig {\\n    allowedLanguages\\n    defaultLanguage\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13]
# params = '{"operationName": null, "variables": {"input": {"username": "lvigueria", "password": "welcome1", "forceLogoutOnlyThisUser": false}}, "query": "mutation ($input: LoginInput) {\\n  authenticate(input: $input) {\\n    token\\n    message\\n    success\\n    showForceLogout\\n  }\\n}\\n"}'
params = '{"operationName": null, "variables": {"input": {"username": "admin", "password": "apj0702", "forceLogoutOnlyThisUser": false}}, "query": "mutation ($input: LoginInput) {\\n  authenticate(input: $input) {\\n    token\\n    message\\n    success\\n    showForceLogout\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
response = json.loads(response)
print(response)
lookupHeaders[39] = ('authentication-token', response['data']['authenticate']['token'])

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13, 39]
params = '{"operationName":"loginStatus","variables":{},"query":"query loginStatus {\\n  loginStatus {\\n    user {\\n      name\\n      authorities {\\n        authority\\n      }\\n    }\\n    isLoggedIn\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)

caseID = '0013804416'
# caseID = '0013804900'

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13, 39]
params = '{"operationName":"OutboundOrderList","variables":{"input":{"leftFilters":[],"topFilters":[{"field":"orderLevel","dateRangeFilterParams":{},"checkboxFilterParams":{"selectedValues":[]},"singleSelectFilterParams":{"label":"View Master Orders","value":"masterOrder"},"multiSelectFilterParams":{"selectedValues":[]},"inputFilterParams":{"inputValue":""},"radioFilterParams":{"selectedValue":""}}],"page":1,"limit":5,"searchKeyword":"' + caseID + '"}},"query":"query OutboundOrderList($input: OutboundOrderListParams) {\\n  outboundOrderList(input: $input) {\\n    orders {\\n      id\\n      type\\n      externalServiceRequestId\\n      status\\n      state\\n      businessState\\n      createdOn\\n      updatedOn\\n      level\\n      parentAttributes {\\n        parentsExternalServiceRequestIds\\n        simplePriority\\n        parentsExternalServiceRequestId\\n      }\\n      srProductsCounts {\\n        exceptions\\n        actuals\\n        expectations\\n      }\\n      attributes {\\n        orderType\\n        simplePriority\\n        has_parent\\n        ppsId\\n        ppsBinId\\n        userName\\n        route\\n        shipment\\n        pickBeforeTime\\n        pickAfterTime\\n        allocationTime\\n        startTime\\n        completionTime\\n        orderOptions {\\n          bintags\\n        }\\n        noOfOrders\\n        binTagsStr\\n        executionTime\\n        carryingUnits\\n      }\\n      orderProgress {\\n        progressPercent\\n        progressLabel\\n      }\\n      canCancel\\n      canChangePAT\\n      canChangePBT\\n      canChangePriority\\n    }\\n    message {\\n      level\\n      text\\n    }\\n    total\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)
response = json.loads(response)

externalServiceRequestId = response['data']['outboundOrderList']['orders'][0]['externalServiceRequestId']

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13, 39]
params = '{"operationName":null,"variables":{"input":{"orders":[{"id":39591749,"externalServiceRequestId":"' + externalServiceRequestId + '","type":"PICK"}]}},"query":"mutation ($input: CancelOrdersInput!) {\\n cancelOrders(input: $input) {\\n   success\\n   message\\n   externalServiceRequestId\\n }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13, 39]
params = '{"operationName": "NotificationList", "variables": {"input": {"page": 1, "leftFilters": [], "topFilters": [{"field": "notificationStatus", "dateRangeFilterParams": {}, "checkboxFilterParams": {"selectedValues": []}, "singleSelectFilterParams": {"label": "All", "value": "ALL"}, "multiSelectFilterParams": {"selectedValues": []}, "inputFilterParams": {"inputValue": ""}, "radioFilterParams": {"selectedValue": ""}}], "limit": 50, "searchKeyword": "' + caseID + '"}}, "query": "query NotificationList($input: NotificationListParams) {\\n  notificationList(input: $input) {\\n    notifications {\\n      createTime\\n      status\\n      id\\n      subscriber {\\n        id\\n        createTime\\n        updateTime\\n      }\\n      eventData {\\n        esrId\\n        esrType\\n        id\\n        createTime\\n        payload {\\n          notification_id\\n          notification_type\\n          status\\n        }\\n      }\\n      failedSubscriber {\\n        retryCount\\n        createTime\\n        status\\n      }\\n    }\\n    message {\\n      level\\n      text\\n    }\\n    total\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)
response = json.loads(response)

eventId = '310863156' #response['data']['notificationList']['notifications'][0]['eventData']['id']
subscriberId = '34' #response['data']['notificationList']['notifications'][0]['subscriber']['id']
print(eventId, subscriberId)

headers = [0, 1, 21, 2, 22, 23, 6, 24, 25, 3, 4, 26, 15, 27, 28, 18, 12, 13, 39]
params = '{"operationName": null, "variables": {"input": {"eventId": ' + eventId + ', "subscriberId": ' + subscriberId + '}}, "query": "mutation ($input: NotificationResendParams!) {\\n  notificationResend(input: $input) {\\n    response\\n  }\\n}\\n"}'
lookupHeaders[21] = ('Content-Length', str(len(params)))
response, responseHeaders = makeRequest(conn, "POST", "/bff", headers, params)
print(response)