import os
from flask import Flask, render_template, request, flash
from get_demerit_points import get_demerit_points

SUCCESS_MSG = 'success'
WARNING_MSG = 'warning'
KEY_SIZE = 24
HTML_TEMPLATE = 'flask_app.html'

# Create Flask instance and set the session key
app = Flask(__name__)
app.secret_key = os.urandom(KEY_SIZE)
        
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home page handler
    """

    print(f'DEBUG. Function received http method type: {request.method}')

    if request.method == 'POST':
        # Gather data that was submitted
        driving_speed = request.form.get('driving_speed')
        speed_limit = request.form.get('speed_limit')
        holiday_period = request.form.get('holiday_period')
        print(f'{holiday_period=}')

        if driving_speed != '' and speed_limit != '':
            # Data has been submitted, process it
            if driving_speed.replace('.','').isdigit() and speed_limit.isdigit():
                # Data is valid
                driving_speed = float(driving_speed)
                speed_limit = int(speed_limit)
                holiday_period = True if holiday_period == 'on' else False
                print(f'{holiday_period=}')

                mandatory_penalty, penalty_points = get_demerit_points(driving_speed, speed_limit, holiday_period)
                print(f'{mandatory_penalty=}')
                print(f'{penalty_points=}')

                if mandatory_penalty:
                    flash(f'Mandatory penalty of {penalty_points} points.', WARNING_MSG)
                else:
                    flash(f'Optional penalty of {penalty_points} points.', SUCCESS_MSG)
            else:
                # Data is invalid
                flash('Invalid data entered. Please try again.', WARNING_MSG)
        else:
            # Data is invalid
            flash('Invalid data entered. Please try again.', WARNING_MSG)

    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator')

if __name__ == '__main__':
    app.run()