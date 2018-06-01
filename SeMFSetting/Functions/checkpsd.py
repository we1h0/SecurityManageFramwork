#coding:utf-8
'''
Created on 2018年5月31日

@author: yuguanc
'''

import re

def checkpsd(passwd):  
    p = re.match(r'^(?=.*?\d)(?=.*?[a-zA-Z]).{6,}$',passwd)
    if p:  
        return True  
    else:  
        return False  