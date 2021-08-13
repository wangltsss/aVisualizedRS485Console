from flask import Flask, request, redirect

from Util.subpages import ConfigManager, ErrManager, ManPage, TimeOutManager, to_err

from functools import wraps

app = Flask(__name__)


form: dict
conn_alive: list


def if_filled_form(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        global form
        try:
            a = form["id"]
        except Exception:
            return redirect('/')
        return f(*args, **kwargs)
    return decorated


@app.route('/', methods=["POST", "GET"])
def board():

    global form
    global conn_alive
    manager = ConfigManager()

    if request.method == "GET":
        ports = manager.get_all_ports()
        return manager.show_page(ports)

    form = manager.get_form()
    manager.connect(form['port'])
    conn_alive = manager.test_alive()
    try:
        form['id'] = conn_alive[0]
        res = manager.consult_metadata(form['id'])
        form['mode'] = res['devGM']
        form['version'] = res['ver']
        form['type'] = res['cate']
        try:
            return manager.redirect()
        except Exception as e:
            print(e)
            return to_err()
    except ValueError:
        return to_err()


@app.route('/man/', methods=["POST", "GET"])
@if_filled_form
def man():
    global form
    global conn_alive
    lcl_form = form
    try:
        manager = ManPage(lcl_form["mode"], lcl_form["id"], lcl_form["type"], lcl_form["version"])
    except NameError:
        return to_err()

    manager.connect(lcl_form["port"])

    if not conn_alive:
        conn_alive = manager.test_alive()
    else:
        manager.conn_alive = conn_alive

    if request.method == "GET":
        try:
            return manager.show_page()
        except ValueError:
            return to_err()

    manager.alter_tunnl_status()

    if manager.alter_group_mode():
        lcl_form['mode'] = manager.mode

    if manager.alter_board_id():
        lcl_form['id'] = manager.id

    if not manager.change_board_focus():
        if manager.change_board_focus():
            form = {'mode': manager.mode,
                    'id': manager.id,
                    'type': manager.cate,
                    'version': manager.version,
                    'port': lcl_form['port']}
    else:
        form = {'mode': manager.mode,
                'id': manager.id,
                'type': manager.cate,
                'version': manager.version,
                'port': lcl_form['port']}

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
    app.run()
