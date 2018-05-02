#coding=utf-8
"""
日期：2018年04月15日
作者：管青企
邮箱：guanqingqi@foxmal.com
"""
from django.shortcuts import render,redirect,reverse
from django.core.paginator import Paginator
from .models import *
import markdown
from django.core.cache import cache
from django.views.decorators.cache import cache_page
# Create your views here.


#首页展示
def index(request):
    #获取教程分类用作导航展示
    categorys = Category.objects.all();
    #获取最新教程标签数据
    tags = Tag.objects.all();
    #封装数据
    context = {'tags':tags,'categorys':categorys,'cur_category':1}
    return render(request=request,template_name='blog/index.html',context=context)


#导航页面展示
def list(request,categoryid,pagenum):


    #重定向反向解析视图
    if int(categoryid) == 1:
        return redirect(reverse('blog:index'))
    # 获取教程分类用作导航展示
    categorys = Category.objects.all();
    # 获取最新教程标签数据
    tags = Tag.objects.filter(category_id=categoryid)
    #获取该导航分类下的文章列表
    articles = Article.objects.filter(category_id=categoryid)

    #分页
    p_articles = Paginator(articles,9)#列表也每页5个
    if pagenum == '':
        pagenum = 1
    num = int(pagenum)
    page_articles = p_articles.page(num)
    page_list = p_articles.page_range
    #封装数据
    context = {'tags': tags, 'categorys': categorys,'page_list':page_list,'cur_category':int(categoryid),'articles':page_articles}
    return render(request=request,template_name='blog/list.html',context=context)

#教程内容展示
def detail(request,categoryid,articleid):
    # 获取教程分类用作导航展示
    categorys = Category.objects.all()

    #获取该文章
    try:
        article = Article.objects.get(pk = articleid)
    except Exception as e:
        print(e)

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    #缓存主要解决的是转化markdown的时间太长了的时间问题
    cache_key = categoryid + '-' + articleid
    if cache:
        cache_article = cache.get(cache_key)
        if cache_article:
            #判断更新时间
            cache_date = cache_article.update_date.strftime("%Y%m%d%H%M%S")
            article_date = article.update_date.strftime("%Y%m%d%H%M%S")
            if article_date == article_date:
                article = cache_article
            else:
                article.body = md.convert(article.body)
                article.toc = md.toc
                cache.set(cache_key,article,60*60*12)# 默认秒为单位
        else:
            article.body = md.convert(article.body)
            article.toc = md.toc
            cache.set(cache_key, article, 60 * 60 * 12)
    else:
        article.body = md.convert(article.body)
        article.toc = md.toc
        cache.set(cache_key, article, 60 * 60 * 12)

    context = {'article':article,'categorys':categorys,'cur_category':int(categoryid)}
    return render(request=request,template_name='blog/detail.html',context=context)

#如果点击标签 只有一篇文章 那么直接展示这篇文章内容，如果是多篇文章 那么展示文章列表（不推荐 尽量保证一个标签一个文章，这是网站简洁的原则）
def tagsearch(request,tagid,pagenum):

    articles = Article.objects.filter(tags=tagid)

    if len(articles)==1:
        return redirect(reverse('blog:detail',args=(articles[0].category_id,articles[0].id)))
    else:
        # 分页
        p_articles = Paginator(articles, 9)  # 列表也每页12个
        if pagenum == '':
            pagenum = 1
        num = int(pagenum)
        page_articles = p_articles.page(num)
        page_list = p_articles.page_range
        # 封装数据
        context = {'page_list': page_list,'articles': page_articles,'tagid':tagid}
        return render(request,'blog/taglist.html',context=context)

# 重写搜索视图，可以增加一些额外的参数，且可以重新定义名称
    # def get_context_data(self, *args, **kwargs):
    #     context = super(MySearchView, self).get_context_data(*args, **kwargs)
    #     # do something
    #     return context
    #context_object_name = 'search_list'# 重新定义搜索结果名字
    # paginate_by = getattr(settings, 'BASE_PAGE_BY', 12)
    # paginate_orphans = getattr(settings, 'BASE_ORPHANS', 0)
    # queryset = SearchQuerySet().order_by('-views')  排序
