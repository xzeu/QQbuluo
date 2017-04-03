#示例用charts（highcharts）做数据分析
import pymongo,json,charts


client = pymongo.MongoClient('localhost')
db = client['QQbuluo']
bars_info = db['barlist']
series=[]
#下面是从明沟db中取数据，并格式化成highcharts所需的数据结构
for bar_info in bars_info.find({'category':12,'fans':{'$gt':500000}},{'name':1,'fans':1,'_id':0}):
    bar_data={
        'name':bar_info['name'],
        'data':[bar_info['fans']],
        'type':'column'
    }
    series.append(bar_data)
#print(series)
charts.plot(series,options=dict(title=dict(text='QQ部落粉丝大于50w的城市'),show='inline'))