from flask import render_template, request, Blueprint, redirect
from HW import get_hardware

hw = get_hardware("gpio")
main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@main.route('/index.html')
def index():
    output_devices = {}
    for device in hw.output_devices:
            output_devices[device] = hw.output_devices.get(device).get_status()

    led_strips = {}
    for device in hw.led_strips:
        led_strips["strip"] = {
                "name": device,
                "status": hw.led_strips.get(device).get_status(),
                "colors": hw.led_strips.get(device).get_defined_colors()
                }

    return render_template(
        'index.html',
        output_devices=output_devices,
        led_strips=led_strips
        )

@main.route('/add')
def add_hardware():
    return "add hardware"

@main.route('/output_devices/', methods=["post"])
def output_devices():

    device = request.form.get('device')
    if device in hw.output_devices:
        hw.output_devices.get(device).toggle()

    return redirect('/')

@main.route('/led_strips/', methods=["post"])
def led_strips():

    print(request.form)

    device = request.form.get('device')
    device_state = request.form.get(device)
    #print(device_state)
    color = request.form.get('color')

    if device in hw.led_strips:
        if device_state == "on":
            hw.led_strips.get(device).set_color_word(color)
        elif device_state == "off":
            hw.led_strips.get(device).set_color_word("none")




    return redirect('/')
