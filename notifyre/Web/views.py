from flask import render_template, request, flash
from flask import Blueprint, redirect, session
from flask_security import login_required
from notifyre import get_hardware

import random

hw = get_hardware("gpio")
main = Blueprint('main', __name__)


@main.route('/', methods=["GET"])
@main.route('/index', methods=["GET"])
#@main.route('/index.html')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return redirect('/dashboard')

@main.route('/dashboard', methods=["GET"])
@main.route('/dashboard.html', methods=["GET"])
#@login_required
def dashboard():
    output_devices = {}
    for device in hw.output_devices:
            output_devices[device] = hw.output_devices.get(device).get_status()

    led_strips = {}
    for device in hw.led_strips:
        led_strips["strip"] = {
                "name": device,
                "status": hw.led_strips.get(device).get_status(),
                "pulseStatus": hw.led_strips.get(device).get_pulse_status(),
                "colors": hw.led_strips.get(device).get_defined_colors()
                }

    return render_template(
        'dashboard.html',
        output_devices=output_devices,
        led_strips=led_strips
        )

@main.route('/manage', methods=["GET"])
#@login_required
def manage_hardware():
    return render_template('manage.html')

@main.route('/settings', methods=["GET"])
#@login_required
def manage():
    return render_template('settings.html')

@main.route('/login', methods=["POST"])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('INCORRECT LOGIN')

    return index()

@main.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@main.route('/output_devices/', methods=["POST"])
def output_devices():

    device = request.form.get('device')
    if device in hw.output_devices:
        hw.output_devices.get(device).toggle()

    return redirect('/dashboard')

@main.route('/led_strips/', methods=["POST"])
def led_strips():

    device = request.form.get('device')
    device_state = request.form.get(device)
    pulse_state = request.form.get('pulse')
    color = request.form.get('color')

    # For some reason it will often send the leds state twice when it shouldn't
    # be sent at all after color choice has been made this should check if it
    # was a malformed response the first one won't have a leds field which is
    # fine but the second one will have two so lets ignore that one
    malformed_response = len(request.form.getlist('leds'))

    print(request.form)

    if device in hw.led_strips:
        if color == 'none' and device_state == 'on':
            #color = hw.led_strips.get(device).get_prev_color()
            color = 'blue'
            hw.led_strips.get(device).set_color_word(color)
        if device_state == 'off' and malformed_response != 2:
            color = 'none'

        hw.led_strips.get(device).set_color_word(color)

        if color != 'none' and pulse_state == 'on':
            hw.led_strips.get(device).pulse()

    return redirect('/dashboard')
