#coding=utf-8
"""
日期：2018年04月15日
作者：管青企
邮箱：guanqingqi@foxmal.com
"""
from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):
    actions_on_top = True
    list_per_page = 10
    list_display = ['name']
    search_fields = ['name']

class KeywordInline(admin.TabularInline):
    model = Keyword


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    actions_on_top = True
    list_per_page = 10
    search_fields = ['name']
    list_display = ['name','slug']

class CategoryInline(admin.TabularInline):
    model = Category

@admin.register(Tag)
class Tag(admin.ModelAdmin):
    actions_on_top = True
    list_per_page = 10
    search_fields = ['name']
    list_display = ['name','slug','create_date','category']

class TagInline(admin.TabularInline):
    model = Tag

@admin.register(Article)
class Article(admin.ModelAdmin):
    actions_on_top = True
    list_per_page = 10
    search_fields = ['title']
    list_display = ['title','author','summary','create_date','views','slug']
    #inlines = [TagInline,KeywordInline,CategoryInline]



