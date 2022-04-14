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
	conn.request(method, path, payload, getHeaders(indexes))
	res = conn.getresponse()
	print(str(res.status) + ', ' + str(res.reason))
	print(path)
	data = res.read()
	try:
		return data.decode('utf-8'), res.headers
	except:
		return gzip.decompress(data).decode('utf-8'), res.headers



lookupHeaders = {
	0	: ('Host', 'bax08s.am.gxo.com'),
	1	: ('Connection', 'keep-alive'),
	2	: ('sec-ch-ua', '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"'),
	3	: ('sec-ch-ua-mobile', '?0'),
	4	: ('sec-ch-ua-platform', '"Windows"'),
	5	: ('Upgrade-Insecure-Requests', '1'),
	6	: ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'),
	7	: ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'),
	8	: ('Sec-Fetch-Site', 'none'),
	9	: ('Sec-Fetch-Mode', 'navigate'),
	10	: ('Sec-Fetch-User', '?1'),
	11	: ('Sec-Fetch-Dest', 'document'),
	12	: ('Accept-Encoding', 'gzip, deflate, br'),
	13	: ('Accept-Language', 'en-US,en;q=0.9'),
	14	: ('Origin', 'https://bax08s.am.gxo.com'),
	16	: ('Sec-Fetch-Site', 'same-origin'),
	31	: ('Referer', 'https://bax08s.am.gxo.com/handm/login/'),
	32	: ('Cookie', 'session=eyJjc3JmX3Rva2VuIjoiN2U3NjIzNmJkYjU5YmNkMjc2YTExODQ4ZTc4YzhmMjg3N2RiYzBmYyJ9.Ykvx4w.ZZkcuqhmMP3m7QWqGoD3b-DR3u4; _client=handm; NSC_WTsw_l8t-johsftt.td.yqp.dpn443=ffffffffaf1b3d1045525d5f4f58455e445a4a42378b'),
	33	: ('Accept', '*/*'),
	37	: ('Content-Length', '0'),
	38	: ('Cache-Control', 'max-age=0'),
	39	: ('Content-Type', 'application/x-www-form-urlencoded'),
	40	: ('Cookie', '_client=handm; NSC_WTsw_l8t-johsftt.td.yqp.dpn443=ffffffffaf1b3d1045525d5f4f58455e445a4a42378b; session=.eJwljktuwzAMBe-idRbUj6RyGUOknlqjbQrYcTZF7143Wb4B3mB-gu_bXO7fH7iFaxAIp8w2rDbzkYR7jFoUoq4zqcgwp-nhEpa5YX8P1_t24BKOHdutf-F0fD7WtwPb2sMLL-s4aU5ZEuv_8bnBUlFTajh1SizZtbVJKihkVbjAoqVCfVSZRtKpWItEDgxI1C7V1aUxxwTqYLYCgmaNzTh28n4WVzZvM3OmEv3UWXGNhjLC7x-mZEhQ.Ykvy1Q.Qb1KS8rnORQsJhCTafzeX7nPxIA'),
	41	: ('Referer', 'https://bax08s.am.gxo.com/handm/superset/dashboard/1000000/'),
	42	: ('Cookie', '_client=handm; NSC_WTsw_l8t-johsftt.td.yqp.dpn443=ffffffffaf1b3d1045525d5f4f58455e445a4a42378b; session=.eJwlj0tuwzAMRO-idRbUj6RyGYOkqNaomwB23E3Ru1dJljPAPLz5DXbsY3ncv_wWroGcMGXUrrWp9UQoMXJhJzYeiYm6GgwLl7CM3Y_PcH3sp1_Cefh-k2-fjO1n_Th9XyW862Xts80pU0J-Dl_ZkarXlJpPHANSNm5tAJMX0EpYXKOmAtIrDQUSKNoigLl3p8hC1dioIcbkII6oxcE5c2yKUcBkGldUayNjhhJt4rQYR_XSp8h2N9mexvP63z-4X0yB.Ykvy2g.PrThQrvdHDybV1FCWXeaVjjGDow'),
	43	: ('X-CSRFToken', 'IjdlNzYyMzZiZGI1OWJjZDI3NmExMTg0OGU3OGM4ZjI4NzdkYmMwZmMi.Ykvy2g.yIkUUMhCbgy9ltl921oYWEFBLyM'),
	44	: ('Sec-Fetch-Mode', 'same-origin'),
	45	: ('Sec-Fetch-Dest', 'empty'),
	48	: ('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundaryeoW7XBYpazf0Y0uG'),
	49	: ('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundary9nA69TfFQg8qZOib'),
	50	: ('Content-Type', 'multipart/form-data; boundary=----WebKitFormBoundaryCpth1F5kvN4Pl8UH')
}

