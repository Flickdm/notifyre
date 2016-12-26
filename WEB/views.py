from flask import render_template, request, Blueprint
from HW import get_hardware

hw = get_hardware("gpio")
main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form)
        hw.output_devices["power"].toggle()

    return render_template('index.html')
