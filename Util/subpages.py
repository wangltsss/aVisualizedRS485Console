from flask import render_template, url_for, redirect, request

from Util.port_manager import PortManager

from Util.code_parser import CodeParser

from time import sleep


def to_err():
    return redirect(url_for('conn_err'))


def to_timeout():
    return redirect(url_for('time_out'))


class Subpage:

    url: str
    template: str

    def show_page(self, *args, **kwargs):
        pass

    def redirect(self, *args, **kwargs):
        pass

    def get_form(self, *args, **kwargs):
        pass


class ConfigManager(Subpage):

    def __init__(self):
        super().__init__()
        self.port_man = PortManager()
        self.url = "/board"
        self.template = 'config.html'

    def show_page(self, ports):
        return render_template(self.template, ports=ports)

    def redirect(self):
        return redirect(url_for("man"))

    def get_all_ports(self):
        return self.port_man.list_ports()

    def get_form(self):
        port = request.form.get("port-select")
        mode = request.form.get("group-mode")
        id = request.form.get("board-id")
        version = request.form.get("version")
        type = request.form.get("board-type")
        return {"port": port, "mode": mode, "id": id, "version": version, "type": type}

    def close(self, ser):
        self.port_man.close(ser)


class ErrManager(Subpage):

    def __init__(self):
        super().__init__()
        self.url = 'conn-err'
        self.template = 'err_page.html'

    def show_page(self):
        return render_template(self.template)


class TimeOutManager(Subpage):

    def __init__(self):
        super().__init__()
        self.url = 'time_out'
        self.template = 'timeout.html'

    def show_page(self):
        return render_template(self.template)


class ManPage(Subpage):
    status: list

    def __init__(self, mode, id, cate, version):
        super().__init__()
        self.url = 'man'
        self.template = 'man.html'
        self.mode = mode
        self.id = id
        self.cate = cate
        self.version = version
        self.coder = CodeParser(self.mode, self.id)
        self.port_man = PortManager()

    def init_page(self):
        if self.port_man.send_data(self.coder.encode_85()):
            try:
                res = self.coder.decode_42(self.port_man.read_data())
                counter = 0
                while (not res["id"]) or counter >= 10:
                    self.port_man.send_data(self.coder.encode_85())
                    sleep(0.1)
                    res = self.coder.decode_42(self.port_man.read_data())
                    counter += 1
                    print("Retrying reading data... " + str(counter))
                if counter >= 10:
                    raise ConnectionError
                print("res has been assigned to")
                print(res)
                self.status = res["tunnl_status"]
            except Exception as e:
                print(e)
                to_err()

    def show_page(self):
        self.init_page()
        return render_template(self.template, nums=self.status)

    def connect(self, port):
        self.port_man.set_port(port)
        self.port_man.create_connection(self.port_man.get_port())

    def get_form(self):
        res = []
        if self.mode == "4*1":
            for i in range(1, 11):
                res.append(request.form.get("tunnl_switch_" + str(i)))
        elif self.mode == "8*1":
            for i in range(1, 6):
                res.append(request.form.get("tunnl_switch_" + str(i)))
        elif self.mode == "16*1":
            for i in range(1, 3):
                res.append(request.form.get("tunnl_switch_" + str(i)))
        elif self.mode == "32*1":
            for i in range(1, 2):
                res.append(request.form.get("tunnl_switch_" + str(i)))
        return res

    def from_raw_ls(self, res):
        new_ls = []
        if self.mode == "4*1":
            for i in range(len(res)):
                new_ls.append([0] * 4)
                try:
                    idx = int(res[i][1])
                    new_ls[i].pop(idx)
                    new_ls[i].insert(idx, 1)
                except ValueError:
                    pass
        elif self.mode == "8*1":
            for i in range(len(res)):
                new_ls.append([0] * 8)
                try:
                    idx = int(res[i][1])
                    new_ls[i].pop(idx)
                    new_ls[i].insert(idx, 1)
                except ValueError:
                    pass
        elif self.mode == "16*1":
            for i in range(len(res)):
                new_ls.append([0] * 16)
                try:
                    idx = int(res[i][1])
                    new_ls[i].pop(idx)
                    new_ls[i].insert(idx, 1)
                except ValueError:
                    pass
        elif self.mode == "32*1":
            for i in range(len(res)):
                new_ls.append([0] * 32)
                try:
                    idx = int(res[i][1])
                    new_ls[i].pop(idx)
                    new_ls[i].insert(idx, 1)
                except ValueError:
                    pass
        return new_ls

    def alter_tunnl_status(self):
        new_ls = self.from_raw_ls(self.get_form())
        self.port_man.send_data(self.coder.encode_82(new_ls))

    def redirect(self):
        return redirect(url_for(self.url))




















































