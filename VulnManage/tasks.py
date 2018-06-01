#coding:utf-8
'''
Created on 2017/11/3

@author: gy
'''
from xml.dom.minidom import parse
from VulnManage.models import Vulnerability
from celery import shared_task
from NoticeManage.views import notice_add
from django.contrib.auth.models import User


@shared_task
def parse_cnvdxml(filepath):
    DOMTree = parse(filepath)
    collection = DOMTree.documentElement
    if collection.hasAttribute('shelf'):
        print('ok: %s' % collection.getAttribute('shelf'))
    Vulnerabities_in = collection.getElementsByTagName('vulnerability')
    for vulnerabit in Vulnerabities_in:
        try:
            number = vulnerabit.getElementsByTagName('number')[0]
            #print('number: %s' % number.childNodes[0].data)
            cveNumber = vulnerabit.getElementsByTagName('cveNumber')[0]
            #print('cveNumber: %s' % cveNumber.childNodes[0].data)
            title = vulnerabit.getElementsByTagName('title')[0]
            #print('title: %s' % title.childNodes[0].data)
            serverity = vulnerabit.getElementsByTagName('serverity')[0]
            #print('serverity: %s' % serverity.childNodes[0].data)
            product = vulnerabit.getElementsByTagName('product')[0]
            #print('product: %s' % product.childNodes[0].data)
            submitTime = vulnerabit.getElementsByTagName('submitTime')[0]
            #print('submitTime: %s' % submitTime.childNodes[0].data)
            referenceLink = vulnerabit.getElementsByTagName('referenceLink')[0]
            #print('referenceLink: %s' % referenceLink.childNodes[0].data)
            description = vulnerabit.getElementsByTagName('description')[0]
            #print('description: %s' % description.childNodes[0].data)
            formalWay = vulnerabit.getElementsByTagName('formalWay')[0]
            #print('formalWay: %s' % formalWay.childNodes[0].data)
            patchName = vulnerabit.getElementsByTagName('patchName')[0]
            #print('patchName: %s' % patchName.childNodes[0].data)
            #patchDescription = vulnerabit.getElementsByTagName('patchDescription')[0]
            #print('patchDescription: %s' % patchDescription.childNodes[0].data)
            cve_id = cveNumber.childNodes[0].data
            cnvd_id = number.childNodes[0].data
            cve_name = title.childNodes[0].data
            leave = serverity.childNodes[0].data
            scopen = product.childNodes[0].data
            introduce = description.childNodes[0].data + '\n' + referenceLink.childNodes[0].data
            fix = formalWay.childNodes[0].data + '\n' + patchName.childNodes[0].data
            update_data = submitTime.childNodes[0].data
            
            vuln_get = Vulnerability.objects.get_or_create(
                                                cve_id=cve_id,
                                                cnvd_id=cnvd_id,
                                                cve_name=cve_name,
                                                )
            vuln=vuln_get[0]
            vuln.leave=leave
            vuln.scopen = scopen
            vuln.introduce =introduce
            vuln.fix =fix
            vuln.update_data=update_data
            vuln.save()
        except Exception as e:
            pass
    data_manage={
                  'notice_title':'漏洞库更新通知',
                  'notice_body':'漏洞文件已更新' ,
                  'notice_url':'/vuln/cnvd/',
                  'notice_type':'notice',
                  }
    user_manage_list = User.objects.filter(is_superuser=True)
    for user_manage in user_manage_list:
        notice_add(user_manage,data_manage)
            
            