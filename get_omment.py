#大部分原理和前几个爬虫一样，不过多解释
import json, pymongo, random, requests ,settings, multiprocessing

client = pymongo.MongoClient('localhost')
db = client['QQbuluo']


class Comment():
    def __init__(self):
        self.base_url = 'https://buluo.qq.com/cgi-bin/bar/post/get_comment_by_page_v2?'

    def get_comment_usr(self,bid_pid,page=1):
        headers = {
                    'accept-encoding':'gzip, deflate, sdch',
                    'accept-language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                    'referer':'https://buluo.qq.com/p/detail.html?bid={}&pid={}'.format(int(bid_pid['bid']),bid_pid['pid']),
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
                    'x-requested-with':'XMLHttpRequest',
                    'Cookie':settings.cookies}
        comment_url = self.base_url+'bid={0}&pid={1}&num=20&cur_lon=0&cur_lat=0&start={2}&barlevel=1&r={3}&bkn={4}'.format(int(bid_pid['bid']),bid_pid['pid'],(page-1)* 20,random.random(),settings.bkn)
        try:
            webdata = requests.get(comment_url, headers=headers).text
            result = json.loads(webdata).get('result')
            isend = result.get('isend')
            if isend is 0:
                print('*'*30,"bid=",int(bid_pid['bid']),"pid=",bid_pid['pid'],'第 %s 页'%page,'*'*30,'\n')
                for replay in result['comments']:
                    self.save_to_mongo(replay)
                self.get_comment_usr(bid_pid,page+1)

            elif isend is 1 and result['commentnum'] is not 0:
                for replay in result['comments']:
                    self.save_to_mongo(replay)
                print('最后一页评论啦，换一个话题吧！')

            else:
                print('*'*30,"bid=",int(bid_pid['bid']),'*'*10,"pid=",bid_pid['pid'],'*'*10,'第 %s 页'%page,'*'*30,'\n')
                print('此话题没有评论，换下一个话题吧！')
                pass
        except:
            print('*' * 30, "bid=", int(bid_pid['bid']), '*' * 10, "pid=", bid_pid['pid'], '*' * 10, '第 %s 页' % page,'*' * 30, '\n')
            print('访问数据出错')
            pass

    def save_to_mongo(self, result):
        try:
            db['topic_comment'].insert(result)
        except:
            print('存储mongodb失败','\n',result)
            pass

if __name__ == '__main__':
    comment = Comment()
    pool = multiprocessing.Pool(4)
    bid_pids = [bid_pid for bid_pid in db.bar_topic.find({},{'bid':1,'pid':1,'_id':0},no_cursor_timeout=True).limit(10000)]
    #取了数据库中前10000个话题爬对应的评论。实测程序运行1.5h，爬取评论648067条
    print(bid_pids)
    pool.map(comment.get_comment_usr,bid_pids)
