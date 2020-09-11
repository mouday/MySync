# -*- coding: utf-8 -*-

from importlib import import_module


def get_method(name):
    """获取方法 name格式： 包名.文件名@方法名"""
    module_name, method_name = name.split("@")

    input_data = import_module(module_name)
    if hasattr(input_data, method_name):
        return getattr(input_data, method_name)
    else:
        raise Exception(f"not found method: {name}")
