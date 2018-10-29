# _*_ coding:utf8 _*_

import threading
import urllib2
import math
import time
import json
from pyquery import PyQuery

class ConfigureHelper:
    """ 爬取不同网站的配置辅助类
            在爬取网站数据的时候可以根据每个网站的布局和CSS不同添加属于这个网站自己的爬取配置
            配置文件的格式如下：
                {
                    'configure_key':_configure_name_key,
                    'configure_content':
                                        {
                                            'book_url':_book_url,
                                            'pre_fix_url':_pre_fix_url,
                                            ......
                                         },
                    'configure_docs':_configure_name_docs
                }
    """    
    
    _configure_file = ''        # 整个配置文件
    _update_configure_url = ''  # 更新地址
    
    _configure_name_key = ''    # 配置文件中每一个网站对应的唯一key,一般为网站域名
    _configure_name_docs = ''   # 每一个网站对应的配置说明
    _configure_content = ''     # 每一个网站对应配置内容
    
    _pre_fix_url = ''           # 下载地址前缀,通常后面跟目录中过去的相对地址构成完整的访问地址
    _book_name_tag = ''         # 页面中小说【名称】的DOM元素标记,可以是id、class和html标记等
    _book_query_tag = ''        # 页面中小说【目录】的DOM元素标记,可以是id、class和html标记等
    _book_content_tag = ''      # 页面中小说【内容】的DOM元素标记,可以是id、class和html标记等

        
    
    def __init__(self):
        """ 初始化配置文件 kung_ke.json如果不存在配置文件则自动创建一个
                         配置文件一次性加载入内存方便程序运行时候调用.kung_ke.ini存放能够更新kung_ke.json的网址
        """
        try:
            f = open('kung_ke.ini','r')
            self.set_update_configure_url(f.readline())
            fp = open('kung_ke.json', 'r')
            self.set_configure_file(json.load(fp))
            if len(self.get_configure_file()) == 0:
                self.update_configure_file()
        except Exception, e:
            print e,' Loads json file failed!' 
        finally:            
            fp.close()
            f.close()
        pass

    def get_configure_content(self):
        return self.__configure_content


    def set_configure_content(self, value):
        self.__configure_content = value


    def get_configure_file(self):
        return self.__configure_file


    def set_configure_file(self, value):
        self.__configure_file = value


    def get_configure_name_key(self):
        return self.__configure_name_key


    def get_configure_name_docs(self):
        return self.__configure_name_docs


    def get_update_configure_url(self):
        return self.__update_configure_url


    def get_pre_fix_url(self):
        return self.__pre_fix_url


    def get_book_name_tag(self):
        return self.__book_name_tag


    def get_book_query_tag(self):
        return self.__book_query_tag


    def get_book_content_tag(self):
        return self.__book_content_tag


    def set_configure_name_key(self, value):
        self.__configure_name_key = value


    def set_configure_name_docs(self, value):
        self.__configure_name_docs = value


    def set_update_configure_url(self, value):
        self.__update_configure_url = value


    def set_pre_fix_url(self, value):
        self.__pre_fix_url = value


    def set_book_name_tag(self, value):
        self.__book_name_tag = value


    def set_book_query_tag(self, value):
        self.__book_query_tag = value


    def set_book_content_tag(self, value):
        self.__book_content_tag = value


    def _private_find_configure_key(self,_configure_name_key):
        """ 私有函数。用于找出某一个网站的爬取配置 """
        li = self.get_configure_file()
        for x in li:
            if x['configure_key'] == _configure_name_key:
                return x 
                pass
        return False
    
    def _private_route_configure_value(self):
        """ 私有函数。分发传入的配置 """
        self.set_book_name_tag(self.get_configure_content()['book_name_tag'])
        self.set_book_query_tag(self.get_configure_content()['book_query_tag'])
        self.set_book_content_tag(self.get_configure_content()['book_content_tag'])
        self.set_pre_fix_url(self.get_configure_content()['pre_fix_url'])
        return True
    

    def use_one_configure(self,configure_name):
        """ 使用一个网站的配置 ,如果没有整个网站的配置将打印出错信息"""
        get_one = self._private_find_configure_key(configure_name)
        if get_one <> False:
            self.set_configure_name_key(get_one['configure_key'])
            self.set_configure_name_docs(get_one['configure_docs'])
            self.set_configure_content(get_one['configure_content'])
            self._private_route_configure_value()            
            return True
        print 'There is no configure by ',configure_name
        return False
    
    
    def get_all_configure_name(self):
        """ 获取所有配置文件名称(网站名字) """
        all_configure_name = []
        li = self.get_configure_file()
        if len(li) <> 0:
            for x in li:
                all_configure_name.append(x['configure_key'])
        return all_configure_name
    
    
    def update_configure_file(self):
        """根据更新的地址更新配置文件内容"""
        
        req = urllib2.Request(self.get_update_configure_url())
        res = urllib2.urlopen(req)
        if res.code == 200:
            try:
                fp = open('kung_ke.json', 'w')
                json.dump(res.read(),fp)
                return True
            except Exception,e:
                print e
            finally:
                fp.close()
        return False




