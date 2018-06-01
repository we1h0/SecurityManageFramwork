#coding:utf-8
'''
Created on 2018年5月23日

@author: yuguanc
'''


from django import template
from django.utils.safestring import mark_safe
from SeMF import settings

register = template.Library()


def get_structure_data(request):
    """处理菜单结构"""
    menu = request.session[settings.SESSION_MENU_KEY]
    all_menu = menu[settings.ALL_MENU_KEY]
    permission_url = menu[settings.PERMISSION_MENU_KEY]
    
    all_menu_dict = {}
    for item in all_menu:
        item['children'] = []
        all_menu_dict[item['id']] = item
  
    for url in permission_url:
        # 添加显示状态
        # 将url添加到菜单下
        all_menu_dict[url['menu_id']]['url'] = url['url']
        all_menu_dict[url['menu_id']]['status'] = True
        
        # 显示菜单：url 的菜单及上层菜单 status: true
        pid = url['menu_id']
        while pid:
            all_menu_dict[pid]['status'] = True
            pid = all_menu_dict[pid]['parent_id']
    
    # 整理菜单层级结构：没有parent_id 的为根菜单， 并将有parent_id 的菜单项加入其父项的chidren内
    menu_data = []
    for i in all_menu_dict:
        if 'status' in all_menu_dict[i].keys():
            if all_menu_dict[i]['parent_id']:
                pid = all_menu_dict[i]['parent_id']
                parent_menu = all_menu_dict[pid]
                parent_menu['children'].append(all_menu_dict[i])
            else:
                menu_data.append(all_menu_dict[i])
    return menu_data


def get_menu_html(menu_data):
    option_str_start = """
    <li>
        <a href="javascript:;">
            <i class="layui-icon">{icon}</i>
            <cite>{title}</cite>
            <i class="iconfont nav_right">&#xe697;</i>
        </a>
    """
    option_str_end = """
    </li>
    """
    
    url_str_start = """
    <ul class="sub-menu">
    """
    url_str_end = """
    </ul>
    """
    
    url_str = """
    <li>
        <a _href="{url}">
            <i class="layui-icon">{icon}</i>
            <cite>{title}</cite>
        </a>
    </li>
    """
    
    
    menu_html = ''
    for item in menu_data:
        if not item['status']:
            continue
        else:
            menu_html += option_str_start.format(icon=item['icon'],
                                                title = item['title'],
                                                 )
            if item['children']:
                menu_html += url_str_start
                for item_c in item['children']:
                    if item_c['status']:
                        menu_html += url_str.format(url = item_c['url'],
                                                    icon = item_c['icon'],
                                                    title = item_c['title'],
                                                    )
                    else:
                        continue
                menu_html += url_str_end
            else:
                pass
            menu_html += option_str_end
                
    return menu_html


@register.simple_tag
def rbac_menu(request):
    """
    显示多级菜单：
    请求过来 -- 拿到session中的菜单，权限数据 -- 处理数据 -- 作显示
    数据处理部分抽象出来由单独的函数处理；渲染部分也抽象出来由单独函数处理
    """
    menu_data = get_structure_data(request)
    menu_html = get_menu_html(menu_data)

    return mark_safe(menu_html)
    # 因为标签无法使用safe过滤器，这里用mark_safe函数来实现