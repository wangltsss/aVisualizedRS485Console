import json


class Parser(object):

    def json_reader(self, addr):
        with open(addr, "r") as file_r:
            return json.load(file_r)

    def json_writer(self, addr, content):
        with open(addr, "w") as file_w:
            json.dump(content, file_w)

