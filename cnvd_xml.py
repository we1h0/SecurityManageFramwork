#! /usr/bin/python3
# -*- coding:UTF-8 -*-
from django.urls import path
import xml.dom.minidom,os,shutil
import django

def renew_vuln_xml():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SeMF.settings')
    django.setup()
    from VulnManage.models import Vulnerability

    fill_path_list = []
    dome_path = os.getcwd()
    files_path = os.path.join(dome_path, 'cnvd_xml')
    files_path_old = os.path.join(dome_path, 'cnvd_xml','xml_file')

    files_list = os.listdir(files_path)
    for file_name in files_list:
        if os.path.splitext(file_name)[1] == '.xml':
            # file_path = os.path.join(files_path,file_name)
            # fill_path_list.append(file_path)
            fill_path_list.append(file_name)

    for file_name in fill_path_list:
        print('import' + file_name)
        os.chdir(files_path)
        DOMTree = xml.dom.minidom.parse(file_name)
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
                patchDescription = vulnerabit.getElementsByTagName('patchDescription')[0]
                #print('patchDescription: %s' % patchDescription.childNodes[0].data)
                cve_id = cveNumber.childNodes[0].data
                cnvd_id = number.childNodes[0].data
                cve_name = title.childNodes[0].data
                leave = serverity.childNodes[0].data
                scopen = product.childNodes[0].data
                introduce = description.childNodes[0].data + '\n' + referenceLink.childNodes[0].data
                fix = formalWay.childNodes[0].data + '\n' + patchName.childNodes[0].data + '\n' + \
                      patchDescription.childNodes[0].data
                update_data = submitTime.childNodes[0].data
                Vulnerability.objects.get_or_create(update_data=update_data, fix=fix, cve_id=cve_id, cnvd_id=cnvd_id,
                                                       cve_name=cve_name, leave=leave, scopen=scopen,
                                                       introduce=introduce )
                print(cve_id + ' is OK')
            except:
                print('Pass')
        shutil.move(os.path.join(files_path,file_name),os.path.join(files_path_old,file_name))


if __name__ == "__main__":
    renew_vuln_xml()
