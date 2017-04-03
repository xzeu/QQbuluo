# 2017-3-29 17:26

import json, random, requests, time, pymongo,multiprocessing,settings
from get_cateids import cateid_list
# 导入所需的模块，get_cateids，settings是当前目录下的
# 导入get_cateids为了得到其中的所有分类的cateid列表，settings是cookies和参数bkn，这两个易变，单独列出来，方便修改

client = pymongo.MongoClient('localhost')
db = client['QQbuluo']
# 用pymongo连接mongodb，并创建数据库QQbuluo

class QQbuluo():

    def __init__(self):
        self.star_url = 'https://buluo.qq.com/cgi-bin/bar/get_star_rank_list?'
        # 明星类目api接口与其他类目有差异，定义两个初始url
        # 好吧，意外发现明星类目，也可以用comm_url来获取,FUCK,不改了，将就用
        self.comm_url = 'https://buluo.qq.com/cgi-bin/bar/get_bar_list_by_category?'

    def get_bar_list(self,url,cateid,page=1):
        # 调用此函数默认请求url的第一页，url和cateid参数用来拼接完整的f_url
        headers = {
                    'accept-encoding':'gzip, deflate, sdch',
                    'accept-language':'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
                    'referer': 'https://buluo.qq.com/p/category.html?cateid={}'.format(cateid),
                    'x-requested-with':'XMLHttpRequest',
                    'Cookie':settings.cookies,
                    'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
                    }
        # playload = {
        #             "gflag": 1,
        #             "sflag": 0,
        #             "n": 20,
        #             "s": (page-1)*20,
        #             "cateid": cateid,
        #             "r": random.random(),
        #             "bkn": settings.bkn
        #             }
        f_url = url+'gflag=1&sflag=0&n=20&s={}&cateid={}&r={}&bkn={}'.format((page-1)*20,cateid,random.random(),settings.bkn)
        # (page-1)*20生成获取[0-20,20-40,40-60];cateid参见21行;
        # 抓包多测试几次会发现r是一个0-1之间的随机数，用random.random()模仿传参，发现可行；bkn参第4行
        response = requests.get(f_url,headers=headers)
        res_json = json.loads(response.text)
        # 返回内容转为json，方便存储和操作
        # print(res_json)
        results = res_json.get('result').get('bars')
        for result in results:
            print(30*"*",result.get("name"),10*"*","fans：",result.get("fans"),10*"*","pids:",result.get("pids"),30*"*")
            # 随便取几条数据，检查运行过程
            self.save_to_mongo(result)
            # 存储到mongo，函数见58行
        if page < 3:
            return self.get_bar_list(url,cateid,page+1)
            # 推荐列表只有3页，所以递归返回原函数(page+1获取下一页)执行2次
        else:
            pass

    def save_to_mongo(self, result):
        # mongodb存储函数
        if db['barlist'].insert(result):
            print('存储mongodb成功')
            return True
        return False

    def main(self,cateid):
        if cateid == 20:
            # cateid=20是明星类目，传入基本url：star_url
            self.get_bar_list(self.star_url,cateid)
        else:
            # 同66行
            self.get_bar_list(self.comm_url,cateid)

if __name__ == '__main__':
    qqbuluo = QQbuluo()
    # 创建对象
    s_time = time.time()
    # 开始时间(s)
    pool = multiprocessing.Pool(8)
    # 开多进程
    pool.map(qqbuluo.main,cateid_list)
    # 将cate_list装载入多进程,并执行
    e_time = time.time()
    # 结束时间(s)
    taken_time =e_time-s_time
    # 程序运行时间(s)，包括开多进程耗时
    print(taken_time)

# **********不同进程数执行时间比较***********
# 电脑配置：四核A8cpu，双通道2*4G内存，网络10M宽带
# 单进程27.004830837249756s
# 2进程14.66017770767212s
# 4进程 8.851022958755493s
# 8进程 7.551532983779907s ******8进程最快*******
# 16进程 11.121328115463257s
