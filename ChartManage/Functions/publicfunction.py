#coding:utf-8
'''
Created on 2018/2/7

@author: gy071089
'''

from django.utils import timezone
from datetime import timedelta

def datelist(argv=30):
    result = []
    curr_date = timezone.now()
    start_date = curr_date - timedelta(days=argv)
    while curr_date != start_date:
        result.append("%04d-%02d-%02d" % (start_date.year, start_date.month, start_date.day))
        start_date = start_date + timedelta(days=1)
    result.append("%04d-%02d-%02d" % (start_date.year, start_date.month, start_date.day))
    return result
