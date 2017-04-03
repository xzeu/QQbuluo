# 取出所有部落分类的cateid
# 程序运行有时候cateid_list为空，多运行几次就可
# 2017-3-29 15:18

import requests
from bs4 import BeautifulSoup


def get_cateids():
    main_url = 'https://buluo.qq.com/p/index.html'
    response = requests.get(main_url)
    soup = BeautifulSoup(response.text,'lxml')
    soup_a = soup.select('div.category.clearfix > a')
    #用bs的css选择器筛出所有带cate_id的<a>标签
    cateid_list = []
    for a in soup_a:
        # print(cateid)
        # name = a.get_text()
        cateid = a.get('href').split('=')[-1]
        # data = {'cate_name':name,'cateid':cateid}
        cateid_list.append(int(cateid))
    return cateid_list

if __name__ == '__main__':
    cateid_list = get_cateids()
    print(cateid_list)


# 运行结果是固定值，这里直接列出，方便以后取用
cateid_list = [20, 10, 11, 14, 58, 50, 49, 12, 51, 23, 61, 19, 47, 38, 41, 53, 35, 48, 39, 21, 40, 42, 43, 57, 52, 54, 55, 59, 56, 13, 24]




# cateids = [{'cateid': '20', 'name': '明星'}, {'cateid': '10', 'name': '游戏'},
#            {'cateid': '11', 'name': '情感'}, {'cateid': '14', 'name': '爱好'},
#            {'cateid': '58', 'name': '综艺'}, {'cateid': '50', 'name': '电视剧'},
#            {'cateid': '49', 'name': '电影'}, {'cateid': '12', 'name': '地区'},
#            {'cateid': '51', 'name': '生活'}, {'cateid': '23', 'name': '动漫'},
#            {'cateid': '61', 'name': '体育竞技'}, {'cateid': '19', 'name': '运动健身'},
#            {'cateid': '47', 'name': '幽默'}, {'cateid': '38', 'name': '小说'},
#            {'cateid': '41', 'name': '女性'}, {'cateid': '53', 'name': '文艺'},
#            {'cateid': '35', 'name': '星座'}, {'cateid': '48', 'name': '闲趣'},
#            {'cateid': '39', 'name': '亲子'}, {'cateid': '21', 'name': '娱乐'},
#            {'cateid': '40', 'name': '旅行'}, {'cateid': '42', 'name': '宠物'},
#            {'cateid': '43', 'name': '饮食'}, {'cateid': '57', 'name': '互联网'},
#            {'cateid': '52', 'name': '网络红人'}, {'cateid': '54', 'name': '健康养生'},
#            {'cateid': '55', 'name': '闲聊'}, {'cateid': '59', 'name': '媒体'},
#            {'cateid': '56', 'name': '数码'}, {'cateid': '13', 'name': '学校'},
#            {'cateid': '24', 'name': '其他'}]
