from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL, ValidationError, Regexp
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap4(app)
print("\N{hot beverage}")

reg_pattern = "[1-9][:][0-5][0-9][APap][Mm]$|[0-1][0-2][:][0-5][0-9][APap][Mm]$|[1-9][APap][Mm]$"
message = "Input the time in the format given in the example"


def check_time(form, field):
    message = "input the time in the format given in the example"
    data = field.data.upper()
    print(data)
    data_list = data.split()
    print(data_list)
    if len(data_list) > 7:
        raise ValidationError(message)
    elif (data_list[-2] != "A" or data_list[-2] != "P") and data_list[-1] != "M":
        raise ValidationError(message)
    elif (len(data_list) == 4 or len(data_list) == 7) and (data_list[0] != 1 or data_list[1] > 2):
        raise ValidationError(message)
    elif (len(data_list) == 7 or len(data_list) == 6) and data_list[-4] > 5:
        raise ValidationError(message)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField("Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL(message="Invalid URL")])
    o_time = StringField("Opening Time e.g. 8AM", validators=[DataRequired(),
                                                              Regexp(regex=reg_pattern, message=message)])
    c_time = StringField("Closing Time e.g. 5:30PM", validators=[DataRequired(),
                                                                 Regexp(regex=reg_pattern, message=message)])
    coffee_rating = SelectField("Coffee Rating", choices=[
        (1, "\N{hot beverage}"),
        (2, "\N{hot beverage}\N{hot beverage}"),
        (3, "\N{hot beverage}\N{hot beverage}\N{hot beverage}"),
        (4, "\N{hot beverage}\N{hot beverage}\N{hot beverage}\N{hot beverage}"),
        (5, "\N{hot beverage}\N{hot beverage}\N{hot beverage}\N{hot beverage}\N{hot beverage}")])
    wifi_rating = SelectField(label="Wifi Strength Rating", choices=[
        ("none", "\N{Heavy Ballot X}"), (1, "\N{flexed biceps}"),
        (2, "\N{flexed biceps}\N{flexed biceps}"),
        (3, "\N{flexed biceps}\N{flexed biceps}\N{flexed biceps}"),
        (4, "\N{flexed biceps}\N{flexed biceps}\N{flexed biceps}\N{flexed biceps}"),
        (5, "\N{flexed biceps}\N{flexed biceps}\N{flexed biceps}\N{flexed biceps}\N{flexed biceps}")])
    power_rating = SelectField(label="Power Socket Availability", choices=[
        ("none", "\N{Heavy Ballot X}"),
        (1, "\N{electric plug}"),
        (2, "\N{electric plug}\N{electric plug}"),
        (3, "\N{electric plug}\N{electric plug}\N{electric plug}"),
        (4, "\N{electric plug}\N{electric plug}\N{electric plug}\N{electric plug}"),
        (5, "\N{electric plug}\N{electric plug}\N{electric plug}\N{electric plug}\N{electric plug}")])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.\N{electric plug}
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["POST", "GET"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        print("True")
        print(form.data)
        new_cafe = form.data
        count = 0
        cafe_list = [new_cafe["cafe"], new_cafe["location"], new_cafe["o_time"], new_cafe["c_time"],
                     new_cafe["coffee_rating"],
                     new_cafe["wifi_rating"], new_cafe["power_rating"]]
        for value in range(4, 7):
            if value == 4:
                emoji = "\N{hot beverage}" * int(cafe_list[value])
                cafe_list[value] = emoji
            elif value == 5:
                if cafe_list[value] == "none":
                    cafe_list[value] = "\N{heavy ballot X}"
                else:
                    emoji = "\N{flexed biceps}" * int(cafe_list[value])
                    cafe_list[value] = emoji
            elif value == 6:
                if cafe_list[value] == "none":
                    cafe_list[value] = "\N{heavy ballot X}"
                else:
                    emoji = "\N{electric plug}" * int(cafe_list[value])
                    cafe_list[value] = emoji

        # for key, value in new_cafe.items():
        #     if count >= 4:
        #         if value == "none":
        #             cafe_list.append("\N{cross mark}")
        #         else:
        #             value = int(value)
        #             if key == 'coffee_rating':
        #                 rate = "\N{hot beverage}" * value
        #             elif key == "'wifi_rating":
        #                 rate = "\N{flexed biceps}" * value
        #             else:
        #                 rate = "\N{electric plug}" * value
        #             cafe_list.append(rate)
        #     else:
        #         cafe_list.append(value)
        #     count += 1
        print(cafe_list)
        with open("cafe-data.csv", mode="a", encoding="utf-8", newline="") as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(cafe_list)
        with open('cafe-data.csv', mode='r', newline='', encoding="utf-8") as csv_file:
            csv_data = csv.reader(csv_file)
            list_of_rows = []
            for row in csv_data:
                print(row)
                list_of_rows.append(row)
            print(list_of_rows)
        return render_template('cafes.html', cafes=list_of_rows)


    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', mode='r', newline='', encoding="utf-8") as csv_file:
        csv_data = csv.reader(csv_file)
        list_of_rows = []
        for row in csv_data:
            print(row)
            list_of_rows.append(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
