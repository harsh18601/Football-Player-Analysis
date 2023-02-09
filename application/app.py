from flask import Flask, render_template, request
import pickle
import sklearn
import math
app = Flask(__name__, template_folder="template")

def train_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

def encode_to_cat(value, value_type):
    output = 0
    if value_type == "age":
        age_list = [(1, [0, 1, 2, 3, 4]), (2, [5, 6, 7]), (3, [8, 9, 10]), (4, [11, 12, 13, 14]), (5, [15, 16]), (6, [17, 18, 19, 20, 21])]
        for age in age_list:
            if value in age[1]:
                output = age[0]
    elif value_type == "region":
        region_list = [(1.0, [22, 60]), (2.0, [1, 4, 5, 8, 10, 16, 17, 18, 19, 22, 23, 24, 25, 26, 28, 29, 30, 32, 38, 41, 42, 43, 44, 45, 46, 48, 49, 51, 52, 53, 60]), (3.0, [1, 7, 9, 11, 12, 13, 20, 33, 55, 57, 58, 59]), (4.0, [0, 2, 3, 6, 10, 14, 15, 21, 27, 31, 34, 35, 36, 37, 39, 40, 47, 50, 54, 56, 57])]
        for region in region_list:
            if value in region[1]:
                output = region[0]
    elif value_type == "position":
        position_list = [(1, [0, 2, 8, 9, 11, 12]), (2, [3, 4, 7, 10]), (3, [1, 6, 9]), (4, [5])]
        for position in position_list:
            if value in position[1]:
                output = position[0]
    elif value_type == "market_value":
        market_value_list = [(0.05, [0]), (0.1, [1]), (0.25, [2]), (0.5, [3]), (0.65, [4]), (0.75, [5]), (1.0, [6]), (1.25, [7]), (1.5, [8]), (1.75, [9]), (2.0, [10]), (2.5, [11]), (3.0, [12]), (3.5, [13]), (4.0, [14]), (4.5, [15]), (5.0, [16]), (5.5, [17]), (6.0, [18]), (7.0, [19]), (7.5, [20]), (8.0, [21]), (9.0, [22]), (10.0, [23]), (11.0, [24]), (12.0, [25]), (13.0, [26]), (14.0, [27]), (15.0, [28]), (16.0, [29]), (17.0, [30]), (18.0, [31]), (20.0, [32]), (21.0, [33]), (22.0, [34]), (24.0, [35]), (25.0, [36]), (28.0, [37]), (30.0, [38]), (32.0, [39]), (35.0, [40]), (38.0, [41]), (40.0, [42]), (45.0, [43]), (50.0, [44]), (60.0, [45]), (65.0, [46]), (75.0, [47])]
        for market_value in market_value_list:
            if value in market_value[1]:
                output = market_value[0]
    return output

@app.route("/", methods=["GET", "POST"])
def index():
  return render_template("index.html")

@app.route("/data", methods=["POST"])
def data():
    position_cat2 = int(request.form["position"])
    position_cat = encode_to_cat(position_cat2, "position")

    age_cat2 = int(request.form["age"])
    age_cat = encode_to_cat(age_cat2, "age")

    region2 = int(request.form["nationality"])
    region = encode_to_cat(region2, "region")

    page_views = int(request.form["page_views"])
    fpl_value = float(request.form["fpl_value"])
    fpl_points = int(request.form["fpl_points"])
    fpl_sel = float(request.form["fpl_sel"])
    club_id = int(request.form["club_id"])
    big_club = int(request.form["big_club"])
    new_signing = int(request.form["new_signing"])
    new_foreign = int(request.form["new_foreign"])

    to_pred_for = [[position_cat, page_views, fpl_value, fpl_sel,
    fpl_points, region, new_foreign, age_cat, club_id, big_club,
    new_signing, age_cat2, position_cat2, region2]]
    print(to_pred_for)
    model = train_model()
    prediction = model.predict(to_pred_for)
    print(prediction)
    market_value = encode_to_cat(math.ceil(prediction), "market_value")
    return render_template("data.html", market_value = market_value)

if __name__ == "__main__":
  app.run()
