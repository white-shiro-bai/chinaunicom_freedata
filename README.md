# chinaunicom_freedata
一个自动处理联通免流的脚本。信息来源https://github.com/simo8102/chinaunicom-AutoSignMachine


# Windows使用方法：

1.安装wireguard。地址：https://download.wireguard.com/windows-client/

2.配置config.ini文件，调整为你实际的安装路径。如果没改过安装参数，则使用默认路径即可

3.运行 pip install -r requirements.txt 安装库（这一步装过可以不用装）

4.运行update_wireguard_conf_windows_amd64.py。根据实际需求开启或关闭免流


# 获得管理员权限的方法：

1.右键update_wireguard_conf_windows_amd64.py 选择 发送到 桌面快捷方式。

2.右键桌面上的快捷方式，选择属性，把目标那一栏前面加上 “python ”<-注意这里有个空格

3.点击高级，勾选 “已管理员身份运行”

4.确定，确定，关闭快捷方式属性。

5.运行快捷方式，会提醒获取管理员权限。选确定。然后无论执行哪个动作都不会受限了。


# 移动端（iOS/Android）使用方法：

1.安装对应系统的wireguard。地址：https://www.wireguard.com/install/

2.重复Windows的步骤

3.在Windows的第四步运行时，选择3.更新信息并展示二维码（移动端适用）。即可弹出二维码

4.运行移动端wireguard，选择扫描二维码添加。扫描后，即可在移动端创建配置文件。