# -*- coding: utf-8 -*-
import urllib2
try: import httplib
except ImportError:
    import http.client as httplib
import urllib
import time
import json
import base64
import hmac
import uuid
from hashlib import sha1

class AliDnsApi(object):
    def __init__(self, access_key_id, access_key_secret, record_id, ip):
        self.__access_key_id = access_key_id
        self.__access_key_secret = access_key_secret
        self.__record_id = record_id
        self.__ip = ip

    def sign(self, accessKeySecret, parameters):
        sortedParameters = sorted(parameters.items(), key=lambda parameters: parameters[0])

        canonicalizedQueryString = ''
        for (k,v) in sortedParameters:
            canonicalizedQueryString += '&' + self.percent_encode(k) + '=' + self.percent_encode(v)

        stringToSign = 'POST&%2F&' + self.percent_encode(canonicalizedQueryString[1:])

        h = hmac.new(accessKeySecret + "&", stringToSign, sha1)
        signature = base64.encodestring(h.digest()).strip()
        return signature

    def percent_encode(self, encodeStr):
        encodeStr = str(encodeStr)
        res = urllib.quote(encodeStr.encode('utf8'),'')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res

    def get_request_header(self):
        return {
            'Content-type': 'application/x-www-form-urlencoded',
            "Cache-Control": "no-cache",
            "Connection": "Keep-Alive",
        }

    def get_response(self):
        connection = httplib.HTTPConnection("dns.aliyuncs.com", 80, 30)
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        parameters = { \
                'Format'        : 'json', \
                'Version'   : '2015-01-09', \
                'Action'        : 'UpdateDomainRecord', \
                'AccessKeyId'   : self.__access_key_id, \
                'SignatureVersion'  : '1.0', \
                'SignatureMethod'   : 'HMAC-SHA1', \
                'SignatureNonce'    : str(uuid.uuid1()), \
                'TimeStamp'         : timestamp, \
                'partner_id'        : '1.0', \
                'Line'        : 'default', \
                'Priority'        : '5', \
                'RR'        : 'home', \
                'TTL'        : '600', \
                'Type'        : 'A', \
                'RecordId'        : self.__record_id, \
                'Value'        : self.__ip, \
        }
        print parameters

        signature = self.sign(self.__access_key_secret,parameters)
        parameters['Signature'] = signature
        url = "/?" + urllib.urlencode(parameters)
        header = self.get_request_header();

        connection.connect()
        connection.request("POST", url, None, headers=header)
        response = connection.getresponse();
        result = response.read()
        jsonobj = json.loads(result)
        return jsonobj

if __name__ =='__main__':
    #修改以下3个参数
    access_key_id = "HPL9DJpRus8xMAL6"                       #阿里云的Access Key ID
    access_key_secret = "DLLhR72K7vHa9AHEk85EEAPhY9cjuS"     #阿里云的	Access Key Secret
    record_id = "82461988"                                   #域名的RecordId
   
    u = urllib2.urlopen('http://members.3322.org/dyndns/getip')
    ip = u.read().strip('\n')
    print "newIp:", ip

    api = AliDnsApi(access_key_id, access_key_secret, record_id, ip)
    response = api.get_response()
    print response

