from fnmatch import translate
import os
from sqlite3 import DatabaseError
import sys
import subprocess
import re
from tabnanny import check
import requests
import logging
import hashlib

# logging.basicConfig(filename='/root/file.log',encoding='utf-8',level=logging.warning)

DATA = {
    'downloadDir':'/var/www/html/downloads/',
    'wkdir':'/root/',
}
DATA_onedrive = {
    'film':'/video/电影/',
    'download':'/download'
}
DATA_gdrive = {
    'film':'/视频/电影/',
    'download':'/Download'
}
video = ['mkv','mp4','mka','end']

def wkDir():
    cu_path = os.getcwd()
    if cu_path != '/root':
        os.chdir('/root')


def check_log_file():
    if os.path.exists('/root/file.log'):
        os.remove('/root/file.log')
        os.popen('touch /root/file.log')
# 既可以判断执行是否成功，还可以获取执行结果
def subprocess_popen(statement):
    p = subprocess.Popen(statement, shell=True, stdout=subprocess.PIPE)  # 执行shell语句并定义输出格式
    while p.poll() is None:  # 判断进程是否结束（Popen.poll()用于检查子进程（命令）是否已经执行结束，没结束返回None，结束后返回状态码）
        if p.wait() is not 0:  # 判断是否执行成功（Popen.wait()等待子进程结束，并返回状态码；如果设置并且在timeout指定的秒数之后进程还没有结束，将会抛出一个TimeoutExpired异常。）
            print("命令执行失败，请检查设备连接状态")
            return False
        else:
            re = p.stdout.readlines()  # 获取原始执行结果
            result = []
            for i in range(len(re)):  # 由于原始结果需要转换编码，所以循环转为utf8编码并且去除\n换行
                res = re[i].decode('utf-8').strip('\r\n')
                result.append(res)
            return result

def clean_up():
    path = DATA['downloadDir']
    g = os.walk(path)
    for p,dr,fl in g:
        for f in fl:
            if f.endswith('.aria2'):
                os.remove(p+f)


def loopup(word,language):
    url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    q = word
    salt = '112313'
    secret = '2HYilScBUeqIfObY6c2n'
    md5 = '20220120001061261'+q+salt+secret
    md5 = hashlib.md5(md5.encode('utf-8')).hexdigest()
    data = {
        'q':q,
        'from':'auto',
        'to':language,
        'appid':'20220120001061261',
        'salt':salt,
        'sign':md5
        
    }
    r = requests.post(url,data)
    return r.json()['trans_result'][0]['dst']

def log(mesg):
    # path = '/root/file.log'
    

    with open('/root/file.log','a') as f:
        print(mesg,file=f,flush=True)

def exec_shell(command):
    rt = subprocess.run(command, shell=True) 
    return rt.returncode


def common(path,suffix=''):
    check_log_file()
    command = "rclone sync" +' '+path+' '+'gdrive:'+DATA_gdrive['download']+'/'+suffix
    a = subprocess_popen(command)
    if a != False:
        log('Sync file to google drive successfully!' )
    else:
        log('Sync file to google drive error,code =%s'%a )

    # print(command)
    
    command = 'rclone move'+' '+ path + ' '+ 'onedrive:'+DATA_onedrive['download']+'/'+suffix
    a = subprocess_popen(command)
    if a != False:
        log('Sync file to onedrive successfully!')
    else:
        log('Sync file to onedrive error,code =%s'%a )
            # print(command)
    
    exit(0)



def downlaodPathUpload(path):
    clean_up()
    g = os.walk(path)
    for pa,dr,fl in g:
        for f in fl:
            name = fl
            path = pa+'/'+fl
            file(name,path)



def dir_consider(path):
    if path == DATA['downloadDir']:
        downlaodPathUpload()
    # g = os.walk(path)
    # for pa,dr,fl in g:
        






def file(name,path):
    year = ''
    #这里的path是指加上文件名的path
    #下面把名字通过.分开
    # path = path
    #这里不要加冒号，其实应该加了也无所谓
    name_list = name.split('.')

    suffix = name_list[len(name_list)-1].lower().split('"')[0]

    for i in video:
        if suffix == i:
            # print(i)
            break
        elif i == 'end':
            common(path,suffix)
            

    if len(name_list) < 2:
        name_list = name.split('-')
    elif len(name_list) < 2:
        name_list = name.split(' ')
    
    
    

    for i in name_list:
        if i.isdigit() and len(i) == 4:
            year = i
            break
    
        
    name_split = name_list[0]

    if ']' and '[' in name_split:
        # print(name_split)
        try:
            try_to_match = re.search(r'(?<=\]).*\w+\s??(?=\[)',name_split)
            word  = try_to_match.group()
        except:
            try:
                try_to_match = re.search(r'(?<=\]).*\w+\s??(?=\()',name_split)
                word  = try_to_match.group()
                
            except:
                try:
                    try_to_match = re.search(r'(?<=\]).*\w+\s??',name_split)
                    word  = try_to_match.group()
                except:
                    # name_split = name_split.split('[')[0]
                    try:
                        try_to_match = re.search(r'(?<=\[)(\w+\s*\w*\s*)+(?=\])',name_list)
                        word = try_to_match.group()
                    except:
                        name_split = name_split.split('[')[0]
                    else:
                        name_split = loopup(word,'zh')
                else:
                    
                    name_split = loopup(word,'zh')
            else:
                
                name_split = loopup(word,'zh')
        else:
            
            name_split = loopup(word,'zh')

    if year == '':
        finalDirName = "'%s'"%name_split
    else:
        finalDirName = name_split+'.'+year
    
    #path要加冒号
    check_log_file()
    command = 'rclone sync'+' '+cha(path)+' '+'gdrive:'+DATA_gdrive['film']+finalDirName+'/'
    a = subprocess_popen(command)
    if a != False:
        log('Sync file to google drive successfully!' )
    else:
        log('Sync file to google drive error!' )
    # print(command)
    command = 'rclone move' + ' ' + cha(path)+' '+'onedrive:'+DATA_onedrive['film']+finalDirName+'/'
    a = subprocess_popen(command)
    if a != False:
        log('Sync file to onedrive successfully!' )
    else:
        log('Sync file to onedrive error!' )
    
    # print(command)




#根据情况判断是否加双引号
def cha(content):
    if not '"' in content or not "'" in content:
        return '"%s"'%content
    else:
        return content

#可以获取到目录的名字
def main():
    name = ''
    
    if len(sys.argv) < 2 or sys.argv[1] == '':
        exit(1)
    
    # path = sys.argv[1]
    #下面是需要分离的路径
    path = sys.argv[1]
    

    #通过判断文件路径是否为文件夹来区分
    if os.path.isdir(path):
        # clean_up()
        # common(path)
        pass
        

    print(path)

    path_list = path.split('/')

    for n in reversed(path_list):
        if "." in n:    #如果名字里有.则判断为视频文件
            name = n
            break

    file(name,path)
    clean_up()


main()

# if __name__ == '__main__':
#     print('yes')
