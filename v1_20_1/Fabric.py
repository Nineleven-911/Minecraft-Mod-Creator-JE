import inspect
import json
import os
import shutil
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Sequence

import logger
from commons import rep_dict, rep_str, BaseFunction, Plugin, Language


def read(name: str) -> str:
    with open(Path(__file__).parent.__str__().replace("\\", "/") + "/" + name, encoding="utf-8") as f:
        return f.read()


BUILDING_EXAMPLE = {
    "fabric.mod.json": read("examples-fabric/fabric.mod.json"),
    "${mod_id}.mixins.json": read("examples-fabric/${mod_id}.mixins.json"),
    "${mod_id}.client.mixins.json": read("examples-fabric/${mod_id}.client.mixins.json"),
}

REGISTRIES: dict[str, str] = (
        json.loads(read("examples-fabric/normal-registries.json")) | {"BaseRegistry": ""})

MODELS: dict[str, str] = {
    "item": read("examples-fabric/objects-models/item_model.json")
}


class Function(BaseFunction):
    ...


class BaseRegistry:
    @abstractmethod
    def __init__(self, identifier: str):
        self.settings = {
            "id": identifier,
            "upper_id": identifier.upper(),
            "class_name": "Object" if self.__class__.__name__ == "BaseRegistry" else self.__class__.__name__,
            "properties": ""
        }
        self.gen_code = REGISTRIES[self.__class__.__name__]
        self.mc_attr = {
            "texture": "*",
            "model": "*"
        }
        self.functions: dict[str, Function | None] = {
            "onRightClick": None,
            "onLeftClick": None,
            "tick": None
        }
        self.lang = dict()

    def __str__(self):
        return self.settings["id"]

    def get_settings(self) -> dict[str, str]:
        return self.settings

    def set_texture(self, texture: str):
        self.mc_attr["texture"] = texture
        return self

    def set_model(self, model_json: str):
        self.mc_attr["model"] = model_json
        return self

    def add_translate_key(self, lang: Language, key: str):
        self.lang[lang.__str__()] = key
        return self

    def custom_function(self, function_name: str, function: Function):
        self.functions[function_name] = function
        return self

    def onRightClick(self, func: Function):
        self.functions["onRightClick"] = func
        return self

    def onLeftClick(self, func: Function):
        self.functions["onLeftClick"] = func
        return self


class Item(BaseRegistry):
    def __init__(self, identifier: str):
        super().__init__(identifier)


class Generates:
    @staticmethod
    def translate_keys(mod_id: str, language: Language, minecraft_objects: Sequence[BaseRegistry]) -> str:
        result = dict()
        # print(language)
        for o in minecraft_objects:
            if isinstance(o, Item):
                result[f"item.{mod_id}.{o.settings["id"]}"] = o.lang[language.__str__()]

        return json.dumps(result, indent=2)


