import json
from abc import abstractmethod, ABC
from enum import Enum


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x + other, self.y + other, self.z + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x - other, self.y - other, self.z - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        return NotImplemented

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"


class BaseFunction:
    def __init__(self, class_name: str, package: str):
        self.class_name = class_name
        self.codes = []
        self.package = package

    def create_entity(self, vec: Vector3, entity_type: str):
        self.codes.append(
            f"{entity_type} entity_obj = {entity_type}();"
        )
        return self


class Plugin:
    class Fabric(Enum):
        TemplateModGenerator_OnWebDriver = 0
        TemplateModGenerator_OnLocal = 1

    class Forge(Enum):
        MdkDownload_OnWebDriver = 0
        MdkDownload_OnLocal = 1


class Language(Enum):
    zh_cn = "zh_cn"
    en_us = "en_us"


def rep_str(text: str, mapping: dict[str, str]):
    """
    替换 text 中的 ${}

    :param text: 要进行替换的字符串
    :param mapping: 字符串中 ${} 的映射
    :return: 替换后的字符串
    """
    for key, value in mapping.items():
        text = text.replace(f"${{{key}}}", value)

    return text


def rep_dict(d_text: str | dict[str, any], mapping: dict[str, str], replace_key: bool = False) -> dict:
    """
    替换 text 中键和值的 ${}

    :param d_text: 要进行替换的字符串JSON (字典)
    :param mapping: 字符串中 ${} 的映射
    :param replace_key: 是否替换键中的 ${}
    :return: 替换后的字典
    """
    # {"aa${w}": "b${q}", "bb": {"aaa", "${lai-cai}"}}
    # 初始化结果字典
    result = dict()

    # 根据 d_text 类型，将其转换为字典
    if isinstance(d_text, dict):
        text = d_text
    else:
        text = json.loads(d_text)
    # 遍历字典的键值对
    for key, value in text.items():
        # 如果值是dict或list类型，则递归调用 replace_dict
        if isinstance(value, dict):
            value = rep_dict(value, mapping)
        elif isinstance(value, list):
            value = [rep_str(i, mapping) for i in value]
        # 如果值是字符串类型，则调用 replace_str 替换字符串中的 ${}
        elif isinstance(value, str):
            value = rep_str(value, mapping)
        # 根据 replace_key 参数决定是否替换键
        if replace_key:
            result[rep_str(key, mapping)] = value
        else:
            result[key] = value

    # 返回替换后的结果字典
    return result
