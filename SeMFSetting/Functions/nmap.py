#coding:utf-8
'''
Created on 2017/11/17
@author: gy
'''

import nmap

#检查目标主机指定端口是否开放
def nmap_port(host,port):
    nm = nmap.PortScanner()
    nm.scan(host,port)
    if nm[host].state()== 'up':
        return  nm[host]['tcp'][port]


#获取目标主机内所有开放端口
def nmap_host_all(host):
    nm = nmap.PortScanner()
    nm.scan(host,'0-65535')
    try:
        if nm[host].state()== 'up':
            return nm[host]['tcp']
        else:
            return 0
    except:
        return 0
    
#获取指定网段内全部存活主机
def nmap_alive_lists(segment):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=segment,arguments='-n -sn')
    except:
        return None
    return nm.all_hosts()


        