class kong1g:

    threadNo = 10
    theradList =[]
    booktext = {}
    url = ''
    prefix = ''
    _miss_total_num = 0
    
    def __init__(self):
        self.set_booktext({})
        self.set_therad_list([])
        self.set_thread_no(10)
        self.set_miss_total_num(0)
        pass

    def get_miss_total_num(self):
        return self.__miss_total_num


    def set_miss_total_num(self, value):
        self.__miss_total_num = value


    def get_therad_list(self):
        return self.__theradList


    def get_booktext(self):
        return self.__booktext


    def get_url(self):
        return self.__url


    def get_prefix(self):
        return self.__prefix


    def set_therad_list(self, value):
        self.__theradList = value


    def set_booktext(self, value):
        self.__booktext = value


    def set_url(self, value):
        self.__url = value


    def set_prefix(self, value):
        self.__prefix = value


    def get_thread_no(self):
        return self.__threadNo


    def set_thread_no(self, value):
        self.__threadNo = value

    
    
    
    """ 将内容保存为文本 """
    def saveBook21Text(self,filename, booktext):
            """  """
            try:
                fp = open(filename, 'a')
                for b in range(self.get_thread_no()):
                    l = booktext[b]
                    for j in l:                    
                        fp.write(j['title'].encode('utf8') + '\n')
                        fp.write(j['content'].encode('utf8'))
                        fp.write('\n')                                               
            except Exception, e:
                print e
            finally:
                fp.close()
            pass
    
    
    def chang_content(self,x,temp):                
        self.get_booktext()[x] = temp
        pass
    
    
    def act(self,i,startflag, endflag, leng,booklist,prefix,lock,content_tag):
        tempList = []    
        if endflag > leng:
            endflag = leng
        for x in range(startflag, endflag):
            try:
                artTitle = booklist[x].text()
                artUrl = prefix + booklist[x].attr('href')                
                flag = True
                while flag:
                    req = urllib2.Request(url=artUrl)
                    res = urllib2.urlopen(req)
                    if res.code == 200:
                        htmltext = res.read()
                        doc = PyQuery(htmltext)                
                        bookcontent = doc(content_tag).text()
                        t = {'title':artTitle,'content':bookcontent}    #爬下来的标题和文章形成一个字典（map）的数据结构存起
                        tempList.append(t)                              #把字典再作为一个列表的一员存到一个列表中
                        flag = False
                        print artTitle,'>>>>>>>.....ok!'
            except Exception, e:
                self.set_miss_total_num(self.get_miss_total_num()+1)
                print e,artTitle,artUrl
        lock.acquire()
        try:
            self.chang_content(i,tempList)
        finally:
            lock.release()
        pass
    
    
    def main(self,ar):
        ch = ConfigureHelper()
        ch.use_one_configure(ar)
        lock = threading.Lock()     #线程锁，主要用于最后把所有线程的内容整合在一个文本中
        print "Let's Go!"
        start = time.time()
        try:
            req = urllib2.Request(self.get_url())
            res = urllib2.urlopen(req)
            if res.code == 200:
                muhtml = res.read()
                doc = PyQuery(muhtml)
                bookName = doc(ch.get_book_name_tag()).text() + ".txt"
                bookQuery = doc(ch.get_book_query_tag()).items()
                booklist = list(bookQuery)         
                leng = float(len(booklist))
                eachThreadNo = math.ceil(leng / self.get_thread_no())  # 每一个线程跑多少页面，通过向上收数保证小数被涵盖        
                for i in range(self.get_thread_no()):
                    t = threading.Thread(target=self.act, args=(i,i * int(eachThreadNo), (i + 1) * int(eachThreadNo), int(leng),booklist,ch.get_pre_fix_url(),lock,ch.get_book_content_tag(),))
                    self.get_therad_list().append(t)
                    t.start()
                
                for t in self.get_therad_list():
                    t.join()
                    
        except Exception, e:
            print e
        self.saveBook21Text(bookName,self.get_booktext())
        end = time.time()
        print
        print bookName,' total ',len(booklist),' artices!'
        print 'Threads number is',self.get_thread_no()
        print 'Missed artices is',self.get_miss_total_num()
        print 'Runs %0.2f seconds.'%(end-start)
        print '=======over======='
        pass
    miss_total_num = property(get_miss_total_num, set_miss_total_num, None, None)
    
    
if __name__=='__main__':
    k = kong1g()
    k.set_thread_no(40)
    myurl = 'http://www.biquge.com.tw/16_16357/'
    tem = myurl.split('.')    
    k.set_url(myurl)
    try:    
        if len(tem) > 1:                  
            k.main(tem[1])
    except Exception, e:
        print e
    
    
    
    
    
    
    
        


    

