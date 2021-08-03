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
        self.coder = CodeParser('', '')
        self.url = "/board"
        self.template = 'config.html'

    def connect(self, port):
        self.port_man.set_port(port)
        self.port_man.create_connection(self.port_man.get_port())

    def show_page(self, ports):
        return render_template(self.template, ports=ports)

    def redirect(self):
        return redirect(url_for("man"))

    def get_all_ports(self):
        return self.port_man.list_ports()

    def consult_metadata(self):
        self.port_man.send_data(self.coder.encode_83())
        return self.coder.decode_83(self.port_man.read_data())

    def get_form(self):
        port = request.form.get("port-select")
        return port

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

    def update_status(self):
        if self.port_man.send_data(self.coder.encode_85()):
            try:
                sleep(0.1)
                res = self.coder.decode_85(self.port_man.read_data())
                counter = 0
                while (not res["id"]) and counter <= 10:
                    self.port_man.send_data(self.coder.encode_85())
                    res = self.coder.decode_85(self.port_man.read_data())
                    counter += 1
                if counter >= 10:
                    raise ConnectionError
                self.status = res["tunnl_status"]
            except Exception as e:
                print(e)
                to_err()

    def show_page(self):
        sleep(0.1)
        self.update_status()
        try:
            a = self.status
        except AttributeError:
            self.update_status()
        self.port_man.close(self.port_man.ser)
        return render_template(self.template, nums=self.status, mode=self.mode, bid=self.id)

    def connect(self, port):
        self.port_man.set_port(port)
        self.port_man.create_connection(self.port_man.get_port())

    def get_form(self):
        res = []
        if self.mode.lower() == "e1":
            for i in range(1, 11):
                res += request.form.getlist("g{}-tunnel".format(i))
        elif self.mode.lower() == "e2":
            for i in range(1, 6):
                res += request.form.getlist("g{}-tunnel".format(i))
        elif self.mode.lower() == "e3":
            for i in range(1, 3):
                res += request.form.getlist("g{}-tunnel".format(i))
        elif self.mode.lower() == "e4":
            for i in range(1, 2):
                res += request.form.getlist("g{}-tunnel".format(i))
        if res:
            return res[0]
        else:
            return False

    def form_parser(self, res):
        if not res:
            return []
        new_ls = self.status
        res = res[1:].split('t')
        grp = int(res[0]) - 1
        tnl = int(res[1]) - 1
        for i in range(len(new_ls[grp])):
            if i != tnl:
                new_ls[grp][i] = 0
        if self.status[grp][tnl]:
            new_ls[grp][tnl] = 0
        else:
            new_ls[grp][tnl] = 1
        return new_ls

    def alter_tunnl_status(self):
        self.update_status()
        before = self.status
        new_ls = self.form_parser(self.get_form())
        if new_ls:
            self.port_man.send_data(self.coder.encode_82(new_ls))
            self.update_status()
            if before == self.status:
                self.port_man.send_data(self.coder.encode_82(new_ls))

    def redirect(self):
        return redirect(url_for(self.url))

    def alter_group_mode(self):
        mode = request.form.get('group-mode-edit')
        if not mode:
            return False
        if self.port_man.send_data(self.coder.encode_87(mode.upper())):
            self.port_man.read_data()
            self.mode = mode.upper()
            self.coder.mode = mode.upper()
            return True
        else:
            return False

    def alter_board_id(self):
        bid = request.form.get("board-id-edit")
        if not bid:
            return False
        if self.port_man.send_data(self.coder.encode_86(bid)):
            self.port_man.read_data()
            self.id = bid
            self.coder.id = bid
            return True
        else:
            return False

















































