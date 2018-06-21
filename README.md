# SecurityManageFramwork-SeMF

#### 项目介绍
企业内网安全管理平台，包含资产管理，漏洞管理，账号管理，知识库管、安全扫描自动化功能模块，可用于企业内部的安全管理。
本平台旨在帮助安全人员少，业务线繁杂，周期巡检困难，自动化程度低的甲方，更好的实现企业内部的安全管理。

本项目原地址:https://gitee.com/gy071089/SecurityManageFramwork<br />
作者:[残源](https://my.oschina.net/u/3867729)<br />


#### 软件架构
后端系统 python3 + django2 + rabbitmq 实现。
前端显示 layui + bootstarp,使用开源模板 X-admin:http://x.xuebingsi.com/

#### 项目特点
1.  可自定义用户类型及权限信息，初始化中生成安全人员，运维人员，网络人员和业务人员四种类型
2.  资产类型和资产属性可在后台自定义，根据需要进行扩展
3.  内网资产发现和端口扫描可自动化进行
4.  完整的漏洞跟进和扫描器漏洞过滤



#### 安装教程

1. 准备centos7系统，安装python3，mysql（选用），rabbitmq，nmap，安装方法可参照项目根目录中的文档《SeMF安装指南》
    
2. 下载解压本项目，并切换到项目路径，修改项目setting.py文件，根据需要设置 发件邮箱、rabbitmq参数以及数据库信息
    ```
    WEB_URL = 'http://localhost:8000'   //这里用来修改网站域名，可根据部署需要修改
    EMAIL_HOST/EMAIL_PORT...等邮件相关设置
    BROKER_URL    //用来设置队列信息和地址
    DATABASES    //可根据需要选择sqlite和mysql或其他数据库，设置文件中给出mysql设置方法，注意数据库的字符编码
    ```
3. 切换到项目根目录执行,分别执行以下命令
    ```
    pip install  -r requirements.txt         //安装python库
    python manage.py makemigrations        //数据表生成
    python manage.py migrate
    python manage.py createsuperuser    //创建超级管理员
    python initdata.py        //初始化数据库，主要生成角色，权限等信息
    python cnvd_xml.py        //用于同步cnvd漏洞数据文件，文件位于cnvd_xml目录下，可自行调整，该文件夹每周更新一次，
    celery -A SeMF worker -l info    //用于开启消费者，执行异步任务
    python manage.py runserver 0.0.0.0:8000    //运行成功，访问即可
    
    如需使用周期巡检和漏洞同步功能，需前往
    http://localhost:8000/semf/        页面设置扫描器API参数，当前支持nessus，后续会根据反馈添加其他扫描器
    ```

#### 使用说明

1. 资产管理模块,以下为管理员界面功能，其他类型用户根据定义的权限生成菜单和界面
    <br>登录注册页</br>
    ![登录注册页](https://gitee.com/uploads/images/2018/0527/113258_154ca8d5_1390378.png "屏幕截图.png")
    <br>系统首页</br>
    ![系统首页](https://gitee.com/uploads/images/2018/0527/113454_07c46a58_1390378.png "屏幕截图.png")
    <br>资产管理</br>
    ![资产管理](https://gitee.com/uploads/images/2018/0527/113543_6a6973ec_1390378.png "屏幕截图.png")
    <br>漏洞管理</br>
    ![漏洞管理](https://gitee.com/uploads/images/2018/0527/113714_90826f30_1390378.png "屏幕截图.png")
    <br>资产详情 ，这里的资产详情可在后台自定义，不同类型资产显示的不一样，就不一一截图了</br>
    ![资产详情](https://gitee.com/uploads/images/2018/0527/114021_ef591ca3_1390378.png "屏幕截图.png")
    <br>报表中心，当前仅显示几类，后续会继续添加</br>
    ![报表中心](https://gitee.com/uploads/images/2018/0527/114106_3cf15048_1390378.png "屏幕截图.png")
    
#### 参与贡献

1.  本项目当前仅自己维护，希望有志之士可协助完善系统，详情可加入qq群，联系群主即可
    ![qq交流群](https://gitee.com/uploads/images/2018/0527/114130_0e8d0451_1390378.png "屏幕截图.png")
2.  如有其他定制化需求，可发邮件至gy071089@outlook.com联系我

