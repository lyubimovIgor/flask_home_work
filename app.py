from flask import Flask, jsonify
from flask.views import MethodView
from flask import request
from models import Session, Ad
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


class HttpError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def error_handler(err: HttpError):
    http_response = jsonify({"status": "error", "message": err.message})
    http_response.status_code = err.status_code
    return http_response


def get_ad(ad_id, session):
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, "Not found")
    return ad


class AdsView(MethodView):

    def get(self, ad_id):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({"ID": ad.id,
                            "Title": ad.title,
                            "Description": ad.description,
                            "Created": ad.created_at,
                            "Author": ad.author})

    def post(self):
        json_data = request.json
        with Session() as session:
            new_ad = Ad(json_data)
            session.add(new_ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(408, "Ad already exists")
            return jsonify({"id": new_ad.id})

    def patch(self, ad_id):

        json_data = request.json
        with Session() as session:
            ad = get_ad(ad_id, session)
            for key, value in json_data.items():
                setattr(ad, key, value)
            session.add(ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(408, "Ad already exists")
            return jsonify({"status": "success"})

    def delete(self, ad_id):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
            return jsonify({"status": "success"})


ads = AdsView.as_view('ads')
app.add_url_rule('/ads/', view_func=ads, methods=['POST'])
app.add_url_rule('/ads/<int:ad_id>/', view_func=ads, methods=['GET', 'PATCH', 'DELETE'])

if __name__ == '__main__':
    app.run()
