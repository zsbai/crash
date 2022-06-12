import flask,json
from flask import request
from flask import jsonify
from flask.helpers import url_for
import xlrd
import os 
import yaml
from random import randint


server = flask.Flask(__name__)

@server.route('/')
def index():
    url = url_for('word')
    return flask.redirect(url)

def get_token_from_alist():
    yamlPath = os.path.join('/opt/alist/', 'conf.yml')
    with open(yamlPath, 'r', encoding='utf-8') as f:
        x = yaml.load(f)
    refresh_token = x['ali_drive']['drives'][0].get('refresh_token')
    return refresh_token
# @server.route('/token',methods=['get','post'])
# def token():
#     # yamlPath = os.path.join('/opt/alist/', 'conf.yml')
#     # with open(yamlPath, 'r', encoding='utf-8') as f:
#     #     x = yaml.load(f)
#     # refresh_token = x['ali_drive']['drives'][0].get('refresh_token')
    
#     used = request.form.get('application')
#     if request.method == 'POST':
#         authority = request.form.get('token')
#         if authority == 'bailu':
#             rep = {'code':'success','token':get_token_from_alist()}
#             return jsonify(rep)
#         else:
#             rep = {'code': 'failed,need login','au':authority}
#             return jsonify(rep)

    # elif request.method == 'GET':
    #     authority = request.values.get('token',default='error')
    #     rep ={'message':'dont support this method','authority':authority}
    #     return jsonify(rep)





@server.route('/word/<chapter>')
def chapter(chapter):
    return '%s'%chapter
@server.route('/word/random',methods=['get'])
def word():
    xlsx = xlrd.open_workbook('/Users/bailu/Documents/work/python/单词.xlsx')
    table = xlsx.sheet_by_index(0)
    nrows = table.nrows# 获取表格总共的行数
    word_list = [table.cell_value(x,0) for x in range(1,nrows)]#获取单词列表
    character_list = [table.cell_value(x,1) for x in range(1,nrows)]#获取词性列表
    chinese_list = [table.cell_value(x,2) for x in range(1,nrows)]#获取中文翻译列表
    value = randint(1,nrows)#获取一个随机整数，在1-表格总数之间
    word = word_list[value]#获取列表中的随机数单词
    character = character_list[value]#同理
    chinese = chinese_list[value]#一样
    how_to_use_list = [table.cell_value(x,4) for x in range(1,nrows)]
    example_sentense_list = [table.cell_value(x,5) for x in range(1,nrows)]
    example_sentense_cn_list = [table.cell_value(x,6) for x in range(1,nrows)]
    how_to_use = how_to_use_list[value]
    example_sentense = example_sentense_list[value]
    example_sentense_cn = example_sentense_cn_list[value]

    while word == '' or chinese == '':#如果单词或者中文意思为空
        value = randint(1,nrows)#获取新的随机值
        word = word_list[value]#获取新的单词
        character = character_list[value]
        chinese = chinese_list[value]
        how_to_use = how_to_use_list[value]
        example_sentense = example_sentense_list[value]
        example_sentense_cn = example_sentense_cn_list[value]

    chapter_point = []#设置一个空列表
    for x in range(1,nrows):#在1-列表总数之间的所有值
        words = table.cell_value(x,0)#所有y=0的值
        if type(words) ==float:#如果这个值是小数
            chapter_point.append(x)#把这个值添加到空列表

    num = len(chapter_point)#查看list中的数量
    
    chapter = ''
    i= 0

    while i < num:
        if chapter_point[i-1]<value< chapter_point[i]:#如果单词的x坐标在第一个标题之后在第二个标题之前
            
            chapter = (table.cell_value(chapter_point[i-1],1))#就返回第一个标题，即为英文阅读的标题
            break
        else:
            # print(chapter)
        # else:
        #     i += 1
            i = i+1
    if chapter == '':
        chapter = table.cell_value(chapter_point[num-1],1)


    if how_to_use == '':
        how_to_use = 'No data'
    if example_sentense == '':
        example_sentense = 'No data'
    if example_sentense_cn == '':
        example_sentense_cn = 'No data'
    resp = {
        '-------':'-------',
        'Chapter':chapter,
        'Word':word,
        'Character':character,
        'Chinese':chinese,
        '---------':'---------',
        'How_to_use_this_word': how_to_use,
        'Example_Sentense': example_sentense,
        'Example_translation':example_sentense_cn,
        '-----------':'-------------',
        
    }
    return jsonify(resp)


@server.route('/post/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@server.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id


@server.route('/login',methods=['get','post'])
def login():
    username = request.values.get('name')
    pwd=request.values.get('pwd')
    if username and pwd:
        if username == 'xiaoming' and pwd == '111':
             resu={'code':200,'message':'登录成功'}
             return json.dumps(resu,ensure_ascii=False)#将字典转换为Json串，json是字符串
        else:
             resu={'code':-1,'message':'账号密码错误'}
             return json.dumps(resu,ensure_ascii=False)
 
    else:
        resu={'code':1001,'message':'参数不能为空'}
        return json.dumps(resu,ensure_ascii=False)

if __name__== '__main__':
    # from waitress import serve
    # serve(server, host='0.0.0.0',port='8999')
    server.config['JSON_AS_ASCII'] = False
    server.config['JSONIFY_MIMETYPE'] ="application/json;charset=utf-8"
    server.config['JSONIFY_PRETTYPRINT_REGULAR']=False
    server.run(debug=True,port = 8888,host='0.0.0.0')
