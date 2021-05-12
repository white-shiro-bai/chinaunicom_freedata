# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import sys
# sys.path.append("./")
sys.setrecursionlimit(10000000)
import requests
import subprocess
from prettytable import PrettyTable
import configparser
import os

cf = configparser.ConfigParser()
cf.read(os.path.dirname(os.path.realpath(__file__))+"/config.ini",encoding='utf-8')
url = cf.get('Configs','url')
wireguard_path = cf.get('Configs','wireguard_path')
conf_path = cf.get('Configs','conf_path')

# print(open('config.txt', mode='r', encoding='utf-8').readlines)
# wireguard_path = 'C:\\Program Files\\WireGuard\\wireguard.exe'
# conf_path = 'C:\\Users\\Administrator\\Desktop\\wireguard.conf'

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
    req = requests.get(url="https://raw.githubusercontent.com/simo8102/chinaunicom-AutoSignMachine/main/%E7%BA%BF%E8%B7%AF%E6%9B%B4%E6%96%B0.md",headers=headers)
    tofile = open(conf_path, mode='w', encoding='utf-8')
    print(req.text.split("```")[1],file=tofile)
    # os.system(wireguard_path + '  /installtunnelservice  "'+ conf_path + ' "')
    subprocess.run(wireguard_path + '  /installtunnelservice  "'+ conf_path + '"')
    


def get_stop():
    pass

def get_cmd():
    with_args = ui(data={"limit_func":True,"desc":"选择要执行的命令","type":"option","display_key":"func_id","func_key":"func_id","data":[{"func_id":1,"func_name":"更新信息并启用免流"},{"func_id":2,"func_name":"停用免流"},{"func_id":3,"func_name":"纯更新"},{"func_id":4,"func_name":"纯启用免流"}]})[0]
    if with_args == '2':
        subprocess.run(wireguard_path + '  /uninstalltunnelservice wireguard')
    elif with_args == '4':
        subprocess.run(wireguard_path + '  /installtunnelservice  "'+ conf_path + '"')
    elif with_args == '1':
        getupdate()
        subprocess.run(wireguard_path + '  /installtunnelservice  "'+ conf_path + '"')
    elif with_args == '3':
        getupdate()


if __name__ == '__main__':
    get_cmd()