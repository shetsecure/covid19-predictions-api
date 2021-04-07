from flask import Flask, jsonify, request
from predict import get_predictions

app = Flask(__name__)

@app.route('/test')
def test():
    return jsonify(get_predictions('france', 'confirmed', 3))

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Predicting new cases of coronavirus.</h1>
                <p>An API for predecting new cases/deaths for a given country in the next few days.</p>

            <h2> Minimal docs </h2>
            <p> To get predictions of confirmed cases go to /api/v1/predict/confirmed </p>
            <p> To get predictions of death cases go to /api/v1/predict/deaths </p>

            <p> params are country (required) and days (optional) </p>
            <p> if days param is not set, then we'll return a prediction for the following day </p>

            <h3> Example </h3>
            <h4>Confirmed cases:</h4>
                <p>/api/v1/predict/confirmed?country=france</p>
                <p>or </p>
                <p>/api/v1/predict/confirmed?country=fr&days=3</p>

            </h4>Deaths:</h4>
                <p>/api/v1/predict/deaths?country=france</p>
                <p>or </p>
                <p>/api/v1/predict/deaths?country=FR&days=3</p>

'''

@app.route('/api/v1/predict/confirmed', methods=['GET'])
def forecast_confirmed():
    if 'country' in request.args:
        country = request.args['country']
    else:
        return "Error: No country name field provided. Please specify a country name."

    if 'days' in request.args:
        days = int(request.args['days'])
    else:
        days = 1

    try:
        p = get_predictions(country, 'confirmed', days)
    except ValueError as e:
        return str(e)

    return jsonify(p)

@app.route('/api/v1/predict/deaths', methods=['GET'])
def forecast_deaths():
    if 'country' in request.args:
        country = request.args['country']
    else:
        return "Error: No country name field provided. Please specify a country name."

    if 'days' in request.args:
        days = int(request.args['days'])
    else:
        days = 1

    try:
        p = get_predictions(country, 'deaths', days)
    except ValueError as e:
        return str(e)

    return jsonify(p)


if __name__ == '__main__':
    app.run(threaded=True)