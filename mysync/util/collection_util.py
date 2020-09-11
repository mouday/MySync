# -*- coding: utf-8 -*-


class Collection(object):
    """列表集合操作"""

    def __init__(self, iterator):
        self.iterator = iterator

    def max(self, key, initial_value=0):
        """获取字典值中最大值"""
        max_value = initial_value

        for row in self.iterator:
            if row[key] > max_value:
                max_value = row[key]

        return max_value

