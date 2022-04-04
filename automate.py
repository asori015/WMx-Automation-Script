import http, http.client
import openpyxl
import threading
import concurrent.futures
import argparse
import json
import gzip
import re
from datetime import date
import logging

# Global variables
readyTotes = [] # All totes status 160 and up will be stored here and then passed to 'loadTotes()' for loading
masteredTotes = {} # Dictionary for storing only *one* container for each masterbuild
unmasteredTotes = {} # Same thing but for 161's
storeBlacklist = ['108', '196'] # Stores that will not be worked on by the script
f = '' # File handler

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
	24	: ('Xposc-EquipmentGroup', 'ALL'),
	25	: ('Xposc-ClientID', 'default'),
	26	: ('Host', 'api.datahelper.wmxp008.wmx.sc.xpo.com'),
    27	: ('Host', 'api.reporting.wmxp008.wmx.sc.xpo.com'),
}

def addThrees(value):
    newValue = ''
    for row in value:
        newValue += '3' + row
    return newValue

def getHeaders(indexes):
    headerDict = {}
    for row in indexes:
        headerDict.update({headerTable[row][0]: headerTable[row][1]})
    return headerDict

def makeRequest(conn, method, path, indexes, payload):
    conn.request(method, path, payload, getHeaders(indexes))
    res = conn.getresponse()
    f.write(str(res.status) + ', ' + str(res.reason) + '\n')
    data = res.read()
    try:
        f.write(method + " " + path + "\n" + data.decode('utf-8') + '\n')
    except:
        f.write(method + " " + path + "\n" + gzip.decompress(data).decode('utf-8') + '\n')
    return data

def initWMx():
    print('Initializing WMx connection')
    conn = http.client.HTTPConnection("172.19.45.163", 80)
    
    headers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    params = '{"UserId":"tponce","Psw":"Welcome123456","SiteId":"ONT005"}'
    headerTable[2] = ('Content-Length', str(len(params)))
    response = makeRequest(conn, "POST", "/login", headers, params)
    headerTable[13] = ('Authorization', 'Bearer ' + json.loads(gzip.decompress(response))['Token'])
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/equipmentgroupdd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/clientdd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/deviceprinters/5043415753303434", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/userprofile/74706f6e6365", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/listboxdd/434c49454e54", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/usersearch/57585f434f4e5441494e45525f53484950/434f4e5441494e455253494e474c45", headers, None)
    
    headers = [10, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = '{"CONTAINERKEY":"0002401084"}'
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/queryservice/data/57585f434f4e5441494e45525f53484950/4144445453/66616c7365/31/3330", headers, params)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/searchconfig/57585f434f4e5441494e45525f53484950", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/listboxdd/434f4e5441494e4552535441545553", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containerstatusdd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/cartonizecodesdd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containership/", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/434f4e5441494e455244454641554c54484549474854", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/434e54424c4443415054555245494e445543544c4f43", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/usersearch/57585f434f4e5441494e45525f5348495044544c/434f4e5441494e455253494e474c45", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/searchconfig/57585f434f4e5441494e45525f5348495044544c", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/554944544c5041474553495a45", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configpropattr/434f4e5441494e455253494e474c45", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/searchconfig/57585f434f4e5441494e45525f5348495044544c", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configpropattr/434f4e5441494e455253494e474c45", headers, None)

    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configpropattr/434f4e5441494e455253494e474c45", headers, None)
    return conn

