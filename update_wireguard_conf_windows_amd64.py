# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import requests
import subprocess
from prettytable import PrettyTable
import configparser
import os
import qrcode


cf = configparser.ConfigParser()
cf.read(os.path.dirname(os.path.realpath(__file__))+"/config.ini",encoding='utf-8')
url = cf.get('Configs','url')
wireguard_path = cf.get('Configs','wireguard_path')
conf_path = cf.get('Configs','conf_path')
qrcode_file = cf.get('Configs','qrcode_file')
url_page = cf.get('Configs','url_page')
url_ip = cf.get('Configs','url_ip')

def gen_qrcode(code):
    qr = qrcode.QRCode(border=1,error_correction=qrcode.ERROR_CORRECT_L)
    qr.add_data(code)
    img = qr.make_image()#.convert('RGBA')
    img_w, img_h = img.size
    factor = 4
    size_w, size_h = int(img_w / factor), int(img_h / factor)
    qrfile = open(qrcode_file, mode='wb')
    img.save(qrfile, format='jpeg')


def ui(data):
    while True:
        print("\n<------------------------------------------------------------------------------------------------>")
        if 'desc' in data:
            print(data['desc'])
        if data["type"] == "option":
            if 'limit_func' in data and data['limit_func'] is True:
                #限制使用返回等功能
                display_keys = []
            else:    
                display_keys = ['~back','~refresh','~home','~exit']
            key_map = {"~back":"~back","~home":"~home","~refresh":"~refresh"} #
            if len(data["data"]) != 0:
                tb = PrettyTable(field_names=data["data"][0].keys())
                tb.padding_width = 1
                for item in data["data"]:
                    display_keys.append(str(item[data["display_key"]]))
                    row = []
                    for content in item.keys():
                        row.append(str(item[content]))
                    tb.add_row(row)
                    key_map[str(item[data["display_key"]])] = str(item[data["func_key"]])
                print(tb)
            else:
                print('无可用数据')    
            print('可供输入的'+data["display_key"]+"有：",display_keys)
            key_in = input("请输入选择的 "+data["display_key"]+" 并按回车键确认：")
            if key_in == "~back":
                return '~back','~menu'
            elif key_in == "~refresh":
                return '~refresh','~menu'
            elif key_in == "~exit":
                print("程序结束")
                exit()
            elif key_in == "~home":
                return '~home','~menu'
            elif key_in =="" and 'limit_func' in data and data['limit_func'] is True:
                continue
            elif key_in =="":
                return '~refresh','~menu'
            elif key_in not in display_keys and ',' not in key_in:
                print("\n<------------------------------------------------------------------------------------------------>\n 你输入的",key_in,"不是一个有效的输入，好好看选项，不然会报错的！")
                continue
            if ',' in key_in:
                key_out = []
                for key in key_in.split(','):
                    key_out.append(key_map[key])
                print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",','.join(key_out))
                return ','.join(key_out),key_in
            elif key_in[0] =='~':
                print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",key_in)
                return key_in,key_in
            else:
                print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",key_map[key_in])
                return key_map[key_in],key_in
        elif data["type"] == "keyword":
            key_in = input("请输入 "+data["display_key"]+" 并按回车键确认：")
            if key_in == "~exit":
                print("程序结束")
                exit()
            elif data["allow_none"] is False and key_in == '':
                print("\n<------------------------------------------------------------------------------------------------>\n "+data["display_key"] +" 选项不可以输入空字符，会报错的！")
                continue
            print("你输入的"+data["display_key"]+"是:",key_in,"执行的是：",key_in)
            if key_in != '' and key_in[0] == '~':
                return key_in,'~menu'
            return key_in,key_in
        elif data["type"] == "show":
            if len(data["data"]) != 0:
                tb = PrettyTable(field_names=data["data"][0].keys())
                tb.padding_width = 1
                for item in data["data"]:
                    row = []
                    for content in item.keys():
                        row.append(str(item[content]))
                    tb.add_row(row)
                print(tb)
                return None,None
            else:
                print('无可用数据')
                return None,None

def getupdate():
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
    }
    req = requests.get(url=url,headers=headers)
    tofile = open(conf_path, mode='w', encoding='utf-8')
    print(req.text.split("```")[1],file=tofile)
    return req.text.split("```")[1]

def getupdateip():
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
    }
    req = requests.get(url=url_ip,headers=headers)
    tofile = open(conf_path, mode='w', encoding='utf-8')
    print(req.text,file=tofile)
    return req.text


def getupdate_url():
    headers = {
        'User-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15'
    }
    req = requests.get(url=url_page,headers=headers)
    tofile = open(conf_path, mode='w', encoding='utf-8')
    keys =  req.text.split('<div class="snippet-clipboard-content position-relative"><pre><code>')[1].split('</code></pre><div class="zeroclipboard-container position-absolute right-0 top-0">')[0]
    print(keys,file=tofile)
    return keys

def get_code(ipid=3):
    if ipid == "1":
        return getupdate()
    elif ipid == "2":
        return getupdate_url()
    elif ipid == "3":
        return getupdateip()

def get_cmd():
    with_args = ui(data={"limit_func":True,"desc":"选择要执行的命令","type":"option","display_key":"func_id","func_key":"func_id","data":[{"func_id":1,"func_name":"更新信息并启用免流"},{"func_id":2,"func_name":"停用免流"},{"func_id":3,"func_name":"更新信息并展示二维码（移动端适用）"},{"func_id":4,"func_name":"不更新信息纯启用免流"}]})[0]
    if with_args == '2':
        subprocess.run(wireguard_path + '  /uninstalltunnelservice wireguard')
    elif with_args == '4':
        subprocess.run(wireguard_path + '  /installtunnelservice  "'+ conf_path + '"')
    elif with_args == '1':
        ipid = ui(data={"limit_func":True,"desc":"选择要使用的密钥来源，每天凌晨3点更新。推荐使用3","type":"option","display_key":"func_id","func_key":"func_id","data":[{"func_id":1,"func_name":"raw.github（对网络环境有要求）"},{"func_id":2,"func_name":"github，大部分网络可以访问"},{"func_id":3,"func_name":"使用作者提供的ip，只要作者服务不关，就对网络没要求"}]})[0]
        get_code(ipid=ipid)
        subprocess.run(wireguard_path + '  /installtunnelservice  "'+ conf_path + '"')
    elif with_args == '3':
        ipid = ui(data={"limit_func":True,"desc":"选择要使用的密钥来源，每天凌晨3点更新。推荐使用3","type":"option","display_key":"func_id","func_key":"func_id","data":[{"func_id":1,"func_name":"raw.github（对网络环境有要求）"},{"func_id":2,"func_name":"github，大部分网络可以访问"},{"func_id":3,"func_name":"使用作者提供的ip，只要作者服务不关，就对网络没要求"}]})[0]
        get_code(ipid=ipid)
        os.system(qrcode_file)


if __name__ == '__main__':
    print('注意！配置文件在每日凌晨会更换。每天需要重新连接。')
    get_cmd()