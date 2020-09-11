# -*- coding: utf-8 -*-
import os

import yaml
import shutil

yaml.warnings({'YAMLLoadWarning': False})

"""
配置逐级覆盖
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
    config_file = None

    if args.table:
        config_file = f"{args.table}_{BASE_CONFIG}"
        config_file = os.path.join(CONFIG_DIR, config_file)

    if args.config:
        config_file = args.config

    if not config_file:
        raise Exception("not config_file")

    if not os.path.exists(config_file):
        raise Exception(f"config file not found {config_file}")

    # 读取基本配置
    # config = json.load(open(os.path.join(BASE_DIR, DEFAULT_CONFIG)))
    config = yaml.load(open(os.path.join(BASE_DIR, DEFAULT_CONFIG)))

    # 加载用户自定义基本配置
    base_config_file = os.path.join(CONFIG_DIR, BASE_CONFIG)
    if os.path.exists(base_config_file):
        # base_config = json.load(open(base_config_file))
        base_config = yaml.load(open(base_config_file))
        config['input'].update(base_config['input'])
        config['output'].update(base_config['output'])

    # 加载用户自定义配置
    # custom_config = json.load(open(config_file))
    custom_config = yaml.load(open(config_file))
    config['input'].update(custom_config['input'])
    config['output'].update(custom_config['output'])

    return config


def init_config():
    source = os.path.join(BASE_DIR, DEFAULT_CONFIG)
    shutil.copy(source, DEFAULT_CONFIG)
