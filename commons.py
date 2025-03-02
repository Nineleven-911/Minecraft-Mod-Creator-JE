import json
import os
import sys

from logger import logger


class ModSettings:
    def __init__(
            self,
            mod_id: str = "example_mod",
            package_name: str = "com.example.examplemod",
            main_class_name: str = "ExampleMod",
            version: str = "1.0.0",
            name: str = "Example Mod",
            description: str = "This is an example description! Tell everyone what your mod is about!",
            saving_path: str = "C:/mmc_generates"
    ):
        self.__setting = {
            "package_name": package_name,
            "mod_id": mod_id,
            "version": version,
            "main_class_name": main_class_name,
            "name": name,
            "desc": description
        }
        self.__class_path = {
            "main": f"{package_name}.{main_class_name}",
            "client": f"{package_name}.{main_class_name}Client",
            "fabric-datagen": f"{package_name}.{main_class_name}DataGenerator",
        }
        self.__saving_path = saving_path.replace("\\", "/") + "/main"

    def build_jsons(self, example: str):
        results = []

        # fabric.mod.json
        def recursion_replacing(k, v):
            if isinstance(v, str):
                for key, value in self.__setting.items():
                    v = v.replace(f"${{{key}}}", value)
                return v
            elif isinstance(v, dict):
                return {inner_key: recursion_replacing(inner_key, inner_val) for inner_key, inner_val in v.items()}
            elif isinstance(v, list):
                return [recursion_replacing(k, item) for item in v]
            else:
                return self.__setting.get(k, v)

        res = {}
        k_v: dict[str, any] = json.loads(example)

        for k, v in k_v.items():
            res[k] = recursion_replacing(k, v)
        logger.info("\"fabric.mod.json\" generated.")

        results.append(json.dumps(res, indent=2))

        # ${mod_id}.mixins.json

        # ${mod_id}.client.mixins.json

        return results

    def build(self, mod_json: str, is_substitution: bool = True):
        def create_and_change(path: str):  # 判断path是否存在, 不存在则创建
            if not os.path.exists(path):
                os.makedirs(path)
                logger.info("Path", path
                if self.__saving_path not in path else path.replace("\\", "/").replace(self.__saving_path, ""),
                            "does not exist. Created directory.")
            os.chdir(path)
            logger.info("Working directory changed to",
                        os.getcwd().replace("\\", "/").replace(self.__saving_path, ""), "."
                        )
        # 生成 main/java
        create_and_change(self.__saving_path + "/java")

        create_and_change(self.__setting["package_name"].replace(".", "/"))
        # /todo

        # 生成 main/resources
        create_and_change(self.__saving_path + "/resources")

        # 生成 main/resources/assets
        create_and_change(self.__saving_path + "/resources/assets")
        # /todo

        # 生成 main/resources/data
        create_and_change(self.__saving_path + "/resources/data")
        # /todo
