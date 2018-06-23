# SecurityManageFramwork-SeMF 
[![Travis](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Github License](https://img.shields.io/aur/license/yaourt.svg)](https://github.com/zhaoweiho/SecurityManageFramwork/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zhaoweiho/SecurityManageFramwork.svg)](https://github.com/zhaoweiho/SecurityManageFramwork/stargazers)


#### 项目介绍
**SEMF**是一款适用于企业内网`安全管理平台，包含资产管理，漏洞管理，账号管理，知识库管、安全扫描自动化功能模块，可用于企业内部的安全管理`。

**本平台旨在帮助安全人员少，业务线繁杂，周期巡检困难，自动化程度低的甲方，更好的实现企业内部的安全管理。本软件只用作企业内部IT资产管理，无攻击性行为。请使用者遵守《[中华人民共和国网络安全法](http://www.npc.gov.cn/npc/xinwen/2016-11/07/content_2001605.htm)》,勿将SEMF用于非授权测试，作者不负任何连带法律责任。**
> 喜欢请点 Star，如果不打算贡献，千万别 Fork


本项目原地址:https://gitee.com/gy071089/SecurityManageFramwork

作者:[残源](https://my.oschina.net/u/3867729)<br />


#### 软件架构
后端系统 python3 + django2 + rabbitmq 实现。<br />
前端显示 layui + bootstarp,使用开源模板 X-admin:http://x.xuebingsi.com/

#### 项目特点
-  可自定义用户类型及权限信息，初始化中生成安全人员，运维人员，网络人员和业务人员四种类型
-  企业IT资产类型和资产属性可在后台自定义，根据需要进行扩展
-  内网资产发现和端口扫描可自动化进行
-  完整的漏洞跟进和扫描器漏洞过滤
-  网络映射,针对大型企业内外网之间映射管理复杂，预留功能
-  知识库管理,针对安全信息共享,分为通告类和科普类
-  漏洞库管理,此模块对接cnvd漏洞库
-  基于插件的漏洞扫描功能,可自行添加
-  多种协议的弱口令检测
-  AWVS(Acunetix Web Vulnerability Scanner) 接口调用
-  Nessus(6/7) 接口调用

#### 安装教程

[安装手册](https://github.com/zhaoweiho/SecurityManageFramwork/tree/master/doc/install_zh.md)

#### 使用说明

1. 资产管理模块,以下为管理员界面功能，其他类型用户根据定义的权限生成菜单和界面
    <br>登录注册页</br>
    ![登录注册页](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113258_154ca8d5_1390378.png "屏幕截图.png")
    <br>系统首页</br>
    ![系统首页](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113454_07c46a58_1390378.png "屏幕截图.png")
    <br>资产管理</br>
    ![资产管理](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113543_6a6973ec_1390378.png "屏幕截图.png")
    <br>资产详情</br>
    ![资产详情](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/114021_ef591ca3_1390378.png "屏幕截图.png")
    <br>漏洞管理</br>
    ![漏洞管理](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113714_90826f30_1390378.png "屏幕截图.png")
    <br>报表中心</br>
    ![报表中心](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/114106_3cf15048_1390378.png "屏幕截图.png")
    
#### 参与贡献

1.  本项目当前仅自己维护，希望有志之士可协助完善系统，详情可加入qq群，联系群主即可
    ![qq交流群](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/114130_0e8d0451_1390378.png "屏幕截图.png")
2.  如有其他定制化需求，可发邮件至gy071089@outlook.com联系我

