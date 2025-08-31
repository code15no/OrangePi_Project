# ZeroTier使用指导

## 基本介绍

> 以下视频对于ZeroTier的介绍很好，推荐观看：
>
> https://youtu.be/y-Rfo2W_JXI?si=DxSvvBxwatP992II



### 痛点

由于我们的任务性质，我们必须要基于手上现有的开发板环境来进行模型的测试、优化等相关工作，所以**随时随地能够便捷、快速地连接到开发板**就成了我们十分关心的一个目标。在同一局域网段下，我们通常通过`SSH`来连接开发板，这里可以借助网线直连，也可以使用查询到的私有`IPv4`地址来连接。而如果不在同一个局域网下，因为很有可能你要连接的设备并没有**公网IP**，或者很难查询，所以想要定位到开发板十分麻烦。

要解决这个事情，传统的方法是**内网穿透（NAT）**，也就是通过一个**中转服务器**，来与你并没有公网IP的设备（比如路由器）建立连接，从而能够将数据转发到你要访问的特定设备。具体的原理我也没有学习过，大家有兴趣可以了解。最常用的内网穿透软件是`frp`，网上也有很多教程。但是它相比我们要用到的ZeroTier来说需要做的事情还是太多了，尤其是还需要购买、配置一个额外的服务器，配置起来非常麻烦。所以，一个更加简易的、开箱即用的方法就很有必要，ZeroTier就是这样的一种技术。

### ZeroTier能干什么？

***ZeroTier*** 用到的技术其实更加复杂，但是我们可以通俗地理解为，它为我们的各个设备创建了一个**VLAN**，并提供给每个设备一个被管理的私有地址，加入到这样的一个虚拟局域网中的设备可以通过私有地址来互相通信。这个网络的基础结构是**星形**的，由中央的根服务器决定两个要通信的设备中谁是服务端，谁是客户端，这一过程会使用UDP穿透技术建立起直接的P2P（点到点）连接；如果都不具备服务器的条件，就需要继续通过全球部署的根服务器转发数据。所以说，ZeroTier是**<u>尽力以P2P的方式通信</u>**。用户只需要注册账户，将设备加入特定ID的VLAN中，就可以和网络中的设备自由通信。听起来它真的是非常方便，简直是开箱即用的一种技术。完美适应了我们的任务场景！*另外，它的Free Trial据说可以支持最多<u>25</u>台设备加入，单个VLAN可以支持<u>10</u>台设备。所以非常良心，几乎可以适应所有非企业级的应用场景！*

> 技术细节可参考ZeroTier的官方文档：https://docs.zerotier.com/protocol/

以下，我们就来介绍如何加入我们的网络，以及如何与开发板通信。

## 操作步骤

### **Step 1 注册ZeroTier账户**

打开[ZeroTier官网](https://www.zerotier.com/)，点击`Start for Free`（可能需要科学上网技术）：

![image-20250801223334647](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801223334647.png)

![image-20250801223426821](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801223426821.png)

来到以下界面，选择任意一种方式注册。

![image-20250801223450496](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801223450496.png)

### **Step 2 完成初始设置**

以下的设置会引导你创建你的第一个个人VLAN，并下载对应系统的客户端，将当前设备加入你的网络中。

![image-20250801223955649](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801223955649.png)

![image-20250801224120853](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801224120853.png)

在点击下载对应的客户端后，你会获得你当前网络的唯一ID（16位16进制数）。

![image-20250801224253355](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801224253355.png)

下载客户端后，你会获得你当前设备的唯一ID（地址）。下图以Windows客户端为例，右击应用LOGO，`My Address`一行就是你的设备地址。

![image-20250801224617139](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801224617139.png)

### **Step 3 连接到网络**

#### Windows（客户端）

请将你需要加入的网络ID粘贴到你的ZeroTier客户端中：```AB64258FED12ABF3```（例）

粘贴后请将你的设备地址告诉网络所属者，联系他给你授权。

或者，你也可以通过扫描二维码来尝试加入网络（二维码由管理员给出）。如果这些都有问题，请联系管理员，令管理员给你的邮箱发送邀请邮件，你可以尝试通过邀请链接加入网络。

#### Linux（服务器/开发板设置，或者你个人主机是Linux）

关于各种发行版的安装措施，详细请查看[官网](https://www.zerotier.com/download/)。

如果是**红帽/Deb系**，可以执行以下两条命令之一来一键安装：

```bash
curl -s https://install.zerotier.com | sudo bash
```

```bash
curl -s 'https://raw.githubusercontent.com/zerotier/ZeroTierOne/main/doc/contact%40zerotier.com.gpg' | gpg --import && \
if z=$(curl -s 'https://install.zerotier.com/' | gpg); then echo "$z" | sudo bash; fi
```

安装成功后会显示本机的地址，请记住。随后执行以下命令加入网络：

```bash
sudo zerotier-cli join ab64258fed12abf3
```

显示成功后，就可以在管理员界面查看设备对应的IP。

### **Step 4 SSH连接到开发板**

我们的香橙派在VLAN中的信息如下（例）：

![image-20250801225830603](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801225830603.png)

其中第一串是设备对应的唯一地址，后面的第一个IPv4地址是本设备在本网络中的`Managed IP`，也就是对应此VLAN中的私有地址（`10.x`即对应A类私有地址）。最后一个IP地址是设备的实际IP地址（`Physical IP`）。我们使用的就是这个`Managed IP`来连接，也就是`10.147.19.50`。

#### 方式 1 使用`MobaXterm`

![image-20250801230447729](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801230447729.png)

随后正常输入密码`Mind@123`即可。

#### 方式2 使用`VSCode` or 其他终端软件

打开`VSCode`或者任意一款终端软件，输入以下命令：

```bash
ssh HwHiAiUser@10.147.19.50 -p22 # 使用默认用户HwHiAiUser，默认ssh端口22
```

提示输入密码，输入该用户密码，成功登录！

![image-20250801234448855](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801234448855.png)

![image-20250801234631373](C:\Users\DELL\AppData\Roaming\Typora\typora-user-images\image-20250801234631373.png)
