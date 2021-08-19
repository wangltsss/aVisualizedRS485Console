from flask import Flask, request, redirect

from Util.subpages import ConfigManager, ErrManager, ManPage, TimeOutManager, to_err

from functools import wraps

from datetime import datetime

app = Flask(__name__)


form: dict
conn_alive: dict


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
    while not manager.check_conn_alive():
        manager.connect(form['port'])
    tic = datetime.now()
    lwr_bounds = request.form.get('scan-lwr-bounds')
    upr_bounds = request.form.get('scan-upr-bounds')
    conn_alive = manager.test_alive(lwr_bounds, upr_bounds)
    toc = datetime.now()
    print("扫描{}个ID共花费了{}秒。".format(int(upr_bounds)-int(lwr_bounds)+1, (toc-tic).total_seconds()))
    try:
        try:
            form['id'] = conn_alive['sgn'][0]['id']
            form['mode'] = conn_alive['sgn'][0]['devGM']
            form['version'] = conn_alive['sgn'][0]['ver']
            form['type'] = conn_alive['sgn'][0]['cate']
        except IndexError:
            try:
                form['id'] = conn_alive['pwr'][0]['id']
                form['mode'] = conn_alive['pwr'][0]['devGM']
                form['version'] = conn_alive['pwr'][0]['ver']
                form['type'] = conn_alive['pwr'][0]['cate']
            except IndexError:
                return to_err()
            except Exception as e:
                print(e)
                return to_err()
        try:
            return manager.redirect()
        except Exception as e:
            print(e)
            return to_err()
    except ValueError:
        return to_err()
    except Exception as e:
        print(e)
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
    except Exception as e:
        print(e)
        return to_err()

    manager.connect(lcl_form["port"])

    manager.conn_alive = conn_alive

    if request.method == "GET":
        try:
            return manager.show_page()
        except ValueError:
            return to_err()
        except Exception as e:
            print(e)
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
