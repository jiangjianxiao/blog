#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'jjx'
SITENAME = u'EasyNew'
SITEURL = 'http://www.easynew.com.cn'
# GITHUB_URL = "https://github.com/jiangjianxiao/"
TIMEZONE = 'Asia/Shanghai'
DISPLAY_PAGES_ON_MENU = False
DISPLAY_CATEGORIES_ON_MENU = False
MENUITEMS = (('未分类', '/category/misc.html'), ('关于我们', '/about-us.html') )
# Blogroll
DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = "feeds/all.atom.xml"
CATEGORY_FEED_ATOM = "feeds/%s.atom.xml"
TRANSLATION_FEED_ATOM = None

OUTPUT_PATH = '../jiangjianxao.github.com'

DISQUS_SITENAME = u"easynew"

LINKS = (('Pelican', 'http://getpelican.com/'),
        ('Python.org', 'http://python.org/'),
        ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
# SOCIAL = (('You can add links in your config file', '#'),
          # ('Another social link', '#'),)

DEFAULT_PAGINATION = 6
# THEME = 'notmyidea'

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True
PLUGIN_PATHS= ["pelican-plugins"]

PLUGINS = ["sitemap"]

# 配置sitemap 插件
SITEMAP = {
    "format": "xml",
    "priorities": {
        "articles": 0.7,
        "indexes": 0.5,
        "pages": 0.3,
    },
    "changefreqs": {
        "articles": "monthly",
        "indexes": "daily",
        "pages": "monthly",
    }
}
