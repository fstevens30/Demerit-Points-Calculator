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
        print(f'{driving_speed=}')
        print(f'{speed_limit=}')
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

                # If the driving speed is a float, report it as a float, if it is an int, report it as an int
                if driving_speed.is_integer():
                    driving_speed = int(driving_speed)
                else:
                    driving_speed = float(driving_speed)


                if mandatory_penalty == True:
                    flash(f'The mandatory penalty for driving {driving_speed}km/h in a {speed_limit}km/h zone is {penalty_points} points.', WARNING_MSG)
                    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, speed_limit=speed_limit, holiday_period=holiday_period)
                if mandatory_penalty == False and penalty_points > 0:
                    flash(f'The discretional penalty for driving {driving_speed}km/h in a {speed_limit}km/h zone is {penalty_points} points.', WARNING_MSG)
                    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, speed_limit=speed_limit, holiday_period=holiday_period)
                if penalty_points == 0:
                    flash(f'You are not required to pay a penalty for driving {driving_speed}km/h in a {speed_limit}km/h zone.', SUCCESS_MSG)
                    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, speed_limit=speed_limit, holiday_period=holiday_period)
            else:
                # Data is invalid because it contains non-numeric characters
                flash('Invalid data entered. Please try again. Test 1', WARNING_MSG)
        else:
            # Data is invalid because it is empty
            if driving_speed == '' and speed_limit != '':
                flash('Please enter a driving speed.', WARNING_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', speed_limit=speed_limit, holiday_period=holiday_period)
            if speed_limit == '' and driving_speed != '':
                flash('Please enter a speed limit.', WARNING_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, holiday_period=holiday_period)
            if driving_speed == '' and speed_limit == '':
                flash('Please enter a driving speed and a speed limit.', WARNING_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', holiday_period=holiday_period)

    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator')

if __name__ == '__main__':
    app.run()