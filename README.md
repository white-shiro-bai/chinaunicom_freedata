# chinaunicom_freedata
一个自动处理联通免流的脚本。信息来源https://github.com/simo8102/chinaunicom-AutoSignMachine


使用方法：
1.安装wireguard。地址https://download.wireguard.com/windows-client/

2.配置config.ini文件，调整为你实际的安装路径。如果没改过安装参数，则使用默认路径即可

3.运行 pip install -r requirements.txt 安装库（这一步装过可以不用装）

4.运行update_wireguard_conf_windows_amd64.py。根据实际需求开启或关闭免流