class FabricModSettings:
    class BuildingClass:
        def __init__(self, fms):
            self.super: FabricModSettings = fms

        def item(self, items: list[Item]):
            def get_all(examples: str, gens: list):
                res = []
                for g in gens:
                    res.append("    " + rep_str(examples, g.settings))
                return res

            logger.info("Item class ModItems building...")
            return rep_str(
                read("examples-fabric/Java-class/ModObjects/ModItems.java"),
                self.super.setting | {"registers": "\n".join(get_all(REGISTRIES["Item"], items))})

    def __init__(
            self,
            mod_id: str = "example_mod",
            package_name: str = "com.example",
            main_class_name: str = "ExampleMod",
            version: str = "1.0.0",
            name: str = "Example Mod",
            description: str = "This is an example description! Tell everyone what your mod is about!",
            saving_path: str = "C:/mmc_generates",

            gradle_location: str | None = None
    ):
        self.building_class = FabricModSettings.BuildingClass(self)
        self.setting = {
            "package_name": package_name,
            "mod_id": mod_id,
            "version": version,
            "main_class_name": main_class_name,
            "name": name,
            "desc": description
        }
        self.class_path = {
            "main": f"{package_name}.{main_class_name}",
            "client": f"{package_name}.{main_class_name}Client",
            "fabric-datagen": f"{package_name}.{main_class_name}DataGenerator",
            "mixins": f"{package_name}.mixins.{main_class_name}Mixin",
            "client-mixins": f"{package_name}.mixins.{main_class_name}ClientMixin"
        }
        self.minecraft_objects: dict[str, list] = {
            "Item": []
        }
        self.__enable_plugins = []
        self.__saving_path = saving_path.replace("\\", "/") + "/main"
        self.__saving_path_out_main = saving_path.replace("\\", "/")
        self.__gradle = gradle_location

    def enable_plugins(self, *plugins: Plugin.Fabric):
        self.__enable_plugins.append(i for i in plugins)

    def build_jsons(self, example: dict[str, str]):
        results: dict[str, str] = {
            "fabric.mod.json": "",
            "${mod_id}.mixins.json": "",
            "${mod_id}.client.mixins.json": ""
        }
        # 生成时 json #
        # fabric.mod.json
        res = rep_str(example["fabric.mod.json"], self.setting)
        logger.info("\"fabric.mod.json\" generated.")

        results["fabric.mod.json"] = json.dumps(res, indent=2)

        # ${mod_id}.mixins.json
        res = rep_str(example["${mod_id}.mixins.json"], self.setting)
        logger.info("\"${mod_id}.mixins.json\" generated.")

        results["${mod_id}.mixins.json"] = json.dumps(res, indent=2)

        # ${mod_id}.client.mixins.json
        res = rep_str(example["${mod_id}.client.mixins.json"], self.setting)
        logger.info("\"${mod_id}.client.mixins.json\" generated.")

        results["${mod_id}.client.mixins.json"] = json.dumps(res, indent=2)

        return results

    def connect(self, *args):
        for arg in args:
            if isinstance(arg, Item):
                self.minecraft_objects["Item"].append(arg)
            else:
                raise ValueError("Class of args was not a subclass of BaseRegistry.")

    def build(self, mod_json: dict[str, str], languages: Sequence[Language], exist_ok: bool = False):
        def create_folder(path: str, change_to: bool = True):  # 判断path是否存在, 不存在则创建
            path = path.replace("\\", "/")
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info("Path", path
                if self.__saving_path not in path else path.replace(self.__saving_path, ""),
                            "does not exist. Created directory.")
            if change_to:
                os.chdir(path)
            logger.info("Working directory changed to",
                        os.getcwd().replace("\\", "/").replace(self.__saving_path, ""),
                        "successfully."
                        )

        def write(name: str, text: str, add: bool = False):
            with open(
                    os.getcwd().replace("\\", "/") + "/" + name,
                    "w+" if not add else "a",
                    encoding="utf-8"
            ) as file:
                file.write(text)
            logger.info("File", name, "built.")

        # 删除已经存在的目录
        create_folder(self.__saving_path_out_main)
        if "main" in os.listdir(os.getcwd()) and not exist_ok:
            logger.info("/src/main already exists. Deleting directory.")
            shutil.rmtree("main")
        create_folder(self.__saving_path)

        # 生成 main/java
        create_folder(self.__saving_path + "/java")
        create_folder(self.setting["package_name"].replace(".", "/"))

        # 样板 Mixins
        create_folder("mixin", False)
        write(
            f"mixin/{self.setting["main_class_name"]}Mixin.java",
            rep_str(read("examples-fabric/Java-class/MODMixin.java"), self.setting |
                    {"MIXIN_CLASS_NAME": f"{self.setting["main_class_name"]}Mixin"})
        )
        write(
            f"mixin/{self.setting["main_class_name"]}ClientMixin.java",
            rep_str(read("examples-fabric/Java-class/MODClientMixin.java"), self.setting |
                    {"MIXIN_CLASS_NAME": f"{self.setting["main_class_name"]}ClientMixin"})
        )

        # ModItems.java
        write(
            "ModItems.java",
            self.building_class.item(self.minecraft_objects["Item"])
        )

        # MainClass.java
        write(
            self.setting["main_class_name"].replace(".", "/") + ".java",
            rep_str(read("examples-fabric/Java-class/MainClass.java"),
                    self.setting | {"activating_functions": "\n".join([
                        "ModItems.onRegistry();"
                    ])}
                    )
        )
        # MainClassClient.java
        write(
            self.setting["main_class_name"].replace(".", "/") + "Client.java",
            rep_str(read("examples-fabric/Java-class/MainClassClient.java"),
                    self.setting | {"CLASS_NAME": f"{self.setting["main_class_name"]}Client"}
                    )
        )
        # DataGenerator (样板代码)
        write(
            self.setting["main_class_name"].replace(".", "/") + "DataGenerator.java",
            rep_str(read("examples-fabric/Java-class/DataGenerator.java"),
                    self.setting | {"CLASS_NAME": f"{self.setting["main_class_name"]}DataGenerator"}
                    )
        )
        # /todo

        # 生成 main/resources
        create_folder(self.__saving_path + "/resources")

        for k, v in self.build_jsons(mod_json).items():
            write(rep_str(k, self.setting), json.loads(v))

        # 生成 main/resources/assets
        create_folder(self.__saving_path + "/resources/assets/" + self.setting["mod_id"])
        shutil.copy2(Path(__file__).parent.__str__() + "/" + "examples-fabric/Example-Icon.png", "../icon.png")
        # 语言文件 /lang
        create_folder("lang")
        # Developer native: zh_cn 简体中文 Chinese (Simplified)
        logger.info("Building language files...")
        for lang in languages:
            lang_string = lang.__str__().replace(lang.__class__.__name__ + ".", "")
            write(
                f"{lang_string}.json",
                Generates.translate_keys(
                    self.setting["mod_id"],
                    lang,
                    self.minecraft_objects["Item"]
                )
            )
            logger.info("Language", lang_string + ".json built.")
        # 模型文件 /models
        create_folder("../models")
        # Items
        create_folder("item")
        for item in self.minecraft_objects["Item"]:
            write(f"{item.__str__()}.json", rep_str(MODELS["item"], self.setting | item.settings))
            logger.info("Item model:", item.__str__(), "built.")
        # /todo
        # 材质文件 textures
        create_folder("../../textures")
        # Items
        create_folder("item")
        for item in self.minecraft_objects["Item"]:
            shutil.copy2(
                item.mc_attr["texture"],
                f"{item.settings["id"]}.png")
            logger.info("Copy object texture from absolute location:", item.mc_attr["texture"], ".")

        # 生成 main/resources/data
        create_folder(self.__saving_path + "/resources/data")
        # /todo
        logger.info("Built modification's resources status: COMPLETE.", on_thread="building")

    def gradle_execute(self, command: list[str]):
        now_loc = os.getcwd()
        os.chdir(self.__gradle)
        using_gradle_bat = "gradlew.bat" if os.name == "nt" else "./gradlew"
        os.system(using_gradle_bat + " " + " ".join(command))
        os.chdir(now_loc)

    def gradle_build(self):
        self.gradle_execute(["build"])

    def gradle_runClient(self):
        self.gradle_execute(["runClient"])

    def exit(self):
        input("FabricModSettings object " + self.__repr__() + " executes complete. Press Enter to exit.")
        raise SystemExit(0)
