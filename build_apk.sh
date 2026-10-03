#!/usr/bin/env bash
# 在 WSL2 (Ubuntu) 中执行本脚本以构建安卓 APK
set -e

echo "== 更新 apt 并安装构建依赖 =="
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git zip unzip curl \
    openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev \
    libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

echo "== 安装 Buildozer =="
pip3 install --upgrade buildozer

echo "== 开始构建 APK (debug) =="
buildozer android debug

echo "== 完成 =="
echo "APK 位于 bin/ 目录下，例如：bin/pethospitalcalc-0.1-debug.apk"
