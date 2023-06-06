import os
from flask import Flask, render_template, request, flash, redirect, url_for
from get_demerit_points import get_demerit_points

# Constants
SUCCESS_MSG = 'success' # Bootstrap alert types
WARNING_MSG = 'warning'
HTML_TEMPLATE = 'flask_app.html'
ERROR_TEMPLATE = '404_page.html'

# Create Flask instance and set the session key
app = Flask(__name__)

# Error handling for invalid URLs
@app.errorhandler(404)
def page_not_found(e):
    """
    Error handler for invalid URLs
    Returns the 404.html template
    After 5 seconds the user is redirected to the home page
    """
    return render_template(ERROR_TEMPLATE, title='404'), 404

# Main page
@app.route('/', methods=['GET','POST'])
def home():
    """
    Home page handler, uses the home.html template
    Logic is from the get_demerit_points.py file
    """

    if request.method == 'POST':
        # Gather data that was submitted
        driving_speed = request.form.get('driving_speed')
        speed_limit = request.form.get('speed_limit')
        holiday_period = request.form.get('holiday_period')

        if driving_speed != '' and speed_limit != '':
            # Data has been submitted, process it
            if driving_speed.replace('.','').isdigit() and speed_limit.isdigit():
                # Data is valid convert it to the correct type for processing
                driving_speed = float(driving_speed)
                speed_limit = int(speed_limit)
                holiday_period = True if holiday_period == 'on' else False

                # Using the function from get_demerit_points.py, get the penalty type and the penalty points
                mandatory_penalty, penalty_points = get_demerit_points(driving_speed, speed_limit, holiday_period)

                # If the driving speed is a float, report it as a float, if it is an int, report it as an int
                if driving_speed.is_integer(): driving_speed = int(driving_speed)
                else: driving_speed = float(driving_speed)

                # Penalty logic
                if mandatory_penalty == True:
                    flash(f'The mandatory penalty for driving {driving_speed}km/h in a {speed_limit}km/h zone is {penalty_points} points.', WARNING_MSG)
                    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, speed_limit=speed_limit, holiday_period=holiday_period)
                
                elif mandatory_penalty == False and penalty_points > 0:
                    flash(f'The discretional penalty for driving {driving_speed}km/h in a {speed_limit}km/h zone is {penalty_points} points.', WARNING_MSG)
                    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, speed_limit=speed_limit, holiday_period=holiday_period)
                
                elif penalty_points == 0:
                    flash(f'You are not required to pay a penalty for driving {driving_speed}km/h in a {speed_limit}km/h zone.', SUCCESS_MSG)
                    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, speed_limit=speed_limit, holiday_period=holiday_period)
                
        else: # Invalid Data
            if driving_speed == '' and speed_limit != '': # Both fields are empty
                flash('Please enter a driving speed.', WARNING_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', speed_limit=speed_limit, holiday_period=holiday_period)
            if speed_limit == '' and driving_speed != '': # Driving speed is empty
                flash('Please enter a speed limit.', WARNING_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', driving_speed=driving_speed, holiday_period=holiday_period)
            if driving_speed == '' and speed_limit == '': # Both fields are empty
                flash('Please enter a driving speed and a speed limit.', WARNING_MSG)
                return render_template(HTML_TEMPLATE, title='Demerit Points Calculator', holiday_period=holiday_period)

    # No data has been submitted, render the template, this happens when the user first visits the page
    return render_template(HTML_TEMPLATE, title='Demerit Points Calculator')

# Run the app
if __name__ == '__main__':
    app.run()