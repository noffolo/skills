#!/usr/bin/env python3
import os
import sys
from enum import Enum
from typing import Dict
import inspect

import yaml


# def import_path_common():
#     current_dir = os.path.dirname(os.path.abspath(__file__))  # .../src
#     parent_dir = os.path.dirname(current_dir)  # .../project_root
#     parent_dir = os.path.dirname(parent_dir) + "/scripts"
#     if parent_dir not in sys.path:
#         sys.path.insert(0, parent_dir)


class YamlUtil:

    @staticmethod
    def load(path, config: Dict = {}) -> Dict:
        try:
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
                return config
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
                for key, value in config.items():
                    if key not in config:
                        config[key] = value
                return config
        except:
            pass
        return config

    @staticmethod
    def save(path, config: Dict) -> Dict:
        try:
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
        except:
            pass
        return config


class BaseEnum:

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        clsModule = cls.__module__
        cls_path = inspect.getfile(cls)
        clsFullName = f"{cls.__module__}.{cls.__name__}"
        cls_dirpath = os.path.dirname(cls_path)  # .../src
        print(
            f"🚀[{clsFullName}]({cls_path})@_{cls_dirpath}___@@@@@ 钩子==__file__:{__file__}触发{clsFullName}：检测到新子类 [{cls.__name__}] 定义完成{cls.__module__}！",
            cls, **kwargs)
        clsModulePath = clsModule.replace(".", "\\")
        current_dir = os.path.dirname(os.path.abspath(__file__))  # .../src
        print(
            f"🚀clsModulePath.in_path {current_dir.find(clsModulePath)}钩子触发23213123123213{__file__},,,,=21{clsFullName}：检测到新子类 [{cls.__name__}] 定义完成{cls.__module__}！",
            cls, **kwargs)
        config_path = os.path.join(cls_dirpath, "config.yaml")
        config = YamlUtil.load(config_path)
        cls.init(config)
        env = config.get("env")
        if env:
            env_config_path = os.path.join(cls_dirpath, f"config-{env}.yaml")
            env_config = YamlUtil.load(env_config_path)
            cls.init(env_config)

    @classmethod
    def init(cls, config=None):
        clsName = cls.__name__
        print("*******+======>>>> get cls and new ==.et fullname :", cls, config, "__clsName", clsName, "_YamlUtil",
              YamlUtil)
        clsConfig = config and config.get(clsName)
        if clsConfig:
            for config_key, config_value in clsConfig.items():
                print("*******+======>>>> get cls and new wwill set key, config_key, config_value:", cls, config,
                      config_key, config_value)
                new_config_key = config_key = config_key.upper().replace("-", "_")
                if hasattr(cls, new_config_key):
                    # print("*******+======>>>> get cls and new wwill set key, config_key, config_value:", cls, config,
                    #       config_key, config_value)
                    setattr(cls, new_config_key, config_value)
                # setattr(cls, config_key, config_value)
                # if hasattr(cls, config_key):


