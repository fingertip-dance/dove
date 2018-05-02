#coding=utf-8
"""
日期：2018年04月15日
作者：管青企
邮箱：guanqingqi@foxmal.com
"""
from django.db import models

import markdown #markdown转化

#关键词
class Keyword(models.Model):
    name = models.CharField(verbose_name='关键词',max_length=20)

    class Meta:
        verbose_name = '关键词'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

#文章分类：也就是导航栏
class Category(models.Model):
    name = models.CharField(verbose_name='分类',max_length=20)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name

# 标签，设计上可以做到一篇文章多个标签
class Tag(models.Model):
    name = models.CharField(verbose_name='标签', max_length=20)
    slug = models.SlugField(unique=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name='标签所属分类')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.name

#文章
class Article(models.Model):
    title = models.CharField(verbose_name='标题',max_length=50)
    body = models.TextField(verbose_name='内容')
    author = models.CharField(verbose_name='作者',max_length=20)
    summary = models.TextField(verbose_name='文章摘要', max_length=230, default='description内容')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    views = models.IntegerField(verbose_name='阅览量', default=0)
    slug = models.SlugField(unique=True)

    #外键
    category = models.ForeignKey(Category, verbose_name='文章分类')#一对多 分类对应多个文章
    tags = models.ManyToManyField(Tag, verbose_name='标签')# 多对多 一个标签对应多个文章 一个文章对应多个标签
    keywords = models.ManyToManyField(Keyword, verbose_name='文章关键词',help_text='文章关键词')#多对对 一个文章对应多个关键词

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-create_date']

    def __str__(self):
        return self.title[:20]

    def body_to_markdown(self):
        return markdown.markdown(self.body, extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

    def update_views(self):
        self.views += 1
        self.save(update_fields=['views'])

