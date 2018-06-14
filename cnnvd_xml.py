#! /usr/bin/python3
# -*- coding:UTF-8 -*-

from django.urls import path
from xml.dom.minidom import parse
import xml.dom.minidom,os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
django.setup()
from VulnManage.models import Vulnerability

fill_path_list = []
dome_path = os.getcwd()
files_path = os.path.join(dome_path,'cnnvd_xml')

files_list = os.listdir(files_path) 
for file_name in files_list:
    if os.path.splitext(file_name)[1] == '.xml':
        #file_path = os.path.join(files_path,file_name)
        #fill_path_list.append(file_path)
        fill_path_list.append(file_name)

for file_name in fill_path_list:
    print ('import'+file_name)
    
    os.chdir(files_path)
    DOMTree = xml.dom.minidom.parse(file_name)
    collection = DOMTree.documentElement
    if collection.hasAttribute('shelf'):
        print('ok: %s' % collection.getAttribute('shelf'))
    
    
    Vulnerabities_in = collection.getElementsByTagName('entry')
    
    for vulnerabit in Vulnerabities_in:
        try:
            number = vulnerabit.getElementsByTagName('vuln-id')[0]
            print('number: %s' % number.childNodes[0].data)
            cveNumber = vulnerabit.getElementsByTagName('cve-id')[0]
            print('cveNumber: %s' % cveNumber.childNodes[0].data)
            title = vulnerabit.getElementsByTagName('name')[0]
            print('title: %s' % title.childNodes[0].data)
            serverity = vulnerabit.getElementsByTagName('severity')[0]
            print('serverity: %s' % serverity.childNodes[0].data)
            product = vulnerabit.getElementsByTagName('product')[0]
            print('product: %s' % product.childNodes[0].data)
            submitTime = vulnerabit.getElementsByTagName('published')[0]
            print('submitTime: %s' % submitTime.childNodes[0].data)
            referenceLink = vulnerabit.getElementsByTagName('ref-url')[0]
            print('referenceLink: %s' % referenceLink.childNodes[0].data)
            description = vulnerabit.getElementsByTagName('vuln-descript')[0]
            print('description: %s' % description.childNodes[0].data)
            patchDescription = vulnerabit.getElementsByTagName('vuln-solution')[0]
            print('patchDescription: %s' % patchDescription.childNodes[0].data)
            cve_id = cveNumber.childNodes[0].data
            cnvd_id = number.childNodes[0].data
            cve_name = title.childNodes[0].data
            leave = serverity.childNodes[0].data
            scopen = product.childNodes[0].data
            introduce = description.childNodes[0].data + '\n' + referenceLink.childNodes[0].data
            fix = patchDescription.childNodes[0].data
            update_data = submitTime.childNodes[0].data
            Vulnerability.objects.get_or_create(update_data=update_data,fix=fix,cve_id=cve_id,cnvd_id=cnvd_id,cve_name=cve_name,leave=leave,scopen=scopen,introduce=introduce,)
            print(cveNumber+' is OK') 
        except:
            print('Pass')
        
        