class ApiEnum(BaseEnum):
    API_KEY = ""

    # DATABASE_USER = "root"
    # DATABASE_PASSWORD = "root"
    # DATABASE_HOST = "192.168.1.234"
    # DATABASE_NAME = "health-cloud"
    # DATABASE_URL = f"mysql+pymysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:3306/{DATABASE_NAME}?charset=utf8mb4"
    DATABASE_URL = ""

    BASE_URL_OPEN_API = ""
    # BASE_URL_OPEN_API = "http://livemonitortest.lifeemergence.com/smyx-open-api"

    # BASE_URL_HEALTH = "https://healthtest.lifeemergence.com/jeecg-boot"
    BASE_URL_HEALTH = ""

    # OPEN_TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ0ZW5hbnROYW1lIjoi55Sf5ZG95raM546w5Lqn56CU5Zui6ZifIiwidXNlclJlYWxOYW1lIjoi55Sf5ZG95raM546w5Lqn56CU5Zui6ZifIiwidGVuYW50SWQiOjE3NzAyOTU0NTU2OTEwMDAwMDAsInJvbGVDb2RlcyI6WyJST0xFX1NNWVhfQURNSU4iLCJST0xFX1BBVElFTlQiLCJST0xFX0RPQ1RPUiIsIlJPTEVfQUlfQU5BTFlTSVMiXSwidGVuYW50Q29kZSI6IjEzMjYwNjU3MDA4IiwicGVybWlzc2lvbkNvZGVzIjpbXSwidXNlcklkIjoxNzcwMjk1NDU1NjkxMDAwMDA4LCJ1c2VybmFtZSI6MTc3MDI5NTQ1NTY5MTAwMDAwMCwic3ViIjoiMTMyNjA2NTcwMDgiLCJpYXQiOjE3NzMzMjgzNTYsImV4cCI6MTc3MzkzMzE1Nn0.6VwO6lkOU2gnGH8PLY76Fi7XxwE-R47b4gJj-HhzLUrmNuLRtib1zsljY6NBQC1hvmgtRjvLQXchyPtaAVcdYQ"
    # OPEN_TOKEN = "Bearer eyJhbGciOiJIUzUxMiJ9.eyJ0ZW5hbnROYW1lIjoi55Sf5ZG95raM546w5Lqn56CU5Zui6ZifIiwidXNlclJlYWxOYW1lIjoi55Sf5ZG95raM546w5Lqn56CU5Zui6ZifIiwidGVuYW50SWQiOjE3Njk2MTM3NzgyMjcxMDAwMDAsInJvbGVDb2RlcyI6WyJST0xFX1NNWVhfQURNSU4iLCJST0xFX1BBVElFTlQiLCJST0xFX0RPQ1RPUiIsIlJPTEVfQUlfQU5BTFlTSVMiXSwidGVuYW50Q29kZSI6IjEzMjYwNjU3MDA4IiwicGVybWlzc2lvbkNvZGVzIjpbXSwidXNlcklkIjoxNzY5NjEzNzc4MjI3MTAwMDA4LCJ1c2VybmFtZSI6MTc2OTYxMzc3ODIyNzEwMDAwMCwic3ViIjoiMTMyNjA2NTcwMDgiLCJpYXQiOjE3NzMzMzYwMDEsImV4cCI6MTc3Mzk0MDgwMX0.4QRhvaNSySVXc8-POCJbP9P3BVja45nppOlzN4RjuNt_QJC2fr2XyEGBi-K5FPBTHZ9mOW40THbm3ozLjuLkbA"
    OPEN_TOKEN = ""

    # TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IjEzODI5Mjk1NTkwIiwiZXhwIjoxNzczNDE3NTA2fQ.PA-C1yt0yWP0kAmVFXdtq2WgMha8r8q5ittOQdgFpZc"
    TOKEN = ""

    DEFAULT__REQUEST_TIMEOUT = 120

    DEFAULT__PAGE_SIZE = 5

    DEFAULT__PAGE_SIZE_MAX = 65536

    GET_DOWNLOAD_URL__URL = BASE_URL_OPEN_API + "/api/tos/get-download-url"


class ConstantEnum(BaseEnum):
    class SourceEnum(Enum):
        ARK_CLAW = "ARK_CLAW"
        FEISHU = "FEISHU"
        COZE = "COZE"
        JVS_CLAW = "JVS_CLAW"
        WUHONG = "WUHONG"
        LIGHT_HOUSE = "LIGHT_HOUSE"
        SKILL_HUB = "SKILL_HUB"
        CLAW_HUB = "CLAW_HUB"

    # ENV = "prod"
    APP__ID = ""

    APP__SOURCE = SourceEnum.CLAW_HUB.value

    IS_DEBUG = False

    CURRENT__OPEN_ID = ""

    CURRENT__USER_NAME = ""

    CURRENT__TENTANT_CODE = ""

    DEFAULT__OUTPUT_LEVEL = ""

    # FEISHU_APP__ID = "cli_a93b91388ef81bcd"
    FEISHU_APP__ID = ""

    # FEISHU_APP__SECRET = "mhbrCwTKA2f1cVKBzMStYgM2yGOaqmWW"
    FEISHU_APP__SECRET = ""

    # FEISHU_APP__RECEIVE_ID = "ou_86fdd8e0d5f116c18a9dd550abefe6d2"
    FEISHU_APP__RECEIVE_ID = ""

    @staticmethod
    def is_debug():
        return ConstantEnum.IS_DEBUG

    @classmethod
    def init(cls, config=None):
        clsName = cls.__name__
        print("*******+======>>>> get cls and new ==.et fullname  AAAA BSSE:", cls, config, "__clsName", clsName,
              "os.environ", os.environ)
        super().init(config)
        openclaw_sender_open_id = os.environ.get("OPENCLAW_SENDER_OPEN_ID")
        openclaw_sender_username = os.environ.get("OPENCLAW_SENDER_USERNAME")
        feishu_open_id = os.environ.get("FEISHU_OPEN_ID")
        if openclaw_sender_open_id:
            print("*******+======>>>> get cls and new ==.et fullname  AAAA BSSE vvvv1232132:", cls, config, "__clsName",
                  clsName, "os.environ", os.environ)
            cls.CURRENT__OPEN_ID = openclaw_sender_open_id
        if openclaw_sender_username:
            print("*******+======>>>> get cls and new ==. openclaw_sender_nameet fullname  AAAA BSSE vvvv1232132:", cls,
                  config, "__clsName",
                  clsName, "os.environ", os.environ)
            cls.CURRENT__USER_NAME = openclaw_sender_username
        if feishu_open_id:
            print("*******+======>>>> get cls and new ==.et fullname  AAAA BSSE  12121___sa:", cls, config, "__clsName",
                  clsName, "os.environ", os.environ)
            cls.FEISHU_APP__RECEIVE_ID = feishu_open_id
