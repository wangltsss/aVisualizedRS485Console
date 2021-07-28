from flask import Flask, request, redirect

from Util.subpages import ConfigManager, ErrManager, ManPage, TimeOutManager, to_err

from time import sleep

from functools import wraps

app = Flask(__name__)


form: dict


def if_filled_form(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        global form
        try:
            a = form["id"]
        except Exception:
            return redirect('/board')
        return f(*args, **kwargs)
    return decorated


@app.route('/board/', methods=["POST", "GET"])
def board():

    global form
    manager = ConfigManager()

    if request.method == "GET":
        ports = manager.get_all_ports()
        return manager.show_page(ports)

    form = manager.get_form()
    try:
        return manager.redirect()
    except Exception as e:
        print(e)
        return to_err()


@app.route('/man/', methods=["POST", "GET"])
@if_filled_form
def man():
    global form
    lcl_form = form
    sleep(0.1)
    try:
        manager = ManPage(lcl_form["mode"], lcl_form["id"], lcl_form["type"], lcl_form["version"])
    except NameError:
        return to_err()

    manager.connect(lcl_form["port"])

    if request.method == "GET":
        return manager.show_page()

    manager.alter_tunnl_status()

    manager.port_man.close(manager.port_man.ser)
    return manager.redirect()


@app.route('/conn_err/', methods=["GET"])
def conn_err():
    manager = ErrManager()
    return manager.show_page()


@app.route('/time_out/', methods=["GET"])
def time_out():
    manager = TimeOutManager()
    return manager.show_page()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
