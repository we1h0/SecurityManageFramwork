# SecurityManageFramwork-SeMF 
[![Travis](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Github License](https://img.shields.io/aur/license/yaourt.svg)](https://github.com/zhaoweiho/SecurityManageFramwork/blob/master/LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/zhaoweiho/SecurityManageFramwork.svg)](https://github.com/zhaoweiho/SecurityManageFramwork/stargazers)

### README English | [中文](README_CN.md)

#### Introduction
** SEMF** is a `security management platform'for enterprise intranet, which includes functions of asset management, vulnerability management, account management, knowledge base management and security scanning automation. It can be used for internal security management.

** This platform aims to help Party A with fewer security personnel, complicated business lines, difficult periodic inspection and low automation to better achieve internal safety management. This software is only used for internal IT asset management, no aggressive behavior. Users are requested to abide by the Network Security Law of the People's Republic of China (http://www.npc.gov.cn/npc/xinwen/2016-11/07/content_2001605.htm). They are not required to use SEMF for unauthorized testing. The authors are not liable for any joint and several legal responsibilities. **

> If you like it, please click Star. If you don't intend to contribute, don't Fork. The later version of Fork will not automatically update the latest version synchronously. You won't enjoy the pleasure and surprise of the latest version.


The original address of this project:
https://gitee.com/gy071089/SecurityManageFramwork

Author:[残源](https://my.oschina.net/u/3867729)<br />


#### Architecture

posterior : python3 + django2 + rabbitmq <br />

Front-end : layui + bootstarp,

Using Open Source Templates X-admin:http://x.xuebingsi.com/

#### Characteristic

- User type and privilege information can be customized, and four types of security personnel, operation and maintenance personnel, network personnel and business personnel can be generated in initialization.

- Enterprise IT asset types and asset attributes can be customized in the background and extended as needed.

- Intranet asset discovery and port scanning can be automated

- Complete vulnerability tracking and scanner vulnerability filtering

- Network mapping, for large enterprise intranet and extranet mapping management is complex, reservation function

- Knowledge base management, for security information sharing, is divided into announcement category and popular science category.

- Vulnerability library management, this module docks with cnvd vulnerability Library

- Plug-in-based vulnerability scanning function can be added by itself

- Weak Password Detection for Multiple Protocols

- AWVS (Acunetix Web Vulnerability Scanner) Interface Call

- Nessus (6/7) interface call
#### Installation

[Installation Guide](https://github.com/zhaoweiho/SecurityManageFramwork/blob/master/doc/SeMF%E5%AE%89%E8%A3%85%E6%8C%87%E5%8D%97-2018-06-12.pdf)

[User Guide](https://github.com/zhaoweiho/SecurityManageFramwork/blob/master/doc/SeMF%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97-2018-06-20.pdf)

#### Screenshot

-    Login Registration Page
    ![Login Registration Page](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113258_154ca8d5_1390378.png "屏幕截图.png")
-    System Home Page
    ![System Home Page](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113454_07c46a58_1390378.png "屏幕截图.png")
-    Asset management
    ![Asset management](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113543_6a6973ec_1390378.png "屏幕截图.png")
-    Details of assets
    ![Details of assets](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/114021_ef591ca3_1390378.png "屏幕截图.png")
-    Vulnerability management
    ![Vulnerability management](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/113714_90826f30_1390378.png "屏幕截图.png")
-    Report Center
    ![Report Center](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/114106_3cf15048_1390378.png "屏幕截图.png")
    
#### Contribution

1.  This project is currently only self-maintenance, hope that people with lofty ideals can help improve the system, details can be added to the QQ group, contact the group owner can be.
    ![qq交流群](https://raw.githubusercontent.com/zhaoweiho/SecurityManageFramwork/master/doc/image/114130_0e8d0451_1390378.png "屏幕截图.png")
2.  If you have other customization requirements, you can contact me by email at gy071089@outlook.com.
