# -*- coding: utf-8 -*-

# Импортируем нужные нам библиотеки
import urllib, urllib2, re, sys, os
from BeautifulSoup import BeautifulSoup
from pprint import pprint
import xml.etree.cElementTree as et
import json
from pprint import pprint
 
# Функция для получения исходного кода web-страниц
def GetHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', 'Content-Type':'application/x-www-form-urlencoded'}
    conn = urllib2.urlopen(urllib2.Request(url, urllib.urlencode({}), headers))
    html = conn.read()
    conn.close()
    
    return html 


siteurl = 'http://www.kino-dom.tv'
# Тест на работоспособность
html = GetHTML(siteurl)
doc = BeautifulSoup(html.decode('windows-1251'))
page = doc.findAll('a', attrs = {'class':'mainmenu','title':lambda t: len(t) > 0 ,'href': lambda url: url.startswith('/')})
 


#pprint( [tag['title']  for  tag in page ] )
for  tag in page:
    print tag['title'], tag['href']

html = GetHTML("%s%s" % (siteurl,page[2]['href']))
genre_links = re.compile('<h1> <a href="(.+?)">(.+?)</a>   </h1>').findall(html.decode('windows-1251'))

for url, title in genre_links:
    print "----------> %s : %s" % (title, url)
    html = GetHTML(url)
    doc = BeautifulSoup(html.decode('windows-1251'))
    embeded = doc.findAll('embed', attrs = {'flashvars': lambda vars: len(vars) > 0})
    print embeded
    
    
    playlist =  re.compile('pl=(.+?)json').findall(embeded[0]['flashvars']).pop()
    playlist_json =  GetHTML("%sjson" % playlist)
    #pprint(json.loads( playlist_json))
    playlist_dict = json.loads( playlist_json)
    for i in playlist_dict['playlist']:
        print i['comment']
        for j in i['playlist']:
            print "------->%s" % j['comment']
            print "------->%s" % j['file']
        
    
    break
    playlist_xml =  GetHTML(playlist)
    #foo = et.XML(playlist_xml)
    trackxml = re.compile('track>(.+?)</track').findall(unicode(playlist_xml, "cp1251"))
    print trackxml
    break
    for track in trackxml:
        movie_links = re.compile('title>(.+?)</title(.+?)location>(.+?)</location').findall(track)
        for a,b,c in movie_links:
                print unicode(a, "cp1251"),c
"""
    for i in trackxml:
         print re.compile('title>(.+?)</title').findall(i).pop()
         print re.compile('location>(.+?)</location').findall(i).pop()
    
"""        
        
        
    

"""
for  tag in page:
    print tag['title'], tag['href']
    html = GetHTML("%s%s" % (siteurl,tag['href']))
    genre_links = re.compile('<h1> <a href="(.+?)">(.+?)</a>   </h1>').findall(html.decode('windows-1251'))
    for url, title in genre_links:
        print "----------> %s" % title


links = soup.findAll('a', attrs = {'class':'mainmenu', 'title':lambda t: len(t) > 0})

genre_links = re.compile('<a href="(.+?)" title="" class="mainmenu">(.+?)</a><br />').findall(html.decode('windows-1251'))

# Сопоставляем результаты первого и второго (.+?) с переменными url и title (будут присвоены в порядке указания)
for url, title in genre_links:
    print title + ' [' + url + ']'
    
    
    <embed 
        pluginspage="http://www.adobe.com/go/getflashplayer" 
        src="http://kino-dom.tv/uppod.swf" 
        width="558" height="435" wmode="opaque" 
        allowscriptaccess="always" 
        allowfullscreen="true" bgcolor="#000000" 
        flashvars="&amp;st=http://kino-dom.tv/templates/kinodom/swf/video30-365.txt&amp;pl=http://kino-dom.tv/4c260f6fcd0dc1fcf8a2febb4cb5b04f/play/navidu.xml.json&amp;embedcode=&lt;iframe%20src%3D%22http%3A%2F%2Femb.kino-dom.tv%2Fembed.php%3Fpl%3Dhttp%3A%2F%2Fkino-dom.tv%2F4c260f6fcd0dc1fcf8a2febb4cb5b04f/play/navidu.xml.json%22%20width%3D%22700%22%20height%3D%22600%22%20frameborder%3D%220%22%20scrolling%3D%22no%22&gt;&lt;/iframe&gt;">
    
    
  re.compile('p(.+?)p').findall(str)  
str='<embed src="http://kino-dom.tv/mediaplayer5.swf" width="558" height="638" allowfullscreen="true" flashvars="&amp;displayheight=458&amp;file=http://kino-dom.tv/4c260f6fcd0dc1fcf8a2febb4cb5b04f/play/smertvraju.xml&amp;playlist=bottom"></embed>'
re.compile('file=(.+?)&amp').findall(str)
"""
