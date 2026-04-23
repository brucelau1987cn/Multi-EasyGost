# Multi-EasyGost 一键脚本使用指南 (Fork 增强版)

***
## 感谢:
1. 感谢 @ginuerzh 大佬开发的 [gost](https://github.com/ginuerzh/gost) 隧道程序，功能强大使用简单，想要详细了解的朋友可以查看[官方文档](https://docs.ginuerzh.xyz/gost/)
2. 感谢 @风萧萧兮易水寒 大佬的[原始脚本](https://www.fiisi.com/?p=125)
3. 感谢 @STSDUST 提供的EasyGost脚本（已删库），此脚本是基于其进行修改增强
4. 感谢 @KANIKIG 的 [Multi-EasyGost](https://github.com/KANIKIG/Multi-EasyGost) 上游项目
***
## 简介

> Fork 增强版项目地址:
> https://github.com/brucelau1987cn/Multi-EasyGost

***

## 🔧 v1.2.0 增强版改动

### 🆕 新功能
- **gost 版本自动获取最新版**：从 GitHub API 动态拉取最新 release 版本，不再绑定固定版本
- **gh-proxy.com 国内加速下载**：替换原已废弃的 OSS 镜像，国内机器可选加速
- **Shadowsocks2022 支持**：新增 SS2022 协议，支持 `2022-blake3-aes-128-gcm` 和 `2022-blake3-aes-256-gcm` 加密

### 🐛 Bug 修复
- 安装校验路径错误：`/usr/lib/systemctl/` → `/usr/lib/systemd/system/`
- cron 定时重启格式错误：修正为标准 6 字段 + root 用户格式
- `chmod 777` 滥用：全部改为 `chmod 755`，删除对 systemd 目录的危险权限
- `check_sys()` 过时：改用 `/etc/os-release` 检测系统（兼容现代 Debian/Ubuntu）
- 重装丢失转发规则：`check_nor_file()` 保留 rawconf 备份恢复
- 变量未加引号：修复空输入导致语法错误
- 更新源指向：从上游 KANIKIG 改为本 Fork 仓库

***

## 脚本

* 启动脚本
  ```bash
  wget --no-check-certificate -O gost.sh https://raw.githubusercontent.com/brucelau1987cn/Multi-EasyGost/master/gost.sh && chmod +x gost.sh && ./gost.sh
  ```
* 再次运行本脚本只需要输入 `./gost.sh` 回车即可

## 功能

### 原脚本功能

- 实现了 systemd 及 gost 配置文件对 gost 进行管理
- 在不借助其他工具(如 screen)的情况下实现多条转发规则同时生效
- 机器 reboot 后转发不失效
- 支持传输类型：
  - tcp+udp 不加密转发
  - relay+tls 加密

### 此脚本新增功能

- 增加了传输类型选择功能
- 新支持传输类型
  - relay+ws
  - relay+wss
- 落地机一键创建 ss/socks5/http/SS2022 代理 (gost 内置)
- 支持多传输类型的多落地简单型均衡负载
- **gh-proxy.com 国内加速下载镜像**
- 简单创建或删除 gost 定时重启任务
- 脚本自动检查更新
- 转发 CDN 自选节点 ip
- 支持自定义 tls 证书，落地可一键申请证书，中转可开启证书校验
