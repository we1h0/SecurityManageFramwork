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