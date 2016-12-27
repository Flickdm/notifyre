from flask import render_template, request, Blueprint, redirect
from HW import get_hardware

hw = get_hardware("gpio")
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@main.route('/index.html')
def index():
    devices = {}
    for device in hw.output_devices:
            devices[device] = hw.output_devices.get(device).get_status()

    return render_template('index.html', devices=devices)

@main.route('/add')
def add_hardware():
    return "add hardware"

@main.route('/devices/', methods=["post"])
def devices():
    
    for device in request.form:
        if device in hw.output_devices:
            hw.output_devices.get(device).toggle()

    return redirect('/')
