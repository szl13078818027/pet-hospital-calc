# 宠物医院经营 & 股权测算（Kivy）

一个用 Kivy 写的双页小工具：
- **页面1 门店盈亏测算**：前期投入、租金、工资、固定开支、月营收、变动成本率 → 月净利、保本月营业额、回本周期。
- **页面2 股权测算**：资金股 70% / 技术干股 30% → 项目估值、单资金股东占股、每名在职医生技术股。

---

## 一、桌面可运行版（Windows / macOS / Linux）

### 最简单：双击运行（Windows）
直接双击 `run.bat`，首次会自动创建虚拟环境并安装 Kivy，之后直接启动。

### 手动运行
```bash
pip install -r requirements.txt
python main.py
```

---

## 二、打包成安卓 APK

APK 构建必须依赖 Linux 工具链（Buildozer + Android SDK/NDK），**Windows 原生不支持**。
本机当前没有 WSL / JDK / Android SDK，因此请在本机开启 WSL2 后按下面步骤构建
（或把整个目录拷到任意 Linux / macOS 机器上构建）。

### 步骤（WSL2 / Ubuntu）
1. Windows 中开启 WSL2 并安装 Ubuntu（需管理员，可能重启）：
   ```powershell
   wsl --install -d Ubuntu
   ```
2. 进入 Ubuntu 终端，把本项目目录挂进去（例如放到 `~/pet-hospital-calc`）。
3. 在该目录下执行构建脚本：
   ```bash
   chmod +x build_apk.sh
   ./build_apk.sh
   ```
4. 构建完成后 APK 在 `bin/` 目录：
   `bin/pethospitalcalc-0.1-debug.apk`
5. 用数据线 / 微信 / QQ 把 APK 传到手机安装即可（debug 包无需上架）。

> 首次构建会下载 Android SDK/NDK 与编译依赖，耗时较长（数分钟到数十分钟，取决于网速）。
> 如需 release 签名包，把 `buildozer android debug` 换成 `buildozer android release` 并配置签名。

---

## 三、已修复的已知问题（相对原始代码）
- `lambda x: self.manager.current = "..."` 原写法会导致 **SyntaxError**（lambda 内不能赋值），
  已改为 `setattr(...)`。
- 股权页 `total_fund=0` 或 `doctor_cnt=0` 会触发除零崩溃，已加友好校验。
- 盈亏页 `变动成本率 ≥ 100%` 已加拦截提示。
- 股权页原“资金股东人数”字段未被使用，现用于显示人均出资并做一致性校验。

---

## 四、已新增功能（第二轮：ROI + UI 美化）
- 盈亏页新增 **年度净利润** 与 **年化回报率 ROI**（年净利 ÷ 总投入）；
  总投入为0或未盈利时 ROI 显示“— (未盈利/总投入为0)”，不崩溃。
- UI 美化（Kivy 原生 canvas，无外部资源）：
  - 医疗青绿主题色、圆角主按钮、次级配色切换按钮。
  - 圆角白卡片输入框、带内边距自动换行的白色结果卡片。
  - 每页标题、统一字段小标签、尺寸用 `dp()` 适配。
- 窗口尺寸调整为 380×760，背景统一浅色。
