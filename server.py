import json
from datetime import datetime, timedelta
from flask import Flask, redirect, url_for, render_template, request, session, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import base62
from sqlalchemy import and_
import os

# generate Flask
app = Flask(__name__, template_folder='template')
# config DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)
# fix CORS problems
CORS(app)


# create URLShortener class as table in DB
class URLShortener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.today())

    def __repr__(self):
        return '<User %r>' % self.id, self.long_url, self.short_url, self.data_created


# routing to home page
@app.route("/")
def home():
    return render_template("index.html")


# redirect the short url to original address
@app.route('/<directed_url>', methods=['GET'])
def directed(directed_url):
    try:
        row = URLShortener.query.filter_by(short_url=directed_url).first_or_404()
        return redirect(row.long_url)
    except Exception as e:
        logWriter("error", e, datetime.today())
        return make_response("cant redirect to original website"
                             " ,please check your address or try again later", 404)


# returning report about the system
@app.route("/stats", methods=["GET"])
def stats():
    try:
        if request.method == "GET":
            # number of rows in URLShortener DB
            rows = URLShortener.query.count()
            # dict of rows that insert before minute/hour/day
            creation_date_dict = {'minute': str(selectURLByDate(days=0, hours=0, minutes=1)),
                                  'hour': str(selectURLByDate(days=0, hours=1, minutes=0)),
                                  'day': str(selectURLByDate(days=1, hours=0, minutes=0))}
            # dict of errors that insert before minute/hour/day
            error_date_dict = {'minute': str(selectErrorByDate(days=0, hours=0, minutes=1)),
                               'hour': str(selectErrorByDate(days=1, hours=1, minutes=0)),
                               'day': str(selectErrorByDate(days=1, hours=0, minutes=0))}
            # return make_response(jsonify(rows=rows, count_by_date=creation_date_dict,
            #                            count_by_error=error_date_dict), 200)
            return render_template("stats.html", rows=rows, count_by_date=creation_date_dict,
                                   count_by_error=error_date_dict)
        else:
            return render_template("stats.html")
    except Exception as e:
        logWriter("error", e, datetime.today())
        return make_response("cant get any information ,try again later", 404)


# read line by line in log file and check if this line is error type and when it had been writen
def selectErrorByDate(days, hours, minutes):
    count = 0
    file = open("log.txt", "r")
    lines = file.readlines()
    current_date = datetime.today() - timedelta(days=days, hours=hours, minutes=minutes)
    for line in lines:
        jsonObj = json.loads(line)
        error_date = datetime.strptime(jsonObj['date'], '%Y-%m-%d %H:%M:%S.%f')
        if jsonObj['type'] == 'error' and error_date >= current_date:
            count += 1
    return count


# get from DB all the urls before x minutes/hours/days
def selectURLByDate(days, hours, minutes):
    return URLShortener.query.filter(
        and_(URLShortener.data_created >= datetime.today()
             - timedelta(days=days, hours=hours, minutes=minutes))).count()


# create the short url by base62 on the index of the row in DB
@app.route("/generate", methods=["POST"])
def generate():
    try:
        if request.method == "POST":
            url_json = request.get_json()
            url = url_json["url"]
            if "https://" not in url:
                url = "https://" + url
            new_url = createShortURL(url)
            insertURL(new_url)
            print(new_url.short_url)
            return make_response(jsonify(url=new_url.short_url), 200)  # return Json
    except Exception as e:
        logWriter("error", e, datetime.today())
        return make_response("", 404)


# check that index is valid : the base62 not direct to function in server.py
def new_index_func(new_index):
    if new_index is None:
        new_index = 1
    else:
        dictionary = {'stats', 'generate'}
        new_index += 1
        while base62.encode(new_index) in dictionary:
            new_index += 1
    return new_index, base62.encode(new_index)


# generate URLShortener obj to write to DB
def createShortURL(url):
    new_index = db.session.query(db.func.max(URLShortener.id)).scalar()
    new_index, base62_url = new_index_func(new_index)
    return URLShortener(id=new_index, long_url=url,
                        short_url=str(base62_url))


# insert the URLShortener obj to URLShortener table
def insertURL(new_task):
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        logWriter("error", e, datetime.today())


def logWriter(description, res, date):
    data = {'type': description, 'description': res.__repr__(), 'date': date.__str__()}
    with open('log.txt', 'a') as outfile:
        json.dump(data, outfile)
        outfile.write("\n")


if __name__ == "__main__":
    app.run()