conn = http.client.HTTPSConnection("bax08s.am.gxo.com", 443)

headers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
response, responseHeaders = makeRequest(conn, "GET", "/handm/login/", headers, None)
csrfToken = re.findall(r'csrf.*value="(.*)">', response)[0]
print(csrfToken)
cookieHeaders = re.findall(r'Set-Cookie: (.*);', str(responseHeaders))
cookieHeader = functools.reduce(lambda a, b: a + b[:b.find(';')] + '; ', cookieHeaders, '')[:-2]

headers = [0, 1, 37, 38, 2, 3, 4, 5, 14, 39, 6, 7, 16, 9, 10, 11, 31, 12, 13, 32]
params = 'csrf_token=' + csrfToken + '&version=1.2.4&username=tponce&password=Welcome1234567&execution=&_eventId=submit&geolocation=&submit=Log+In'
lookupHeaders[37] = ('Content-Length', str(len(params)))
lookupHeaders[32] = ('Cookie', cookieHeader)
print('loging in...')
response, responseHeaders = makeRequest(conn, "POST", "/handm/login/", headers, params)
print(response, responseHeaders)
#
for i in range(len(cookieHeaders)):
	if cookieHeaders[i].find('session') != -1:
		cookieHeaders[i]= 'session=' + re.findall(r'session=(.*);', str(responseHeaders))[0]
cookieHeader = functools.reduce(lambda a, b: a + b[:b.find(';')] + '; ', cookieHeaders, '')[:-2]
lookupHeaders[32] = ('Cookie', cookieHeader)
print(lookupHeaders[32])
print(lookupHeaders[40])
print('loading main dashboard...')
headers = [0, 1, 38, 5, 6, 7, 16, 9, 10, 11, 2, 3, 4, 31, 12, 13, 40]
response, responseHeaders = makeRequest(conn, "GET", "/handm/superset/dashboard/1000000/", headers, None)
csrfToken = re.findall(r'csrf.*value="(.*)">', response)[0]
print(csrfToken)
lookupHeaders[43] = ('X-CSRFToken', csrfToken)

print('load random api')
headers = [0, 1, 2, 43, 3, 6, 4, 33, 16, 44, 45, 41, 12, 13, 42]
response, responseHeaders = makeRequest(conn, "GET", "/csstemplateasyncmodelview/api/read", headers, None)
# print(response[:200])
print('load another random api')
headers = [0, 1, 2, 43, 3, 6, 4, 33, 16, 44, 45, 41, 12, 13, 42]
response, responseHeaders = makeRequest(conn, "GET", "/handm/csstemplateasyncmodelview/api/read", headers, None)


