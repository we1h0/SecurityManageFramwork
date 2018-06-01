#coding:utf-8
'''
Created on 2018年5月12日

@author: yuguanc
'''


from django.core.mail import EmailMultiAlternatives

from SeMF.settings import DEFAULT_FROM_EMAIL,WEB_URL


url = WEB_URL


def sendmails(email,data):
    '''
    data={'subject':'',
          'text_content',
          'html_content'}
    '''
    try:
        msg = EmailMultiAlternatives(data['subject'],data['text_content'],DEFAULT_FROM_EMAIL,[email])
        msg.attach_alternative(data['html_content'], "text/html")
        msg.send()
        return True
    except:
        return False
    
    
def sendregistmail(email,argu):
    data={'subject':'SeMF账号初始化',
          'text_content':'',
          'html_content':''}
    data['text_content'] = "您的SeMF安全管理平台账号初始化地址如下"+ url +"/view/regist/"+argu +"  如无申请过该平台账号，请忽略该邮件"
    data['html_content'] = """
    <p>Dear user:</p>
    <p>    您的SeMF安全管控平台账号初始化地址已创建，<a href='"""+ url +"/view/regist/"+argu +"""'>点我</a>以完成账号初始化</p>
    <p>    如点击失效，请前往访问以下地址""" + url +"/view/regist/"+argu + """</p>
    <p>    如非本人操作，忽略该邮件</p>
    <p>    本邮件为安全管控平台SeMf系统邮件，请勿回复</p>
    """
    res = sendmails(email,data)
    if res:
        return True
    else:
        return False
    
    
def send_notice_mail(email,data):
    try:
        subject = data['notice_title']
        text_content = data['notice_body']+'访问地址为：'+url+data['notice_url']
        html_content = "<p>"+data['notice_body']+"，<a href='"+url+data['notice_url']+"'><a>点我访问</a></p>"
        msg = EmailMultiAlternatives(subject,text_content,DEFAULT_FROM_EMAIL,[email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except:
        return False
    
def sendresetpsdmail(email,argu):
    data={'subject':'SeMF账号密码重置',
          'text_content':'',
          'html_content':''}
    data['text_content'] = "您正在申请重置SeMF平台账号，请前往以下地址处理："+ url +"/view/resetpsd/"+argu +"  如无执行重置操作，请忽略该邮件"
    data['html_content'] = """
    <p>Dear user:</p>
    <p>    您正在申请重置SeMF的密码，请前往以下地址进行密码重置，<a href='"""+ url +"/view/resetpsd/"+argu +"""'>点我</a>以完成密码重置</p>
    <p>    如点击失效，请前往访问以下地址""" + url +"/view/resetpsd/"+argu + """</p>
    <p>    如非本人操作，忽略该邮件</p>
    <p>    本邮件为安全管控平台SeMf系统邮件，请勿回复</p>
    """
    res = sendmails(email,data)
    if res:
        return True
    else:
        return False