# -*- coding: utf-8 -*-
import os

SYNC_FILE_DIR = "sync_point"


class SyncUtil(object):
    """同步点文件记录"""

    def __init__(self, sync_file, sync_type):
        if not os.path.exists(SYNC_FILE_DIR):
            os.mkdir(SYNC_FILE_DIR)

        self.sync_file = os.path.join(SYNC_FILE_DIR, sync_file)
        self.sync_type = sync_type

    def read_sync_id(self, read_sync_point=True):
        if not read_sync_point:
            return self.convert_type(None)

        sync_point = None

        if os.path.exists(self.sync_file):
            with open(self.sync_file) as f:
                sync_point = f.read()

        return self.convert_type(sync_point)

    def write_sync_id(self, sync_id):
        with open(self.sync_file, "w") as f:
            return f.write(f"{sync_id}")

    def convert_type(self, value):
        if self.sync_type == 'int':
            if not value:
                return 0
            else:
                return int(value)

        elif self.sync_type == 'str':
            if not value:
                return ""
            else:
                return value
        else:
            raise Exception("only support int or str")
