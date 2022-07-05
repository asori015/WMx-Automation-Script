import json
import os

# os.chdir('C:/Users/asorialimon/Documents/WMX')
f = open('Resources/bax.har', 'r')
# f = open('x.har', 'r')
f2 = open('convert.txt', 'w')
x = json.load(f)

headerTable = {
	0	: ('Host', 'api.security.wmxp008.wmx.sc.xpo.com'),
	1	: ('Connection', 'keep-alive'),
	2	: ('Content-Length', '0'),
	3	: ('Accept', 'text/json'),
	4	: ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'),
	5	: ('Content-Type', 'text/json'),
	6	: ('Origin', 'http://ont005.wmx.sc.xpo.com'),
	7	: ('Referer', 'http://ont005.wmx.sc.xpo.com/'),
	8	: ('Accept-Encoding', 'gzip, deflate'),
	9	: ('Accept-Language', 'en-US,en;q=0.9'),
	10	: ('Host', 'api.cqrs.wmxp008.wmx.sc.xpo.com'),
	11	: ('Xposc-EquipmentID', ''),
	12	: ('Xposc-DeviceID', 'PCAWS044'),
	13	: ('Authorization', ''),
    14	: ('Content-Type', 'application/json'),
	15	: ('Accept', 'application/json'),
	16	: ('Xposc-UserID', 'tponce'),
	17	: ('Xposc-SiteId', 'ONT005'),
	18	: ('Xposc-Language', 'ENG'),
	19	: ('Xposc-ClientID', '4044'),
	20	: ('Host', 'api.outbound.wmxp008.wmx.sc.xpo.com'),
    21	: ('Origin', 'http://m.ont005.wmx.sc.xpo.com'),
	22	: ('Referer', 'http://m.ont005.wmx.sc.xpo.com/'),
	23	: ('Authorization', 'Bearer eyJhbGciOiJodHRwOi8vd3d3LnczLm9yZy8yMDAxLzA0L3htbGRzaWctbW9yZSNyc2Etc2hhMjU2IiwidHlwIjoiSldUIn0.eyJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL3JvbGUiOiJTS1VESU1FTlNJT04sQ09OVEFJTkVSTUFTVEVSLElOVkxQTixJTlZTTUFSVEJBTEFOQ0UsTU9CSUxFQ09OVEFJTkVSUkVQQUNLQ0FTRSxNT0JJTEVJTlZNT1ZFLE1PQklMRUxTVUJDQVNFQ09OU09MSURBVEUsTU9CSUxFTUFTVEVSQ09OVEFJTkVSLE1PQklMRU1BU1RFUkxQTkFTU0lHTixNT0JJTEVQSUNLQ01QQ09OVCxNT0JJTEVQWlBJQ0ssTU9CSUxFUkVQTEVOLFdFQkVSUk9STE9HLENGR1BST0RVQ1RISUVSQVJDSFksQ0ZHU0VDVElPTixJTlZQTEFOVFJBTlNGRVIsTU9CSUxFQ09OVEFJTkVSQlVJTERQQUNLTEFORSxNT0JJTEVMUE5DT1VOVCxNQU5JRkVTVCxDT1VOVFJFUVVFU1RSRVZJRVcsQ1lDTEVDT1VOVElNUE9SVCxJTlZMT1QsSU5WTUFTVEVSTFBOQlVJTEQsSU5WTU9WRSxNQU5JRkVTVFBTU0VSUk9SLE1PQklMRUlOVkxPVCxNT0JJTEVQSUNLQ0FTRURST1AsTU9CSUxFUElDS0RZTkFNSUNCWU9SREVSV0lUSERST1BJRCxNT0JJTEVQSUNLT1JERVIsTU9CSUxFUUNJTlNQRUNUSU9OLE1PQklMRVJFUExFTkNMT1NFRFJPUCxNT0JJTEVVU0VSU0VUVElOR1MsQ0ZHQ0xJRU5ULENGR0RPQ0NPTkZJRyxDT05UQUlORVJNT1ZFLE1BTklGRVNUUkVQUklOVCxNQk9MLFZFUklGSUNBVElPTixBUFBPSU5UTUVOVCxDT05UQUlORVJTS1VWRVJJRklDQVRJT04sQ1JPU1NET0NLTVVMVElDT05UQUlORVIsTE9BRE1BTkFHRU1FTlQsTFBOQURKVVNULE1PQklMRUlOVlNQRUNJQUxNT1ZFLE1PQklMRUxPQURBU1NJR04sTU9CSUxFTFBOQURKVVNULE1PQklMRU1BTlVBTE1BU1RFUkNPTlRCVUlMRCxNT0JJTEVNQVNURVJMUE5NT1ZFLE1PQklMRU1PVkUsVEFTS0hJU1RPUlksVEFTS1JFUExFTlpPTkUsVEFTS1pPTkVSUExOUVVFVUUsQ0ZHQ09NUEFOWSxHT0lOVlpPTkUsTUFOSUZFU1RFWFBSRVNTLE9SREVSLFNQUkVBRFNIRUVUSU1QT1JULERPQ1JFUFJJTlQsQ0ZHU0tVTE9DQVRJT04sSU5WSE9MRCxJTlZUUkFOU0ZFUixNT0JJTEVDWUNMRUNPVU5ULE1PQklMRUdPQ0xPU0VEUk9QLE1PQklMRUxQTk1PVkUsTU9CSUxFTFBOU1RBVFVTLE1PQklMRVBJQ0tDQVNFLE1PQklMRVBJQ0tGVUxMQ0FTRUJZT1JERVJOT0RST1AsTU9CSUxFUExBTklOVk1PVkUsTU9CSUxFVkFTVFJBTlNJVENPTlRBSU5FUixOQ0ksUUNEQVRBLFJFQ0VJVkUsVEFTS0FVRElULENBU0VDT05TT0xJREFUSU9OLElOVlNOLE1PQklMRUxQTlBUV1lTRUNUSU9OLFBPLExQTkNSRUFURSxDT05UQUlORVJTSU5HTEUsQVVUT1JFUExFTixEWU5QSUNLWk9ORSxFUlJPUkxPRyxNT0JJTEVHT1JFUExFTkNBUlQsTU9CSUxFUEFMTEVUQlVJTEQsTU9CSUxFUElDS0ZVTExDQVNFQllPUkRFUixNT0JJTEVQWlBVVCxNT0JJTEVTSU5HTEVMSU5FUkNULE1PQklMRVVOTE9BRCxQUklOVFFVRVVFLFNLVUhBWk1BVCxUQVNLREFTSEJPQVJELFRBU0tSRVBMRU5JU0hNRU5ULENGR0RFVklDRVBSSU5URVIsQ0ZHV0FWRUNPREUsR09DQVNFUkVQUk9DRVNTLEdPSU5WU05BUFNIT1QsTFBOREFUQSxUQVNLUkVQTEVOUVVFVUVISVNULFRBU0taT05FUlBMTlFVRVVFSElTVCxET0NLQUNLLENPTlRBSU5FUk1VTFRJLE1BTklGRVNURU9ELE1BTklGRVNUVk9JRCxDRkdTS1UsSU5WQURKVVNUTUVOVCxJTlZMT1RBVFRSLExQTkhPU1BJVEFMLE1BU1RFUkxQTk1PVkUsTUFTVEVSTFBOUFVUQVdBWSxNT0JJTEVHT1JFUExFTixNT0JJTEVNVUxUSUNPTlRBSU5FUixNT0JJTEVQSUNLQ0xVU1RFUixNT0JJTEVQSUNLT1JERVJEUk9QLE1PQklMRVBVVEFXQVksTU9CSUxFVkFTUFVULFRBU0tJTlZNT1ZFLFRBU0tSRVBMRU5RVUVVRSxJTlZIT0xEUkVNT1ZFUVVFVUUsSU5WU1BFQ0lBTE1PVkUsSU5WVFJBTlNBQ1RJT05TLE1PQklMRUNBU0VDT05TT0xJREFUSU9OLFdBVkUsQkFUQ0hWRVJJRklDQVRJT04sQ0ZHUEFDS1BPU0lUSU9OLFRSQUNLSU5HQUREVVBEQVRFLElOVlRSQU5TRkVSUkVMT1QsTUFTVEVSTFBOLE1PQklMRUxPQUQsTU9CSUxFTFBNT1ZFLE1PQklMRUxQTkRFQ09OU09MSURBVEUsTU9CSUxFTFBOUkVDRUlQVCxNT0JJTEVQQUxMRVRNT1ZFLE1PQklMRVBJQ0tEWU5BTUlDQllPUkRFUixNT0JJTEVTWVNURU1JTkZPUk1BVElPTixDRkdQUklOVEVSLExQTlJFR1JPVVAsTU9CSUxFQ09OVEFJTkVSQlVJTERDT05TT0xMT0MsU0hJUE9SREVSLENPTlRBSU5FUlZFUklGSUNBVElPTixBU04sQ1lDTEVDT1VOVFBMQU4sQ1lDTEVDT1VOVFJFVklFVyxJTlZCQUxBTkNFLE1BU1RFUkxQTkhPTEQsTU9CSUxFR09DQVJUU0VBUkNILE1PQklMRUlOU1BFQ1QsTU9CSUxFSU5WQkFMQU5DRSxNT0JJTEVTVEFHRUNPTlRBSU5FUixQTEFOTklORyxRQ0lOU1BFQ1RJT04sQ0ZHTE9DQVRJT04sQ0ZHU1BSRUFEU0hFRVRJTVBPUlQsQ0ZHWk9ORSxJTlZIT0xEVFJBTlNBQ1RJT04sTU9CSUxFUFJJTlRRVUVVRSIsImh0dHA6Ly9zY2hlbWFzLm1pY3Jvc29mdC5jb20vd3MvMjAwOC8wNi9pZGVudGl0eS9jbGFpbXMvdXNlcmRhdGEiOiJPTlQwMDUiLCJleHAiOjE2NDkzOTgxMjQsImlzcyI6Imh0dHA6Ly9hcGkuc2VjdXJpdHkud214cDAwOC53bXguc2MueHBvLmNvbSJ9.QFOBJfTF96H8xFgX9qKS5Bd1CBN1kzK_FUPTnT_0sbrouYhDe4IctFcJrMnQwDouw-DGcyQTINBuD4xD8mw6KrpCKrcyRo9g5zowF2iZt5UQS8_5cqZDHA7Dxda_4iEwE5nqMA3NURAadT28oM2llt500e5uyfWI5b4Eq8C2oZmqpYzRPc6wv1yWpFhYExS6zDuN10IgAZu3vMQiS3Tp-OUkjMjW4frkdgD1PcGPz1GeqHK7tFhZrhoFfCndgBuiY3vx2h9JFGZgQVKKWXPe6c5OY4So-BS79bQp3dMeNAVoO7sXgiTgbqSSu4fqcHqkn0zSLW1rRWKXZCLJTm68zg'),
	24	: ('Xposc-EquipmentGroup', 'ALL'),
	25	: ('Xposc-ClientID', 'default'),
    26	: ('Host', 'api.datahelper.wmxp008.wmx.sc.xpo.com'),
    27	: ('Host', 'api.reporting.wmxp008.wmx.sc.xpo.com'),
}

