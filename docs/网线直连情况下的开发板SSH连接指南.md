# 网线直连情况下的开发板SSH连接指南

## 前言

通过在本子网内逐一搜索获得IP来连接开发板这一方法实在效率低下，当开发板在手的时候，设置以太网静态IP可以便捷地通过以太网私有IP地址连接开发板。以下给出具体步骤。

## 设置步骤

### PC端设置（`Windows`为例）

通过网线连接后，一般来说对应的网络适配器是`以太网0`。我们需要修改网络适配器的属性，从而实现静态IP。

1. 在任务栏的搜索框中输入“管理网络适配器设置”，并进入设置页面。

   ![image-20250802003638546](https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802003638546.png)

   > 或者打开“设置”——“网络和Internet”——“高级网络设置”

2. 找到当前的WLAN，编辑网络适配器属性，打开共享功能，并设置共享连接的网络适配器为“以太网”：

   <img src="https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802015538927.png" alt="image-20250802015538927" style="zoom:50%;" />

   <img src="https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802015515164.png" alt="image-20250802015515164" style="zoom:50%;" />

3. 找到最下面的“以太网”，编辑网络适配器属性（下图中，找到“更多适配器选项”，点击“编辑”）：

   ![image-20250802004358079](https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802004358079.png)

   找到下图所示的IPv4功能，双击打开：

   <img src="https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802004537022.png" alt="image-20250802004537022" style="zoom: 50%;" />

   <img src="https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802004714104.png" alt="image-20250802004714104" style="zoom:50%;" />

   设置成上图这样，点“确定”保存。

   > 实际上，应该只需要把Windows端的IP设置成同一网段的IP就可以？
   
   > 实际上先设置好WLAN的共享，打开后好像是会自动变成上图这样？如果已经变成这样，不要动，直接退出；如果仍然显示自动获得，可以直接尝试`ssh`连接试一下，如果不好使再调整。

这下个人电脑这边就好了，剩下需要调整开发板。

### 开发板设置

> 已经提前设置好，这一部分无需远程用户操作。项目中运维负责人需要注意。

#### 静态IP设置

实际上，就是通过以下两条命令来设置网关地址和静态IP地址，并把它加入到开机自动执行的命令里（`/etc/profile`）：

```bash
ifconfig eth0 192.168.137.30 up # IPv4 addr of ethernet0
route add default gw 192.168.137.1 # gw: gateway
```

> 实际使用时会遇到权限问题，这时候可以通过设置`setuid`权限位来解决特定命令的权限问题。具体来说，执行以下命令：
>
> ```bash
> sudo chmod u+s /usr/sbin/ifconfig
> sudo chmod u+s /usr/sbin/route
> ```
>
> 或者也可以通过修改`sudoers`文件来实现，但是在这个板子上似乎并不好使，暂不清楚缘由。

所以，现在这个板子在通过网线和电脑直连时，以太网的IPv4地址是`192.168.137.30`，默认网关是`192.168.137.1`。

#### 解决`nmcli`自动管理与以上设置冲突的问题

实际连接中会发现，按照以上方法设置开发板虽然在每次开机时可以顺利进入，但是过了一小会就会自动断开连接，并且按照原IP输入重新尝试连接时不成功。经过检查后，发现是因为`Network Manager`默认会自动配置以太网的IP，所以就会出现当它重新配置IP后导致SSH连接失效的问题。以下给出解决方案。

