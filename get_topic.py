#根据部落名获取前30页话题，原理和前面几乎相同，不多解释
import pymongo,requests,random,json,time,settings,multiprocessing

client = pymongo.MongoClient('localhost')
db = client['QQbuluo']

class Topic():

    def get_topic(self,bid,t_page=1,retries=0):
        headers = {
                    'accept-encoding': 'gzip, deflate, sdch',
                    'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                    'referer': 'https://buluo.qq.com/p/category.html?bid={}'.format(bid),
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                    'Cookie': settings.cookies
                    }

        url = 'https://buluo.qq.com/cgi-bin/bar/post/get_post_by_page?bid={}&num=20&start={}&source=2&r={}&bkn=1060100960'.format(bid, 20*(t_page-1),random.random())
        #防止网络问题，设置一个重试次数及判断
        if retries < 3:
            try:
                webdata = requests.get(url, headers=headers).text
                # print(webdata)
                response = json.loads(webdata)
                print('*' * 60, "bid=",bid,'第 %s 页' % t_page, '*' * 60, '\n')
                try:
                    #result是整个页面的话题，在这进行循环取出每个话题，有些页面没有话题所以做一个try...except判断
                    for result in response.get('result').get('posts'):
                        #打印部分信息出来
                        print(10*"-",'title:',result.get("title"),10*"-",'pid:',result.get("pid"),10*"-")
                        self.save_to_mongo(result)
                    if t_page<30:
                        #迭代获取30页
                        return self.get_topic(bid,t_page+1)
                    else:
                        print("已经存了30 页啦，换下一个部落吧")
                except:
                    #有些部落没有三十页话题（例如腾讯推广的一些新部落）
                    if response.get('isend') == 1:
                        print('第%s页是最后一页了,换下一个部落……'%t_page)
                        pass
                    else:
                        print('数据有问题',response)
            except:
                time.sleep(10)
                self.get_topic(bid,t_page,retries=retries+1)
                print('访问失败,进行第%s次重试'%retries)
        else:
            print('不能访问了')
            pass

    def save_to_mongo(self, result):
        try:
            db['bar_topic'].insert(result)
        except:
            print('存储mongodb失败','\n',result)
            pass

if __name__ == '__main__':
    topics = Topic()
    #barlist是从mongodb中取出的数据，用列表生产式返回的list。no_cursor_timeout=True是防止操作时间过长，pymongo的cursor会断开
    bar_list = [bar.get('bid') for bar in db.barlist.find({}, {"bid": 1, '_id': 0}, no_cursor_timeout=True)]
    #通过get_barlist的效率测试，根据个人机器情况，这里用4进程抓取
    pool = multiprocessing.Pool(4)
    pool.map(topics.get_topic,bar_list)