def getNewLoadID(conn):
    print('looking for new Dummy Load ID...')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/4d4f42494c45545241494c45524c4f4144414456534541524348", headers, None)
    # Here we get all relevant load IDs and look for the first B05 load that's status 101 New
    headers = [20, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    response = makeRequest(conn, "GET", "/container/activeloads", headers, None)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/searchconfig/57585f4c4f4144", headers, None)
    #
    activeLoads = json.loads(response)
    dummyLoads = []
    for load in activeLoads:
        if load['TRAILERTYPE'] == 'B05' and load['STATUS'] == 101:
            dummyLoads.append(load['LOADID'])
    #
    if len(dummyLoads) == 0:
        print('No B05 Load IDs found. What the hell happened?')
        input('Press anything to continue...')
        return ''
    dummyLoads.sort()
    dummyLoad = dummyLoads[0]
    print('Found LOAD_ID: ' + dummyLoad)
    if input('Use this Load ID? (Y/N)') != 'Y':
        return ''
    print('Utilizing Dummy Load: ' + dummyLoad)
    #
    headers = [10, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = '{"LOADID":"' + dummyLoad + '"}'
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/queryservice/data/57585f4c4f4144/4144445453/66616c7365/31/3330", headers, params)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/load/" + addThrees(dummyLoad), headers, None)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/usersearch/57585f4c4f414444544c/4c4f41444d414e4147454d454e54", headers, None)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/4c4f414444544c42594f52444552", headers, None)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/loadDtlList/" + addThrees(dummyLoad), headers, None)

    # Updating our chosen load ID with correct values
    response = json.loads(response)
    response['SEALNUMBER'] = 'SN' + dummyLoad
    response['TRAILERNUMBER'] = 'DUMMY' + date.today().strftime('%m%d%y')
    response['DOOR'] = 'S9'
    response['LOADTYPE'] = 'VIA_SP'
    response = json.dumps(response)
    #
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = response
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/isloaddirty", headers, params)
    #
    headers = [26, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = response
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/datamodify/saveload", headers, params)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/load/" + addThrees(dummyLoad), headers, None)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/4c4f414444544c42594f52444552", headers, None)
    #
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/loadDtlList/" + addThrees(dummyLoad), headers, None)
    return dummyLoad