```bash
(base) root@orangepiaipro:~# nmcli
eth0: connected to Wired connection 1 # 记住此处的以太网名
        "eth0"
        ethernet (hns3-platform), C0:74:2B:FD:DA:7C, hw, mtu 1500
        ip4 default
        inet4 192.168.137.118/24
        route4 192.168.137.0/24 metric 100
        route4 default via 192.168.137.1 metric 100
        inet6 fe80::5ee1:4c5d:b5b:38fa/64
        route6 fe80::/64 metric 1024

ztksezojiz: connected (externally) to ztksezojiz
        "ztksezojiz"
        tun, F6:73:45:D2:49:36, sw, mtu 2800
        inet4 10.147.19.148/24
        route4 10.147.19.0/24 metric 0
        inet6 fe80::f473:45ff:fed2:4936/64
        route6 fe80::/64 metric 256

wlan0: connected to HUAZHU-Hanting
        "Realtek Wi-Fi"
        wifi (rtl8821cu), 28:F5:2B:A7:BA:FC, hw, mtu 1500
        inet4 192.168.51.66/20
        route4 192.168.48.0/20 metric 600
        route4 default via 192.168.50.254 metric 600
        inet6 fe80::9fa0:1515:8e49:293a/64
        route6 fe80::/64 metric 1024

docker0: connected (externally) to docker0
        "docker0"
        bridge, 4E:DF:DB:0D:51:05, sw, mtu 1500
        inet4 172.17.0.1/16
        route4 172.17.0.0/16 metric 0

p2p-dev-wlan0: disconnected
        "p2p-dev-wlan0"
        wifi-p2p, hw

bond0: unmanaged
        "bond0"
        bond, 7A:9D:C3:16:FE:49, sw, mtu 1500

lo: unmanaged
        "lo"
        loopback (unknown), 00:00:00:00:00:00, sw, mtu 65536

DNS configuration:
        servers: 192.168.137.1
        domains: mshome.net
        interface: eth0

        servers: 210.22.70.3 210.22.84.3

(base) root@orangepiaipro:~# nmcli con show "Wired connection 1" # 网络名超过一个单词需要用引号套住
connection.id:                          Wired connection 1
connection.uuid:                        da58fe05-e694-3bc2-a263-10aa9038fa98
connection.stable-id:                   --
connection.type:                        802-3-ethernet
connection.interface-name:              eth0
connection.autoconnect:                 yes
connection.autoconnect-priority:        -999
connection.autoconnect-retries:         -1 (default)
connection.multi-connect:               0 (default)
connection.auth-retries:                -1
connection.timestamp:                   1754714736
connection.read-only:                   no
connection.permissions:                 --
connection.zone:                        --
connection.master:                      --
connection.slave-type:                  --
connection.autoconnect-slaves:          -1 (default)
connection.secondaries:                 --
connection.gateway-ping-timeout:        0
connection.metered:                     unknown
connection.lldp:                        default
connection.mdns:                        -1 (default)
connection.llmnr:                       -1 (default)
connection.dns-over-tls:                -1 (default)
connection.wait-device-timeout:         -1
802-3-ethernet.port:                    --
802-3-ethernet.speed:                   0
802-3-ethernet.duplex:                  --
802-3-ethernet.auto-negotiate:          no
802-3-ethernet.mac-address:             --
802-3-ethernet.cloned-mac-address:      --
802-3-ethernet.generate-mac-address-mask:--
802-3-ethernet.mac-address-blacklist:   --
802-3-ethernet.mtu:                     auto
802-3-ethernet.s390-subchannels:        --
802-3-ethernet.s390-nettype:            --
802-3-ethernet.s390-options:            --
802-3-ethernet.wake-on-lan:             default
802-3-ethernet.wake-on-lan-password:    --
802-3-ethernet.accept-all-mac-addresses:-1 (default)
ipv4.method:                            auto  # 看到关键在这里，IPv4的设置是auto模式，且未设置默认的DNS，所以才会出现问题。
ipv4.dns:                               --
ipv4.dns-search:                        --
ipv4.dns-options:                       --
ipv4.dns-priority:                      0
ipv4.addresses:                         --
ipv4.gateway:                           --
ipv4.routes:                            --
ipv4.route-metric:                      -1
ipv4.route-table:                       0 (unspec)
ipv4.routing-rules:                     --
(base) root@orangepiaipro:~# nmcli con mod "Wired connection 1" ipv4.method manual ipv4.addresses 192.168.137.30/24 ipv4.gateway 192.168.137.1 #设置IPv4手动管理，地址为192.168.137.30，网关为192.168.137.1
(base) root@orangepiaipro:~# nmcli con mod "Wired connection 1" ipv4.dns "114.114.114.114 8.8.8.8" # 设置DNS
(base) root@orangepiaipro:~# nmcli con down "Wired connection 1" && nmcli con up "Wired connection 1" # 重启网络
Connection 'Wired connection 1' successfully deactivated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/154)
Connection successfully activated (D-Bus active path: /org/freedesktop/NetworkManager/ActiveConnection/155)

```

按照以上步骤配置，就能重新使用SSH连接了。

## 连接

### 使用`MobaXterm`

<img src="https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802015915272.png" alt="image-20250802015915272" style="zoom:50%;" />

<img src="https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802015943892.png" alt="image-20250802015943892" style="zoom:50%;" />

测试是否能正常上网：

```bash
(base) HwHiAiUser@orangepiaipro:~$ curl baidu.com
<html>
<meta http-equiv="refresh" content="0;url=http://www.baidu.com/">
</html>
(base) HwHiAiUser@orangepiaipro:~$ clashon
[sudo] password for HwHiAiUser:
😼 已开启代理环境
(base) HwHiAiUser@orangepiaipro:~$ curl google.com
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>301 Moved</TITLE></HEAD><BODY>
<H1>301 Moved</H1>
The document has moved
<A HREF="http://www.google.com/">here</A>.
</BODY></HTML>
(base) HwHiAiUser@orangepiaipro:~$

```

一切正常！

### 使用`VSCode`

输入`ssh HwHiAiUser@192.168.137.30 -p22`后，进入连接：

![image-20250802020213850](https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802020213850.png)

![image-20250802020302140](https://github.com/code15no/OrangePi_Project/blob/main/docs/notes_images/image-20250802020302140.png)

成功！
