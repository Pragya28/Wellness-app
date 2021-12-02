def calculate_bmi(height, weight):
    bmi = weight/(height ** 2) * 10000
    return round(bmi, 2)


# Formula source: http://www.shapesense.com/fitness-exercise/calculators/activity-based-calorie-burn-calculator.aspx
def calculate_bmr(height, weight, age, gender):
    if gender == "male":
        bmr = 13.75 * weight + 5 * height - 6.76 * age + 66
    else:
        bmr = 9.56 * weight + 1.85 * height - 4.68 * age + 655
    return bmr
 

def calculate_calories_burned(met, bmr, time):
    cal = met * time * bmr/24 
    return round(cal)


def total_calories(data):
    return sum([x.calorie for x in data])


def calculate_sleeping_time(sleep_time, wakeup_time):
    sleep_time = list(map(int, sleep_time.split(":")))
    wakeup_time = list((map(int, wakeup_time.split(":"))))
    mins = wakeup_time[1] - sleep_time[1]
    if mins < 0:
        mins += 60
        wakeup_time[0] -= 1
    hrs = wakeup_time[0] - sleep_time[0]
    if hrs < 0:
        hrs += 24
    return {
        'hrs' : hrs,
        'mins' : mins,
        'total' : hrs*60+mins
    }

