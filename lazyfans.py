#! /usr/bin/python
# -*- coding:utf-8 -*-
'''
Service for sina weibo fans service platform
You can Simply start this service by shell command:
    #nohup python lazyfans.py &
The core project must be provided by a restful interface.
Request example:
    "http://lazy.changes.com.cn/fans/index.php"
All recieved message will be push to interface and the responce will be sent there
'''

import sys
import json
import socket
import ConfigParser
import fcntl
import os
import urllib
import urllib2
import base64
import re


'''
message should be json type
'''
def handler(fromdata):
    ret = re.split(r'\r\n+',fromdata)
    if (len(ret) == 4):
        retval = ret[1]
    else:
        retval = ret[7]
    print retval
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    username = config.get('Config','username')
    password = config.get('Config','password')
    server = config.get('Config','server')
    accesstoken = config.get('Config','accesstoken')
    since_id = config.get('Config','since_id')
    # Record since id 
    json_loads = json.loads(retval)
    id = json_loads['id']
    fp = open(since_id, 'w')
    fp.write('%s'%id)
    fp.close()
    # Call content dump program
    request_data = {"token":accesstoken, 'data': retval}
    request_data = urllib.urlencode(request_data)
    req = urllib2.Request(server, request_data)
    response = urllib2.urlopen(req).read() 
    print response

'''
Socker connect
'''
def connect(appkey, weibouid, since_id ,username, password):
    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error,e:
        print 'Socket init failed:%s'%e
    
    hostname = 'm.api.weibo.com'
    ipaddress = socket.gethostbyname(hostname)
    
    try:
        sock.connect((ipaddress, 80))
    except socket.error, e:
        print 'Socket connect failed:%s'%e
        sock.close()
    # Send request
    try:
        query = urllib.urlencode({'source':appkey, 'uid': weibouid, 'since_id':since_id})
        query = '/2/messages/receive.json?'+query
        str = 'GET '+query+' HTTP/1.1\r\n'
        basic = base64.b64encode(username+ ':' +password)
        str += 'Authorization: Basic '+ basic +'\r\n'
        str += 'Host:'+hostname+'\r\nConnection:keep-alive\r\n\r\n'
        sock.send(str)
    except socket.error,e:
        print 'Socket send failed:%s'%e
        sock.close()
    return sock

if __name__=='__main__':
    '''
    Run single
    '''
    config = ConfigParser.ConfigParser()
    config.readfp(open('config.ini'))
    lockfile = config.get('Config','lockfile')
    if (os.path.isfile(lockfile) == False):
        f = open(lockfile,'w')
        f.close()
    # Try to lock file
    fp = open(lockfile, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except e:
        # another instance is running
        print "Another instance is running.%s"%e
        sys.exit(0)

    appkey = config.get('Config','appkey')
    username = config.get('Config','username')
    password = config.get('Config','password')
    weibouid = config.get('Config','weibouid')
    sinceid = config.get('Config','since_id')
    if (os.path.isfile(sinceid) == False):
        since_id = ''
    else:
        fp_sd = open(sinceid, 'r')
        since_id = fp_sd.read()
        fp_sd.close()
    
    sock = connect(appkey, weibouid, since_id ,username, password)
    # Parse data
    data = ''
    while(1):
        data = ''
        try:
            data = sock.recv(1024)
        except:
            # Close by remote server
            fp_sd = open(sinceid, 'r')
            since_id = fp_sd.read()
            fp_sd.close()
            sock = connect(appkey, weibouid, since_id ,username, password)
            data = sock.recv(1024)

        if data:
            handler(data)