headerTable = dict((v,k) for k,v in headerTable.items())
index = 28

# headerTable = {}
# index = 0

# Parse .har file and get all unique headers
for i in x['log']['entries']:
    url = i['request']['url']
    method = i['request']['method']
    headers = i['request']['headers']
    #
    if method != None and method != 'OPTIONS' and headers != [] and url.find('ont005.wmx.sc.xpo.com') == -1 and url.find('cdn.walkme.com') == -1:
        for j in headers:
            if j['name'] == 'Content-Length':
                if (j['name'], '0') not in headerTable:
                    headerTable[(j['name'], '0')] = index
                    index += 1
            elif j['name'][:1] != ':':
                if (j['name'], j['value']) not in headerTable:
                    headerTable[(j['name'], j['value'])] = index
                    index += 1

# Parse .har file again to generate index lists for every request and print out code
for i in x['log']['entries']:
    url = i['request']['url']
    method = i['request']['method']
    headers = i['request']['headers']
    indexes = []
    if method != None and method != 'OPTIONS' and headers != [] and url.find('ont005.wmx.sc.xpo.com') == -1 and url.find('cdn.walkme.com') == -1:
        for j in headers:
            if j['name'] == 'Content-Length':
                indexes.append(headerTable[(j['name'], '0')])
            elif j['name'][:1] != ':':
                indexes.append(headerTable[(j['name'], j['value'])])
		#
        f2.write('headers = ' + str(indexes) + '\n')
        if method != 'GET':
            if 'postData' in i['request']:
                f2.write('params = \'' + i['request']['postData']['text'] + '\'\n')
            else:
                f2.write('params = \'\'\n')
            f2.write('lookupHeaders[' + str(headerTable[('Content-Length', '0')]) + '] = (\'Content-Length\', str(len(params)))\n')
            f2.write('makeRequest(conn, "' + i['request']['method'] + '", "' + url[url.find('.com') + 4:] + '", headers, params)\n#\n')
            # x = "lookupHeaders[44] = ('Content-Length', str(len(params)))"
        else:
            f2.write('makeRequest(conn, "' + i['request']['method'] + '", "' + url[url.find('.com') + 4:] + '", headers, None)\n#\n')

# Print out header lookup dictionary
f2.write('lookupHeaders = {\n')
for i in headerTable:
    f2.write('\t' + str(headerTable[i]) + '\t: ' + str(i) + ',\n')

f2.write('}\n')
f2.close()
f.close()