def handle_118(conn):
    print('TODO')
    return
    # print('118\'s are handled in')
    # This request just fails...
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/usersearch/57585f57415645/57415645", headers, None)
    # Here we're grabbing every wave that's status 118 or below.
    headers = [10, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = '{"STATUS":"102|105|106|112|115|116|118|101"}'
    headerTable[2] = ('Content-Length', str(len(params)))
    response = makeRequest(conn, "PUT", "/queryservice/data/57585f57415645/4144445453/66616c7365/31/3330", headers, params)
    #
    response = json.loads(response)
    numberOfWaves = response['Count']
    currentWaves = response['Data']
    pageNumber = 2
    while numberOfWaves > 30:
        headers = [10, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        params = '{"STATUS":"102|105|106|112|115|116|118|101"}'
        headerTable[2] = ('Content-Length', str(len(params)))
        response = makeRequest(conn, "PUT", "/queryservice/data/57585f57415645/4144445453/66616c7365/" + addThrees(str(pageNumber)) + "/3330", headers, params)
        #
        response = json.loads(response)
        currentWaves += response['Data']
        numberOfWaves -= 30
        pageNumber += 1
    #
    casesInWaves = []
    for wave in currentWaves:
        if wave['LINECOUNT'] == 0:
            continue
        waveKey = wave['WAVEKEY']
        print(waveKey)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/wavecodefilteroperatorsdd", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/wavestatusdd", headers, None)
        #
        # headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        # params = '{}'
        # lookupHeaders[2] = ('Content-Length', str(len(params)))
        # response = makeRequest(conn, "PUT", "/waveprocess/updwavestatus/" + addThrees(waveKey), headers, params)
        # response = json.loads(response)
        # if response['LINECOUNT'] == 0:
        #     continue
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/wavedetailsbywavekey/" + addThrees(waveKey), headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/usersearch/434f52454f52445f5741564544544c5f5657/57415645", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/searchconfig/434f52454f52445f5741564544544c5f5657", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/usersearch/57585f4f524445525f43415345/57415645", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/searchconfig/57585f4f524445525f43415345", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/searchconfig/57585f4f524445525f43415345", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/listboxdd/4f52444552535441545553", headers, None)
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        response = makeRequest(conn, "GET", "/queryservice/ordercasebywavekey/" + addThrees(waveKey), headers, None)
        # print(response)
        if len(response) > 2:
            response = json.loads(response)
            casesInWaves += response
        #
        headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
        makeRequest(conn, "GET", "/queryservice/autoprocesswave/" + addThrees(waveKey), headers, None)
        #
    #
    print(casesInWaves)
    
def handle_125():
    print('125\'s are handled in Grey Orange. Skipping...')

def handle_130():
    print('130\'s are handled in Grey Orange. Skipping...')

def handle_135(conn, sscc):
    print('Handling status 135 tote')
    response = ''
    caseID = ''
    containerKey = ''
    print('1')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/order/" +  addThrees(sscc) + "/case", headers, None)
    caseID = re.findall(r'"CASEID":"(\d*)"', response.decode('utf-8'))[0]
    print('2')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = ''
    headerTable[2] = ('Content-Length', str(len(params)))
    response = makeRequest(conn, "PUT", "/container/opencontainersingle/" + addThrees(caseID) + "/", headers, params)
    containerKey = response.decode('utf-8')[1:-1]
    print('3')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containership/" + addThrees(containerKey), headers, None)
    print('4')
    #This request for whatever reason always gets 404
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containershipdetailsbycontainerkey/" + addThrees(containerKey), headers, None)
    print('5')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = '{}'
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/addcasesingle/" + addThrees(containerKey) + "/" + addThrees(caseID) + "/", headers, params)
    print('6')
    #The response from this query gets fed into the 'iscontainerdirty' request
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/containership/" + addThrees(containerKey), headers, None)
    print('7')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/carrierdd", headers, None)
    print('8')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containershipdetailsbycontainerkey/" + addThrees(containerKey), headers, None)
    print('9')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/434e545041434b4147455459504557495448434152544f4e54595045", headers, None)
    print('10')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = response.decode('utf-8')
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/iscontainerdirty", headers, params)
    print('11: Requesting to close container')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = '{}'
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/closepackedcontainersingle/" + addThrees(containerKey), headers, params)
    print('12')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containership/" + addThrees(containerKey), headers, None)
    print('13')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/containershipdetailsbycontainerkey/" + addThrees(containerKey), headers, None)
    print('14')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/434e545041434b4147455459504557495448434152544f4e54595045", headers, None)
    return containerKey

def handle_140(conn, sscc):
    print('Handling status 140 tote')
    return handle_135(conn, sscc) # Status 140 totes function almost the same as status 135 totes

def handle_141(conn, sscc):
    print('TODO')
    return
    print('Handling status 141 tote')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/orderstatusdd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/verdoctypedd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/config/434f5245564552494659/5645524849444544455441494c", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configpropattr/564552494649434154494f4e534541524348", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configpropattr/4f52444552564552494659", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configpropattr/434f4e5441494e455253494e474c45", headers, None)
    # Entering in an SSCC value
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/order/" + addThrees(sscc) + "/case", headers, None)
    
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = '""'
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/verification/create/43415345/" + addThrees(sscc), headers, params)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/order/" + addThrees(sscc) + "/case", headers, None)
    response = json.loads(response)
    caseID = response['CASEID']
    orderKey = response['ORDERKEY']
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/usersearch/434f52455645525f4f524445525f5645524946595f5657/564552494649434154494f4e", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/searchconfig/434f52455645525f4f524445525f5645524946595f5657", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/cartonizecodedd", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/tracebydoctypedockey/open/4f52444552/" + addThrees(orderKey), headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/listboxdd/4f52444552535441545553", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/listboxdd/4f52444552535441545553", headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/tracebydoctypedockey/open/43415345/" + addThrees(caseID), headers, None)
    
    headers = [20, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/verification/gervergrpdd/43415345/" + addThrees(sscc), headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/order/" + addThrees(sscc) + "/case", headers, None)
    
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    params = response.decode('utf-8')
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/verification/instructions/case/43415345", headers, params)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    makeRequest(conn, "GET", "/queryservice/order/" + addThrees(orderKey), headers, None)
    
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/orderverifyviewbydoctype/43415345/" + addThrees(caseID), headers, None)
    response = json.loads(response)
    
    for skuRecord in response:
        count = skuRecord['PICKQTY'] - skuRecord['VERIFYQTY']
        while count > 0:
            headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            makeRequest(conn, "GET", "/queryservice/codelist/56455251545945444954", headers, None)
            
            headers = [27, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            params = '"' + skuRecord['SKU'] + '"'
            headerTable[2] = ('Content-Length', str(len(params)))
            makeRequest(conn, "POST", "/format/parselist/534b554c4142454c/3030/3138", headers, params)
            
            headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            makeRequest(conn, "GET", "/queryservice/tracebydoctypedockey/open/534b55/" + addThrees(sku), headers, None)
            
            headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            makeRequest(conn, "GET", "/queryservice/tracebydoctypedockey/open/564552534b55/" + addThrees(sku), headers, None)
            
            headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            params = '{"ORDERVERIFYID":27110881,"SITEID":"ONT005","CASEID":"0011847104","ORDERKEY":"0003772380","ORDERLINENO":9,"SKU":"000990977002214005","DESCRIPTION":"Sweater White, L","SERIAL_FLAG":"N","CLIENTID":"4044","LOT":"LOT","PICKQTY":3,"VERIFYQTY":0,"UOM":"EA","UOM_LEVEL":1,"UOMQTY":3,"UOMCONVQTY":1,"NONINVENTORY_FLAG":"N","DATACAPTURE_FLAG":"N","DATACAPTURECODE":null,"VALIDATE_FLAG":"N","VALIDATECODE":null,"VERIFYWHO":null,"DEFECT_FLAG":"N","DEFECTCODE":null,"DEFECTNOTES":null,"PICKER":null,"RESOLVECODE":null,"RESOLVEWHO":null,"HAZMAT_FLAG":"N","HAZMATCODE":null,"PACK_FLAG":"N","PACKTS":null,"PACKWHO":null,"PACKREFKEY":null,"DROPID":null,"ORDERPICKID":33851009,"STATUS":141,"STATUSTS":"2022-03-12T18:16:07.180676-05:00","VERGROUPCD":null,"VERGROUPKEY":null,"ADDTS":"2022-03-12T18:16:07.180682-05:00","ADDWHO":"yharosvargas","EDITTS":"2022-03-12T18:16:07.180685-05:00","EDITWHO":"yharosvargas","SKUSCAN_FLAG":"Y","LOTATR1":null,"LOTATR2":null,"LOTATR3":null,"LOTATR4":null,"LOTATR5":null,"LOTATR6":null,"LOTATR7":null,"LOTATR8":null,"CARTONTYPE":"A16"}'
            headerTable[2] = ('Content-Length', str(len(params)))
            makeRequest(conn, "PUT", "/verification/instructions/verifyline", headers, params)
            
            headers = [20, 1, 2, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            params = '""'
            headerTable[2] = ('Content-Length', str(len(params)))
            makeRequest(conn, "PUT", "/verification/verifydetail/3237313130383831/31", headers, params)
            
            headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            makeRequest(conn, "GET", "/queryservice/sku/" + addThrees(sku), headers, None)
            
            headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 6, 7, 8, 9]
            makeRequest(conn, "GET", "/queryservice/orderverifyviewbydoctype/43415345/" + addThrees(caseID), headers, None)

def handle_150(conn, sscc):
    print('Handling status 150 tote')
    return handle_135(conn, sscc) # Status 150 totes function almost the same as status 135 totes

def handle_160():
    print('Handling status 160 tote') # We don't really need to do anything for this status.

def handle_161(conn, sscc, row):
    print('Handling status 161 tote')
    unmasteredTotes[row[11].value] = row[10].value

def handle_165(row):
    print('Handling status 165 tote')
    masteredTotes[row[11].value] = row[10].value

def masterTotes(conn, containerKey):
    print('Mastering stack...')
    print('1: Looking up master container')
    headers = [20, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/container/lookupmastercontainer/" + addThrees(containerKey), headers, None)
    
    print('2: Closing master container')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    params = '{}'
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/closemastercontainer/" + addThrees(containerKey), headers, params)
    return containerKey

def loadTotes(conn, loadID, containerKeys):
    print('Loading all totes to Load ID:' + loadID)
    
    #First we enter the loadID
    print('1')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/loadSearch/" + addThrees(loadID), headers, None)

    print('2')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    response = makeRequest(conn, "GET", "/queryservice/load/" + addThrees(loadID), headers, None)
    
    print('3')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/uiconfig/4d4f42494c454c4f4144/4d4f42494c45", headers, None)
    
    print('4')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/trailertypedd", headers, None)
    
    print('5')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/uiconfig/4d4f42494c454c4f4144/4d4f42494c45", headers, None)
    
    print('6')
    headers = [10, 1, 11, 12, 13, 14, 15, 16, 4, 17, 18, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/uiconfig/4d4f42494c454c4f4144/4d4f42494c45", headers, None)
    #Then we process the load ID
    
    print('7')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    params = response.decode('utf-8')
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/isloaddirty", headers, params)
    
    print('8')
    headers = [20, 1, 2, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    params = response.decode('utf-8')
    headerTable[2] = ('Content-Length', str(len(params)))
    makeRequest(conn, "PUT", "/container/saveload", headers, params)
    
    print('9')
    headers = [20, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/container/activeloads", headers, None)
    
    print('10')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/configbyconfigid/all/4c4f4144444f4f52434f4e4649524d", headers, None)
    
    print('11')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/load/" + addThrees(loadID), headers, None)
    
    print('12')
    headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
    makeRequest(conn, "GET", "/queryservice/loadDtlList/" + addThrees(loadID), headers, None)
    
    for containerKey in containerKeys:
        #This is us loading a containerKey
        print('13: Loading container ' + containerKey)
        headers = [20, 1, 2, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
        params = '{}'
        headerTable[2] = ('Content-Length', str(len(params)))
        makeRequest(conn, "PUT", "/container/loadcontainer/" + addThrees(loadID) + "/" + addThrees(containerKey) + "/5339/302e646f76716f386a6c366774", headers, params)
        
        print('14')
        headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
        makeRequest(conn, "GET", "/queryservice/load/" + addThrees(loadID), headers, None)
        
        print('15')
        headers = [10, 1, 11, 12, 13, 14, 15, 18, 24, 17, 16, 4, 19, 21, 22, 8, 9]
        makeRequest(conn, "GET", "/queryservice/loadDtlList/" + addThrees(loadID), headers, None)

def handleAllTotes(conn, wb):
    sheet_ranges = wb['Sheet1']

    # Loop through every tote in sheet and process it based on its status
    for row in sheet_ranges:
        blacklisted = False
        for store in storeBlacklist:
            if row[16].value.find('US0' + store) != -1:
                blacklisted = True
                break
        #
        if blacklisted:
            continue
        #
        status = row[18].value[:3] # first three letters of cell value in 18th column
        if status == '118':
            # handle_118()
            continue
        elif status == '125':
            handle_125()
        elif status == '130':
            handle_130()
        elif status == '135':
            try:
                readyTotes.append(handle_135(conn, row[9].value))
            except http.client.HTTPException:
                print('Connection is broken. Restarting connection to WMx.')
                conn = initWMx()
            except:
                print('Error Occcured')
        elif status == '140':
            try:
                readyTotes.append(handle_140(conn, row[9].value))
            except http.client.HTTPException:
                print('Connection is broken. Restarting connection to WMx.')
                conn = initWMx()
            except:
                print('Error Occcured')
        elif status == '141':
            try:
                handle_141(conn, row[9].value)
                readyTotes.append(handle_135(conn, row[9].value))
            except http.client.HTTPException:
                print('Connection is broken. Restarting connection to WMx.')
                conn = initWMx()
            except:
                print('Error Occcured')
        elif status == '150':
            try:
                readyTotes.append(handle_150(conn, row[9].value))
            except http.client.HTTPException:
                print('Connection is broken. Restarting connection to WMx.')
                conn = initWMx()
            except:
                print('Error Occcured')
        elif status == '160':
            handle_160()
            readyTotes.append(row[10].value)
        elif status == '161':
            handle_161(conn, row[10].value, row)
        elif status == '165':
            handle_165(row)
        else:
            if status != 'COM':
                print('Tote status ' + status + ' is not handled by this script.')

def formatExcelSheet(workBook):
    print('Formatting Excel Sheet')

    splitPoints = set()
    red = openpyxl.styles.PatternFill(fill_type='solid', start_color='FF0000', end_color='FF0000')
    yellow = openpyxl.styles.PatternFill(fill_type='solid', start_color='FFFF00', end_color='FFFF00')
    green = openpyxl.styles.PatternFill(fill_type='solid', start_color='00B050', end_color='00B050')
    currentSheet = workBook['Sheet1']
    currentSheet.column_dimensions['C'].width = len('PROCESSED, ASSUMED SHIPPED ')
    currentSheet['C1'] = 'NOTES'

    # Color code every row based on the status it has
    for count, row in enumerate(currentSheet):
        if count == 0:
            continue
        status = row[18].value[:3]
        if status < '135':
            for cell in row:
                cell.fill = red
            row[2].value = 'NEEDS IT SUPPORT'
        elif status < '180':
            for cell in row:
                cell.fill = yellow
            row[2].value = 'PROCESSED, ASSUMED SHIPPED'
        else:
            for cell in row:
                cell.fill = green
            if row[2].value == None:
                row[2].value = 'ON DOCK'

        splitPoint = row[12].value[2:5]
        splitPoints.add(splitPoint)

    # Delete all sheets except for 'Sheet 1'
    for sheet in workBook:
        if sheet.title != 'Sheet1':
            del workBook[sheet.title]

    # Copy 'Sheet1' for every splitpoint and delete all rows that arn't for that splitpoint
    for splitPoint in sorted(splitPoints):
        print('Formating ' + splitPoint)
        newSheet = workBook.copy_worksheet(workBook['Sheet1'])
        newSheet.title = splitPoint + ' ' + date.today().strftime('%m.%d.%y')

        row = 2
        cellName = 'M' + str(row)
        while newSheet[cellName].value != None:
            if newSheet[cellName].value[2:5] != splitPoint:
                newSheet.delete_rows(row)
                row -= 1
            row += 1
            cellName = 'M' + str(row)

def run(threadID: int):
    print('here1', threadID)
    with logLock:
        print('inside lock')
        logger.debug('Starting thread %s', threadID)
        print('leaving lock')
    print('here2', threadID)
    # global f
    # f = open('output.txt', 'w')

    # Open Excel sheet
    # wb = openpyxl.load_workbook(filename = 'Resources/totes.xlsx')
    # sheet_ranges = wb['Sheet1']
    # formatExcelSheet(wb)

    # Establish WMx initial connection
    # conn = initWMx()
    # dummyLoad = getNewLoadID(conn)

    #handleAllTotes(conn, wb)
    #handle_118(conn)

    # Master 161s and add to loading list
    # for row in unmasteredTotes:
    #     readyTotes.append(masterTotes(conn, unmasteredTotes[row]))

    # Add 165s to loading list
    # for row in masteredTotes:
    #     readyTotes.append(masteredTotes[row])

    # If we have selected a Load_ID for loading
    # if dummyLoad != '':
    #     loadTotes(conn, dummyLoad, readyTotes)

    # wb.save(filename = 'Resources/otr.xlsx')
    # conn.close()
    # f.close()

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Automates WMx Dummy Load",
        epilog="Please use responsibly..."
    )
    parser.add_argument(
        "-v", "--version", 
        action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument(
        "-f", "--format",
        action = 'store_true',
        help='Format otr into excel sheet.'
    )
    parser.add_argument(
        '-l', '--loadid',
        type=str,
        help='Load ID to be used for loading.'
    )
    parser.add_argument(
        '-t', '--threads',
        type=int,
        help='Number of threads this script will generate.'
    )
    return parser

logLock = threading.Lock()
def main() -> None:
    # Set up logging for this script
    logging.basicConfig(format='(%(name)s - %(levelname)s) %(message)s', level=logging.DEBUG, filename='log.txt', filemode='w')

    # Parse CLI arguments
    parser = init_argparse()
    args = parser.parse_args()
    logging.debug('args = %s', args)

    # Create threads
    logging.debug('args.threads = %s', args.threads)
    # logLock = threading.Lock()
    if args.threads is not None and args.threads > 0:
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as executor:
            # executor.submit(run, 0, [logLock])
            executor.map(run, range(args.threads))

if __name__ == '__main__':
    main()
