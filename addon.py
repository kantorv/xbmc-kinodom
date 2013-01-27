# -*- coding: utf-8 -*-

import urllib, urllib2, re, sys
import xbmcplugin, xbmcgui
from BeautifulSoup import BeautifulSoup
import json

def getHTML(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3', 'Content-Type':'application/x-www-form-urlencoded'}
    conn = urllib2.urlopen(urllib2.Request(url, urllib.urlencode({}), headers))
    
    html = conn.read()
    conn.close()
    
    return html



def Categories():
    url = 'http://www.kino-dom.tv'
    html = getHTML(url)
    doc = BeautifulSoup(html.decode('windows-1251').encode('utf-8'))
    page = doc.findAll('a', attrs = {'class':'mainmenu','title':lambda t: len(t) > 0 ,'href': lambda url: url.startswith('/')})
    #genre_links = re.compile('<a href="(.+?)" title="" class="mainmenu">(.+?)</a><br />').findall(html.decode('windows-1251').encode('utf-8'))
    for  tag in page:    
        addDir(tag['title'].encode('utf-8'), "%s%s" % (url  ,  tag['href']), 20)


    
    

def MoviesLinks(url):
    html = getHTML(url)
    movie_links = re.compile('<h1> <a href="(.+?)">(.+?)</a>   </h1>').findall(html.decode('windows-1251').encode('utf-8'))
    for link, title in movie_links:
        addDir(title[:-12], link, 30)
    categorystring = re.compile('http://www.kino-dom.tv/(.+?)/').findall(url).pop()
    #print categorystring
    doc = BeautifulSoup(html.decode('windows-1251').encode('utf-8'))
    nav_section = doc.findAll('div', attrs = {'class':'navigation'}).pop()
    pages = nav_section.findAll('a', attrs = {})
    for link in pages:
        if link.string.isdigit():
            #print link.string.encode('utf-8')
            pagetitle = 'Page %s' % link.string
            pageurl = "http://www.kino-dom.tv/%s/page/%s" % (categorystring , link.string)
            print pageurl
            addDir(pagetitle,pageurl , 20)
    


def Seasons(url):
    html = getHTML(url)
    doc = BeautifulSoup(html.decode('windows-1251'))
    embeded = doc.findAll('embed', attrs = {'flashvars': lambda vars: len(vars) > 0})
    #print embeded
    #playlist =  re.compile('file=(.+?)&playlist').findall(embeded.pop()['flashvars']).pop()
    #playlist_xml =  getHTML(playlist)
    
    playlist =  re.compile('pl=(.+?)json').findall(embeded[0]['flashvars']).pop()
    playlist_json =  getHTML("%sjson" % playlist)
    playlist_dict = json.loads( playlist_json)
    for i in playlist_dict['playlist']:
        #print i['comment']
        #addDir(i['comment'].encode("utf-8"),"%sjson" % playlist, 40)
        #continue
        addLink(i['comment'].encode("utf-8"), '')
        for j in i['playlist']:
            addLink("------->%s" % j['comment'].encode("utf-8"), j['file'])




def Videos(title,url):
	addLink(title, url)

	    


def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                            
    return param


def addLink(title, url):
    item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )
    #print url
    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)


def addDir(title, url, mode):
    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))

    item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    item.setInfo( type='Video', infoLabels={'Title': title} )

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)


params = get_params()
url    = None
title  = None
mode   = None

try:    title = urllib.unquote_plus(params['title'])
except: pass

try:    url = urllib.unquote_plus(params['url'])
except: pass

try:    mode = int(params['mode'])
except: pass

if mode == None:
    Categories()

elif mode == 20:
    MoviesLinks(url)

elif mode == 30:
    #Series(url)
    Seasons(url)

elif mode == 40:
    Videos( title, url)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))
