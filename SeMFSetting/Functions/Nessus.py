#coding:utf-8

import requests
import json
import time
from requests.packages import urllib3
from SeMFSetting.models import Scanner
# Create your views here.

verify = False

def get_scannerinfo(scanner_id):
    
    scanner = Scanner.objects.filter(id=scanner_id).first()

    url = scanner.scanner_url
    Access_Key = scanner.scanner_apikey
    Secret_Key = scanner.scanner_apisec
    return url,Access_Key,Secret_Key


def build_url(url,resource):
    return '{0}{1}'.format(url, resource)


def connect(scanner_id,method, resource, data=None):
    '''
    该模块用来定制连接
    '''
    url,Access_Key,Secret_Key=get_scannerinfo(scanner_id)
    
    headers = {
               'content-type': 'application/json',
               'X-ApiKeys':'accessKey = '+ Access_Key +';secretKey ='+Secret_Key,
               }
    if data != None:
        data = json.dumps(data)
    urllib3.disable_warnings()
    if method == 'POST':
        r = requests.post(build_url(url,resource), data=data, headers=headers, verify=verify)
    elif method == 'PUT':
        r = requests.put(build_url(url,resource), data=data, headers=headers, verify=verify)
    elif method == 'DELETE':
        r = requests.delete(build_url(url,resource), data=data, headers=headers, verify=verify)
    else:
        r = requests.get(build_url(url,resource), params=data, headers=headers, verify=verify)
    
    # Exit if there is an error.
    if r.status_code != 200:
        e = r.json()
        print(e)
        #sys.exit()
        
    if 'download' in resource:
        return r.content
    else:
        try:
            return r.json()
        except:
            return True
    
    
def get_policies(scanner_id):
    """
    Get scan policies
    Get all of the scan policies but return only the title and the uuid of
    each policy.
    """
    data = connect(scanner_id,'GET', '/policies')
    return dict((p['name'], p['template_uuid']) for p in data['policies'])

def add(name, desc, targets, uuid,scanner_id):
    """
    Add a new scan

    Create a new scan using the policy_id, name, description and targets. The
    scan will be created in the default folder for the user. Return the id of
    the newly created scan.
    """
    scan = {
        'uuid': uuid,
        'settings': {
            'name': name,
            'description': desc,
            'text_targets': targets
        }
    }
    data = connect(scanner_id,'POST', '/scans', scan)
    return data['scan']

def launch(sid,scanner_id):
    """
    Launch a scan
    Launch the scan specified by the sid.
    """
    data = connect(scanner_id,'POST', '/scans/{0}/launch'.format(sid))
    return data['scan_uuid']


def stop(sid,scanner_id):
    """
    Stop a scan
    Stop the scan specified by the sid.
    """
    data = connect(scanner_id,'POST', '/scans/{0}/stop'.format(sid))
    return data

def pause(sid,scanner_id):
    """
    Pause a scan
    Pause the scan specified by the sid.
    """
    data = connect(scanner_id,'POST', '/scans/{0}/pause'.format(sid))
    return data

def resume(sid,scanner_id):
    """
    Resume a scan
    Resume the scan specified by the sid.
    """
    data = connect(scanner_id,'POST', '/scans/{0}/resume'.format(sid))
    return data

def details(sid,scanner_id):
    """
    Details a scan
    Details the scan specified by the sid.
    """
    data = connect(scanner_id,'GET', '/scans/{0}'.format(sid))
    return data

def get_plugin_output(sid,host_id,plugin_id,scanner_id):
    data = connect(scanner_id,'GET','/scans/{0}/hosts/{1}/plugins/{2}'.format(sid,host_id,plugin_id))
    return data

if __name__ == '__main__':
    pass
    '''
    policies = get_policies()
    pid = policies['Advanced Scan']
    scan = add('test','this is a test','10.10.19.5',pid)
    scan_id=scan['id']
    print(scan_id)
    scan_uuid=launch(scan_id)
    #res=pause(sid)
    #res=resume(sid)
    while True:
        res = details(scan_id)
        if res['info']['status'] == 'completed':
            res = details(scan_id)['vulnerabilities']
            break
        time.sleep(300)
        
    print(res)
    '''
