#coding:utf-8
'''
Created on 2017/12/4

@author: gy071089
'''

import os,requests
from xml.dom import minidom
from requests.packages import urllib3

#level_white_list= ["high", "medium","low","informational"],
'''
except_vuln = {
    "level_white_list": ["high", "medium","low","informational"],
    "bug_black_list": [
        "User credentials are sent in clear text",
        "HTML form without CSRF protection",
        "Broken links",
        "Password type input with auto-complete enabled",
        "Slow HTTP Denial of Service Attack",
        "Application error message",
    ]
}'''

def details_parse_xml(scan_id,path):
    file_name = os.path.join(path,scan_id+'.xml')
    bug_list = {}
    try:
        root = minidom.parse(file_name).documentElement
        ReportItem_list = root.getElementsByTagName('ReportItem')
        Crawler_list = root.getElementsByTagName('SiteFile')
        bug_list['starturl'] = root.getElementsByTagName('StartURL')[0].firstChild.data
        bug_list['time'] = root.getElementsByTagName('ScanTime')[0].firstChild.data
        bug_list['url'] = []
        bug_list['bug'] = []

        if Crawler_list:
            for crawl in Crawler_list:
                spider = {}
                URL = crawl.getElementsByTagName("URL")[0].firstChild.data
                fURL = crawl.getElementsByTagName("FullURL")[0].firstChild
                spider['path'] = URL
                spider['furl'] = fURL
                bug_list['url'].append(spider)
        if ReportItem_list:
            for node in ReportItem_list:
                level = node.getElementsByTagName("Severity")[0].firstChild.data
                name = node.getElementsByTagName("Name")[0].firstChild.data
                #if level in level_white_list:
                try:
                    Request = node.getElementsByTagName("Request")[0].firstChild.data
                except:
                    Request = ""
                try:
                    details = node.getElementsByTagName("Details")[0].firstChild.data
                except:
                    details = ""
                try:
                    recommendation = node.getElementsByTagName("Recommendation")[0].firstChild.data
                except:
                    details = ""

                temp = {}
                temp['name'] = name
                temp['level'] = level
                temp['request'] = Request
                temp['details'] = details
                temp['recommendation'] = recommendation
                temp['path'] = node.getElementsByTagName("Affects")[0].firstChild.data

                bug_list['bug'].append(temp)
        os.remove(file_name)
                 
    except Exception as e:
        print ("Error in parse_xml: %s" % str(e))

    return bug_list


def get_scan_xml(reporturl,scan_id,path):
    filename = os.path.join(path,scan_id+'.xml')
    urllib3.disable_warnings()
    try:
        resp = requests.get(reporturl,timeout=120,verify=False)
        content = resp.content
        fp = open(filename,'wb')
        fp.write(content)
        fp.close()
    except Exception as e:
        return e