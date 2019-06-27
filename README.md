# micropython_wifi_demo
- 基于micropython网络服务的wifi连接程序。
- 使用esp32开发测试，欢迎提交issues和pull request。

### 使用步骤

- 克隆项目，将代码上传到运行micropython固件的设备
- 首次启动时，将自动创建名为“micropython_ap”的Wi-Fi热点
- 使用手机或电脑连接Wi-Fi热点，并查看网关，esp32默认为：192.168.4.1
- 在浏览器输入网关地址，输入连接信息
- 连接成功后，下次启动将自动连接Wi-Fi
