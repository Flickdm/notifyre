from flask import render_template, Blueprint
from HW import get_hardware

hw = get_hardware("gpio")
main = Blueprint('main', __name__)

@main.route('/')
def index():
    hw.output_devices["power"].toggle()
    return "hello world!"#render_template('index.html')
