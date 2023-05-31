def get_demerit_points(driving_speed, speed_limit, holiday_period = False):
    """
    Function works out the demerit (penalty) points for a driving speed in a particular speed limited zone.
    driving_speed: Int or Float. The speed the driver was travelling at (assumed to be positive).
    speed_limit: Int. The speed limit of the zone (assumed to be positive).
    holiday_period: Boolean. Whether or not the driver was speeding during a holiday period. default = False.
    Returns a Tuple of (Mandatory penalty, penalty points).

    About Mandatory Penalty:
    Mandatory penalty is True if the driving speed exceeds the speed limit during a holiday period by more than 4km/h.
    Mandatory penalty is False if the driving speed does not exceed the speed limit during a holiday period by more than 4km/h.
    Mandatory penalty is True if the driving speed exceeds the speed limit outside a holiday period by more than 5km/h.
    Mandatory penalty is False if the driving speed does not exceed the speed limit outside a holiday period by more than 5km/h.

    About Penalty Points:
    If the driving speed is less than the speed limit, the function will return 0 penalty points in the tuple.  Mandatory penalty will be False.
    If the driving speed is the same as the speed limit, the function will return 0 penalty points in the tuple. Mandatory penalty will be False.
    If the driving speed exceeds the speed limit by no more than 10km/h when driving during the holiday period, the function will return 10 penalty points in the tuple. The mandatory penalty is specified in the mandatory penalty section above.
    If the driving speed exceeds the speed limit by more than 10km/h but not more than 20km/h, the function will return 20 penalty points in the tuple.  Mandatory penalty will be True.
    If the driving speed exceeds the speed limit by more than 20km/h but not more than 30km/h, the function will return 30 penalty points in the tuple. Mandatory penalty will be True.
    If the driving speed exceeds the speed limit by more than 30km/h, the function will return 50 penalty points in the tuple. Mandatory penalty will be True.

    This function does not verify the inputs, that will be done in the web side of the application.
    Penalty point values are not real values, they are just for the purposes of this exercise.
    """

    speed_diff = driving_speed - speed_limit

    if driving_speed <= speed_limit:
        return False, 0

    if holiday_period:
        if speed_diff <= 4:
            return False, 10
        elif speed_diff <= 10:
            return True, 10
        elif speed_diff <= 20:
            return True, 20
        elif speed_diff <= 30:
            return True, 30
        else:
            return True, 50
    else:
        if speed_diff <= 5:
            return False, 10
        elif speed_diff <= 10:
            return True, 10
        elif speed_diff <= 20:
            return True, 20
        elif speed_diff <= 30:
            return True, 30
        else:
            return True, 50