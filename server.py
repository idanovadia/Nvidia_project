from datetime import datetime
from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import base62

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
db = SQLAlchemy(app)


class URLShortener(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    long_url = db.Column(db.String(200), nullable=False)
    short_url = db.Column(db.String(200), nullable=False)
    data_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.id, self.long_url, self.short_url, self.data_created


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/<directed_url>', methods=['GET'])
def directed(directed_url):
    row = URLShortener.query.filter_by(short_url=directed_url).first_or_404()
    return redirect(row.long_url)


@app.route("/generate", methods=["POST"])
def generate():
    if request.method == "POST":
        url_json = request.get_json()
        url = url_json["url"]
        new_url = createShortURL(url)
        insertURL(new_url)
        print(new_url.short_url)
        return {"url": new_url.short_url}


def createShortURL(url):
    new_index = db.session.query(db.func.max(URLShortener.id)).scalar()
    if new_index is None:
        new_index = 1
    else:
        new_index += 1
    return URLShortener(id=new_index, long_url=url,
                        short_url=str(base62.encode(new_index)))


def insertURL(new_task):
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    app.run()
