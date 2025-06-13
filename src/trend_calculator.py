import numpy as np

def calculate_trend(datapoints):
    # Überprüfe, ob genau drei Werte vorhanden sind
    if len(datapoints) < 3:
        return None
    # Konvertiere die Eingabeliste in ein NumPy-Array
    npdata = np.array(datapoints)

    # Berechne die Steigung (1. Ableitung) der linearen Approximation
    x = np.array([0, 1, 2])
    y = npdata

    # Führe eine lineare Regression durch
    coefficients = np.polyfit(x, y, 1)
    slope = coefficients[0]
    if datapoints[-1] != 0:  # Prevent ZeroDivisionError
        percent_between_datapoints = ((datapoints[-2] - datapoints[-1]) / datapoints[-1]) * 100
    else:
        percent_between_datapoints = 100

    if slope > 0.5 and percent_between_datapoints < 30:
        return_val = "increasing"
    elif slope < -0.5 and percent_between_datapoints < 30:
        return_val = "decreasing"
    else:
        return_val = "flat"

    return return_val