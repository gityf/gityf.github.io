# -*- coding:utf-8 -*-  
'''
Created on 2016-1-25

@author: wangyaofu
'''

from  HTMLParser import HTMLParser
import urllib2
import re
from macpath import split
import sys  
reload(sys)  
sys.setdefaultencoding('utf8') 

def header():
    headerHtml = '''<!DOCTYPE HTML PUBLIC -//W3C//DTD HTML 4.01 Transitional//EN "http://www.w3.org/TR/html4/loose.dtd">
        <html><head><title>Main page for gityf.</title>
        <meta http-equiv="content-type" content="text/html; charset=utf-8">
        <style type=text/css><!--
        body {
         font-family: arial, helvetica, sans-serif;
         font-size: 12px;
         font-weight: normal;
         color: black;
         background: white;
        }
        th,td {
         font-size: 10px;
        }
        h1 {
         font-size: x-large;
         margin-bottom: 0.5em;
        }
        h2 {
         font-family: helvetica, arial;
         font-size: x-large;
         font-weight: bold;
         font-style: italic;
         color: #6020a0;
         margin-top: 0em;
         margin-bottom: 0em;
        }
        h3 {
         font-family: helvetica, arial;
         font-size: 16px;
         font-weight: bold;
         color: #b00040;
         background: #e8e8d0;
         margin-top: 0em;
         margin-bottom: 0em;
        }
        li {
         margin-top: 0.25em;
         margin-right: 2em;
        }
        .hr {margin-top: 0.25em;
         border-color: black;
         border-bottom-style: solid;
        }
        .in    {color: #6020a0; font-weight: bold; text-align: left;}
        .frontend {background: #e8e8d0;}
        .s   {background: #e0e0e0;}
        .a0  {background: #FF99CC; font-weight: bold;}
        .a1  {background: #CCFF99;}
        .a2  {background: #CCFFFF;}
        .a3  {background: #CCCCFF;}
        .a4  {background: #66CCCC;}
        .a5  {background: #CCFF66;}
        .a6  {background: #FFCC99;}
        .maintain {background: #c07820;}
        .rls      {letter-spacing: 0.2em; margin-right: 1px;}

        a.px:link {color: #ffff40; text-decoration: none;}
        a.px:visited {color: #ffff40; text-decoration: none;}
        a.px:hover {color: #ffffff; text-decoration: none;}
        a.lfsb:link {color: #000000; text-decoration: none;}
        a.lfsb:visited {color: #000000; text-decoration: none;}
        a.lfsb:hover {color: #505050; text-decoration: none;}

        table.tbl { border-collapse: collapse; border-style: none;}
        table.tbl td { text-align: right; border-width: 1px 1px 1px 1px; border-style: solid solid solid solid; padding: 2px 3px; border-color: gray; white-space: nowrap;}
        table.tbl td.ac { text-align: center;}
        table.tbl th { border-width: 1px; border-style: solid solid solid solid; border-color: gray;}
        table.tbl th.pxname { background: #b00040; color: #ffff40; font-weight: bold; border-style: solid solid none solid; padding: 2px 3px; white-space: nowrap;}
        table.tbl th.empty { border-style: none; empty-cells: hide; background: white;}
        table.tbl th.desc { background: white; border-style: solid solid none solid; text-align: left; padding: 2px 3px;}

        table.lgd { border-collapse: collapse; border-width: 1px; border-style: none none none solid; border-color: black;}
        table.lgd td { border-width: 1px; border-style: solid solid solid solid; border-color: gray; padding: 2px;}
        table.lgd td.noborder { border-style: none; padding: 2px; white-space: nowrap;}
        u {text-decoration:none; border-bottom: 1px dotted black;}
        -->
        </style></head><body><h1>Git of Mr.WYF</h1><hr><h3>&gt; General git project information.</h3>
        <table border=0>'''
    return headerHtml

def footer():
    footHtml = '''</table></body></html>'''
    return footHtml

def indexMainRow():
    rowHtml = '''<tr class=a0><td>ID</td><td>Project</td><td>Basic doc description.</td></tr>'''
    return rowHtml

def indexRow():
    rowHtml = '''<tr class=a%d><td>%d</td><td><a href="http://github.com/%s">%s</a></td><td>%s</td></tr>'''
    return rowHtml

def tdClassId(pageId):
    pageId += 1
    if pageId >= 7:
        pageId = 1
    return pageId

class myparser(HTMLParser):

    # 继承父类初始化方法，并添加一个tag属性
    def __init__(self):
        HTMLParser.__init__(self)
        self.tag = None
        self.tagClass = None
        self.projects = {}
        self.thisProject = ""

    def handle_starttag(self,tag,attrs):
        #print u"开始标签；",tag

        # 判断是否是a开头的标签
        if tag=='a' and len(attrs):
            #设置 self.tag 标记
            self.tag='a'
            for href,link in attrs:
                if href=='href' and link.startswith("/gityf/"):
                    if len(link.split("/")) == 3:
                        #print href+":"+link
                        self.thisProject = link
        if tag=='p' and len(attrs):
            #设置 self.tag 标记
            self.tag='p'
            for href,link in attrs:
                if href=='class' and link.startswith("repo-list-description"):
                    self.tagClass = "repo"
                    #print href+":"+link

    def handle_data(self,data):
        #处理 a 标签开头的数据
        ddd = data.decode("utf-8")
        if self.tag=='p' and self.tagClass == "repo":
            #print u"数据内容：",ddd
            self.tag = None
            self.tagClass = None
            self.projects[self.thisProject] = ddd
    def getProject(self):
        return self.projects
def down(url):
    return urllib2.urlopen(url)
def parserGitProject(): 
    fn = open("index.html", "w")
    fn.write(header())
    fn.write(indexMainRow())
    for i in range(1,4):
        giturl = "https://github.com/gityf?page=%d"%(i)
        print giturl
        buf = down(giturl).read()
        m = myparser()
        m.feed(buf)
        ii = 1
        index = 1
        for proj, desc in m.getProject().items():
            fn.write(indexRow() % (ii, index, proj, proj, desc))
            ii = tdClassId(ii)
            index += 1
    fn.write(footer())
    fn.close()           

if __name__ == '__main__':
    parserGitProject()