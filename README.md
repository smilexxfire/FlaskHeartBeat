# FlaskHeartBeat
## 概述
FlaskHeartBeat是一款基于flask的心跳监控程序，用于接收客户端udp心跳包，并将心跳信息美化后展示到前端

## 安装
推荐使用docker一键安装
```shell
docker run -d -p 8081:8081 -p 5006:5006/udp smilexxfire/flask-heart-beat
```
## 客户端
客户端发送心跳消息必须遵循以下条件
1. 必须使用udp发送
2. 必须为json格式消息 
2. 消息中必须包含`hostname`,`duration`字段
## 截图
![](https://qiniu.xxf.world/pic/2024/09/04/56a3c252-1323-49a0-b216-947f949339ab.png)
