# -*- coding: utf-8 -*-
import os

import yaml
import shutil
from pprint import pprint

yaml.warnings({'YAMLLoadWarning': False})

"""
配置支持单继承，逐级覆盖
"""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 默认配置文件
# DEFAULT_CONFIG = "default_config.json"
DEFAULT_CONFIG = "default_config.yml"

# 配置文件目录
CONFIG_DIR = ""

# 用户自动以基本的文件
# BASE_CONFIG = "config.json"
BASE_CONFIG = "config.yml"


def parse_config(args):
    """读取配置"""

    # 解析参数
    config_file = None
    if args.test_config:
        config_file = args.test_config

    if args.config:
        config_file = args.config

    if not config_file:
        raise Exception("not config_file")

    # 读取基本配置
    # config = json.load(open(os.path.join(BASE_DIR, DEFAULT_CONFIG)))
    default_config_file = os.path.join(BASE_DIR, DEFAULT_CONFIG)
    default_config = yaml.load(open(default_config_file))

    # 配置继承栈, 添加基类
    config_list = []

    while True:
        # 加载用户自定义基本配置
        if not os.path.exists(config_file):
            raise Exception(f"config file not found {config_file}")

        # base_config = json.load(open(base_config_file))
        custom_config = yaml.load(open(config_file))
        config_list.append(custom_config)

        # 读取父配置
        config_file = custom_config.get("extends")
        if not config_file:
            break

        if not config_file.endswith(".yml"):
            config_file = config_file + '.yml'

    config_list.reverse()

    for temp_config in config_list:
        default_config['input'].update(temp_config['input'])
        default_config['output'].update(temp_config['output'])

    pprint(default_config)

    # 如果只是测试就打印配置
    if args.test_config:
        return None
    else:
        return default_config


def init_config():
    source = os.path.join(BASE_DIR, DEFAULT_CONFIG)
    shutil.copy(source, DEFAULT_CONFIG)
