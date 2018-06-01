#coding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

ARTICLE_STATUS=(
                ('0','新建'),
                ('1','发布'),
                ('2','撤回'),
                ('3','审核'),
                )



class ArticleType(models.Model):
    article_type_name =  models.CharField('文章分类',max_length = 30)
    article_type_body = models.TextField('分类简介')
    parent = models.ForeignKey('self',verbose_name=u'父菜单',related_name='articletype_type',null=True,blank=True,on_delete=models.CASCADE)
    
    def __str__(self):
        #显示层级菜单
        title_list = [self.article_type_name]
        p = self.parent
        while p:
            title_list.insert(0,p.article_type_name)
            p = p.parent
        return '-'.join(title_list)
    

class Article(models.Model):
    article_id = models.CharField('文章ID',max_length = 30)
    article_name = models.CharField('文章标题',max_length = 50,unique=True)
    article_order = models.IntegerField('文章推广',default=0)
    file = models.FileField('附件',upload_to ='article/',null=True,blank=True)
    article_body = models.TextField('文章内容')
    article_status = models.TextField('文章状态',choices=ARTICLE_STATUS,default='0')
    article_starttime = models.DateTimeField('添加时间',auto_now_add=True)
    article_updatetime = models.DateTimeField('更新时间',auto_now=True)
    
    article_type = models.ForeignKey(ArticleType,related_name='articletype_for_article',on_delete=models.CASCADE,null=True,verbose_name='文章分类',limit_choices_to={'parent__isnull':False})
    article_user = models.ForeignKey(User,related_name='article_for_user',on_delete=models.CASCADE,null=True)
    
    def __str__(self):
        return self.article_id
    
class ArticleComments(models.Model):
    article_comment_id = models.CharField('评论ID',max_length = 30)
    article_comment_body = models.TextField('评论内容')
    article_comment_status = models.TextField('评论状态',choices=ARTICLE_STATUS)
    article_comment_starttime = models.DateTimeField('添加时间',auto_now_add=True)
    
    article_comment_article =  models.ForeignKey(User,related_name='articlecomment_for_article',on_delete=models.CASCADE,verbose_name='文章关联')
    article_comment_user = models.ForeignKey(User,related_name='articlecomment_for_user',on_delete=models.CASCADE)
    
    def __str__(self):
        return self.article_comment_id
    