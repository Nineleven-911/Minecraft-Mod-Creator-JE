<div align="center">

![logo](Github-assets/mmc-logo.png)  

# 开发中
# Minecraft Mod Creator: Java Edition
## Minecraft 模组生成器 (以下简称 MMC)

![GitHub Repo stars](https://img.shields.io/github/stars/Nineleven-911/Minecraft-Mod-Creator-JE?style=flat)
![GitHub branch status](https://img.shields.io/github/checks-status/Nineleven-911/Minecraft-Mod-Creator-JE/main)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/Nineleven-911/Minecraft-Mod-Creator-JE)
![GitHub last commit](https://img.shields.io/github/last-commit/Nineleven-911/Minecraft-Mod-Creator-JE)
![GitHub Created At](https://img.shields.io/github/created-at/Nineleven-911/Minecraft-Mod-Creator-JE)  

</div>

# MMC是什么? 
## 简介
MMC是一个使用Python编写的快速模组(Modifcations)生成器, 开源, 使用方便。
## 优点
MMC 可以快速生成对于Minecraft JE的模组代码。暂不支持生成器GUI。
## 支持版本
Minecraft Java Edition

Fabric 1.20.1

Forge 暂不支持

Forge 可参见:

[MCreator](https://mcreator.net/)
## 注意
如果需要使用Gradle的gradle_build, 请先在

[Fabric - Template Mod Generator](https://fabricmc.net/develop/template/)

下载生成包, 所有信息按照创建ModSettings时的一致, 不选择`Spilt Client and Server`, 使用`Using Custom Id`并填上Minecraft支持的 小写字母+下划线(lowercase+underline)

# 使用方法
## 准备
1. 使用`pip install -r requirements.txt`下载需要的库
2. 将存储源码的文件夹改成一个合法的 `Python` 包(Package)名
3. 作为包导入即可
## Build时须知
1. 下载开发包 参考 MMC是什么? / 注意
2. 解压zip, 并设置ModSetting中的 `saving_path=${Your MDK Absolute location + /src}` 和 `gradle_location=${Your MDK Absolute location}`
3. 使用`ModSetting.build()`或`ModSetting.gradle_build()`
## 使用 (Fabric)
```Python
from v1_20_1 import Fabric as f
# 创建一个模组设置对象 Create a ModSettings
mod_setting = f.FabricModSettings(
    mod_id="all_the_mods",
    package_name="mc_group.all_the_mods.atm",
    main_class_name="AllTheMods",
    version="0.01.0",
    name="All The Mods! ATM",
    description="This mod adds a lot of mods! Enjoy it! ",
    saving_path="D:/MinecraftMods/FabricMods/TEST-all_the_mods-fabric-1.20.1/src",
    gradle_location="D:/MinecraftMods/FabricMods/TEST-all_the_mods-fabric-1.20.1"
)
# 创建物品 Create Item
sapphire = (
    f.Item("sapphire")
    .set_texture("sapphire.png")
    .set_translate_key("zh_cn", "蓝宝石")
)
# 添加至模组 Add it into the mod
mod_setting.connect_mod(
    sapphire
)
# Gradle 任务 Gradle Daemons
mod_setting.build(f.BUILDING_EXAMPLE) # 生成src Generate /src
mod_setting.gradle_runClient() # ./gradlew runClient
mod_setting.exit() # 退出 Exit
```

# Q&A

- Python环境报错
1. 使用`pip install -r requirements.txt`
2. 检查是否缺少文件
3. 安装一个Python 3.12.5环境
4. <span title="你是认真的? (bushi">我忘了上传文件了</span>

- Build时报错
1. 确保保存路径设置正确
2. 未使用自定义类

- `runClient` 或者 `runServer` 出现 `Uncaught Exception`
1. 检查build.gradle和settings.gradle等配置文件编写正确
2. 检查版本不支持、Fabric API版本不匹配等跟Minecraft或者Fabric的问题

- 程序在执行命令时乱码
1. 使用
``` Python
import subprocess
subprocess.run(['chcp', '65001'], shell=True)
```

- 上面都没有我的问题或者解决方案无效: 

  请在Issue或者Pull Request反馈这个问题

# 更多
## 文档
- 编写中
