import numpy as np

def calculate_trend(datapoints):
    if len(datapoints) < 3:
        return None

    npdata = np.array(datapoints)

    x = np.array([0, 1, 2])
    y = npdata

    # Calculate the grade (1. derivative) of the Approximation
    coefficients = np.polyfit(x, y, 1)
    slope = coefficients[0]
    if datapoints[-1] != 0:  # Prevent ZeroDivisionError
        percent_between_datapoints = ((datapoints[-2] - datapoints[-1]) / datapoints[-1]) * 100
    else:
        percent_between_datapoints = 100

    if slope > 0.6 and percent_between_datapoints < 25:
        return_val = "increasing"
    elif slope < -0.6 and percent_between_datapoints < 25:
        return_val = "decreasing"
    else:
        return_val = "flat"

    return return_val