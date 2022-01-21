from fnmatch import translate
import os
import sys
import subprocess
import re
import requests
import hashlib

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
    with open('/root/file.log','a') as f:
        print(mesg,file=f,flush=True)

def exec_shell(command):
    rt = subprocess.run(command, shell=True) 
    return rt.returncode


def common(path,suffix):
    command = "rclone sync" +' '+path+' '+'gdrive:'+DATA_gdrive['download']+'/'+suffix
    a = exec_shell(command)
    if a == 0:
        log('Sync file to google drive successfully!' )
    else:
        log('Sync file to google drive error,code =%s'%a )

    # print(command)
    
    command = 'rclone move'+' '+ path + ' '+ 'onedrive:'+DATA_onedrive['download']+'/'+suffix
    a = exec_shell(command)
    if a == 0:
        log('Sync file to onedrive successfully!')
    else:
        log('Sync file to onedrive error,code =%s'%a )
            # print(command)
    exit(0)

def bt_classify(path):
    common(path,'')
    

#可以获取到目录的名字
def main():
    year = ''
    name = ''
    
    if len(sys.argv) < 2 or sys.argv[1] == '':
        exit(1)
    
    # path = sys.argv[1]
    #下面是分离路径的list
    path = sys.argv[1]
    print(path)
    if sys.argv[2] != 1:
        bt_classify(path)

    path_list = path.split('/')

    for n in reversed(path_list):
        if "." in n:
            name = n
            break
    #下面把名字通过.分开
    path = path
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

    if year == '':
        finalDirName = "'%s'"%name_split
    else:
        finalDirName = name_split+'.'+year
    

    command = 'rclone sync'+' '+path+' '+'gdrive:'+DATA_gdrive['film']+finalDirName+'/'
    a = exec_shell(command)
    if a:
        log('Sync file to google drive successfully!' )
    else:
        log('Sync file to google drive error!' )
    # print(command)
    command = 'rclone move' + ' ' + path+' '+'onedrive:'+DATA_onedrive['film']+finalDirName+'/'
    a = exec_shell(command)
    if a:
        log('Sync file to onedrive successfully!' )
    else:
        log('Sync file to onedrive error!' )
    # print(command)
    




main()
