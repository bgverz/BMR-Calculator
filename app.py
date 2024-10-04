from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

calendar_data = {}

def calculate_bmr(weight, height_feet, height_inches, age, gender):
    height_cm = (height_feet * 30.48) + (height_inches * 2.54)
    weight_kg = weight * 0.453592
    if gender == 'male':
        return 88.362 + (13.397 * weight_kg) + (4.799 * height_cm) - (5.677 * age)
    elif gender == 'female':
        return 447.593 + (9.247 * weight_kg) + (3.098 * height_cm) - (4.330 * age)

def calculate_caloric_needs(bmr, activity_level):
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'super_active': 1.9
    }
    return bmr * activity_multipliers.get(activity_level, 1.2)

def calculate_weight_change_calories(caloric_needs, change_type, amount):
    calorie_change = amount * 3500
    if change_type == 'gain':
        return caloric_needs + calorie_change / 7
    elif change_type == 'lose':
        return caloric_needs - calorie_change / 7

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    weight = float(request.form['weight'])
    height_feet = float(request.form['height_feet'])
    height_inches = float(request.form['height_inches'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity_level = request.form['activity_level']

    bmr = calculate_bmr(weight, height_feet, height_inches, age, gender)
    caloric_needs = calculate_caloric_needs(bmr, activity_level)

    caloric_needs_gain_05 = calculate_weight_change_calories(caloric_needs, 'gain', 0.5)
    caloric_needs_gain_1 = calculate_weight_change_calories(caloric_needs, 'gain', 1)
    caloric_needs_gain_15 = calculate_weight_change_calories(caloric_needs, 'gain', 1.5)

    caloric_needs_lose_05 = calculate_weight_change_calories(caloric_needs, 'lose', 0.5)
    caloric_needs_lose_1 = calculate_weight_change_calories(caloric_needs, 'lose', 1)
    caloric_needs_lose_15 = calculate_weight_change_calories(caloric_needs, 'lose', 1.5)

    return render_template('result.html', bmr=bmr, caloric_needs=caloric_needs,
                           caloric_needs_gain_05=caloric_needs_gain_05,
                           caloric_needs_gain_1=caloric_needs_gain_1,
                           caloric_needs_gain_15=caloric_needs_gain_15,
                           caloric_needs_lose_05=caloric_needs_lose_05,
                           caloric_needs_lose_1=caloric_needs_lose_1,
                           caloric_needs_lose_15=caloric_needs_lose_15)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/save_calendar_data', methods=['POST'])
def save_calendar_data():
    date = request.form['date']
    meals = request.form.getlist('meals[]')
    total_calories = sum(int(meal) for meal in meals)
    calendar_data[date] = total_calories
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
