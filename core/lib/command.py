import os


class Command(object):
    name: str
    key: str
    command: str
    pid: str

    path: str
    file_name = "pid"

    def run(self):

        pass

    def write_pid(self, pid: str):
        filename = self.path + self.file_name
        if not os.path.isfile(filename):  # 无文件时创建
            with open(filename, mode="w", encoding="utf-8") as fd:
                fd.write(pid)


