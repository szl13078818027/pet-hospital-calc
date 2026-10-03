[app]

# (str) 应用标题
title = 宠物医院经营&股权测算

# (str) 包名
package.name = pethospitalcalc

# (str) 包域名（安卓/iOS 打包需要）
package.domain = org.pethospital.calc

# (str) 源码目录（main.py 所在目录）
source.dir = .

# (list) 需要包含的源文件扩展名
source.include_exts = py,png,jpg,kv,atlas

# (str) 应用版本
version = 0.1

# (list) 应用依赖
requirements = python3,kivy

# (str) 屏幕方向
orientation = portrait

# (list) 安卓权限
android.permissions = INTERNET

# (int) 目标 Android API 等级
android.api = 33

# (int) 最低 Android API 等级
android.minapi = 21

# (str) Android NDK 版本
android.ndk = 25b

# (str) Android SDK 版本
android.sdk = 24

# (bool) 显示构建日志级别 2=详细
log_level = 2

# (bool) 自动接受 SDK 许可协议
android.accept_sdk_license = True

# (bool) 关闭“在 root 下构建”的警告
warn_on_root = 0

# (bool) 全屏 0=否
fullscreen = 0