print('load aging totes report')
# headers = [0, 1, 37, 2, 43, 3, 48, 6, 4, 33, 14, 16, 44, 45, 41, 12, 13, 42]
# params = '{"datasource":"1003238__table","viz_type":"table","slice_id":1001929,"url_params":{},"granularity_sqla":null,"time_grain_sqla":"P1D","time_range":"No filter","groupby":[],"metrics":[],"percent_metrics":[],"timeseries_limit_metric":null,"row_limit":1000,"include_time":false,"order_desc":true,"all_columns":["ORDER_CREATE_DATE","CASE_CREATE_DATE","MBOLKEY","LOAD_ID","TR_TYPE","ORDERKEY","CS_ID","SSCC","CONT_KEY","MASTER_CONTAINERKEY","CARRIER","PICK_METHOD","PACKGROUPKEY","LANE","TOTALQTY","COMMENTS","LAST_USER_EDITING_LOAD","LAST_USER_EDITING_CASE"],"order_by_cols":[],"adhoc_filters":[],"table_timestamp_format":"%Y-%m-%d %H:%M:%S","page_length":0,"include_search":false,"table_filter":false,"align_pn":false,"color_pn":true,"label_colors":{},"extra_filters":[]}'
# lookupHeaders[37] = ('Content-Length', str(len(params)))
# response, responseHeaders = makeRequest(conn, "POST", "/handm/superset/explore_json/?form_data=%7B%22slice_id%22%3A1001929%7D", headers, params)
# print(response, responseHeaders)
# atr = json.loads(response)
# print(atr)



# ////////////
# headers = [0, 1, 37, 2, 43, 3, 49, 6, 4, 33, 14, 16, 44, 45, 41, 12, 13, 42]
# params = '{"datasource":"1004028__table","viz_type":"table","slice_id":1002187,"granularity_sqla":null,"time_grain_sqla":"P1D","time_range":"No filter","groupby":[],"metrics":[],"percent_metrics":[],"timeseries_limit_metric":null,"row_limit":1000,"include_time":false,"order_desc":true,"all_columns":["ORDER_CREATE_DATE_PST","CASE_CREATE_DATE_PST","MBOLKEY","LOAD_ID","TR_TYPE","SITEID","EXTERNKEY","ORDERKEY","CS_ID","SSCC","CONT_KEY","MASTER_CONTAINERKEY","CARRIER","PICK_METHOD","LANE","ROUTE","PACKGROUPKEY","TOTALQTY","COMMENTS"],"order_by_cols":[],"adhoc_filters":[],"table_timestamp_format":"%Y-%m-%d %H:%M:%S","page_length":0,"include_search":false,"table_filter":false,"align_pn":false,"color_pn":true,"label_colors":{},"extra_filters":[]}'
# lookupHeaders[37] = ('Content-Length', str(len(params)))
# response, responseHeaders = makeRequest(conn, "POST", "/handm/superset/explore_json/?form_data=%7B%22slice_id%22%3A1002187%7D", headers, params)
# atr = json.loads(response)

# print(atr)

# atr = json.loads(response)
# statuses = {}
# for record in atr['data']['records']:
# 	if record['COMMENTS'] not in statuses:
# 		statuses[record['COMMENTS']] = 1
# 	else:
# 		statuses[record['COMMENTS']] += 1
# for i in statuses:
# 	print(i, statuses[i])

# headers = [0, 1, 37, 2, 43, 3, 50, 6, 4, 33, 14, 16, 44, 45, 41, 12, 13, 42]
# params = '{"datasource":"1004031__table","viz_type":"table","slice_id":1002188,"granularity_sqla":null,"time_grain_sqla":"P1D","time_range":"No filter","groupby":[],"metrics":[],"percent_metrics":[],"timeseries_limit_metric":null,"row_limit":10,"include_time":false,"order_desc":true,"all_columns":["ORDER_CREATE_DATE_PST","CASE_CREATE_DATE_PST","MBOLKEY","LOAD_ID","TR_TYPE","EXTERNKEY","SITEID","ORDERKEY","CS_ID","SSCC","CONT_KEY","MASTER_CONTAINERKEY","CARRIER","PICK_METHOD","LANE","ROUTE","PACKGROUPKEY","TOTALQTY","COMMENTS"],"order_by_cols":[],"adhoc_filters":[],"table_timestamp_format":"%Y-%m-%d","page_length":0,"include_search":false,"table_filter":false,"align_pn":false,"color_pn":true,"label_colors":{},"extra_filters":[]}'
# print(params)
# lookupHeaders[37] = ('Content-Length', str(len(params)))
# response, responseHeaders = makeRequest(conn, "POST", "/handm/superset/explore_json/?form_data=%7B%22slice_id%22%3A1002188%7D", headers, params)
# atr = json.loads(response)
# print(atr)
