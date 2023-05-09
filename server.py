from hashlib import md5
from flask import Flask, jsonify, request
from flask.views import MethodView
from models import Session, Ad
from schema import CreateAd, PatchAd, VALIDATION_CLASS
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

app = Flask("app")


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | list | str):
        self.status_code = status_code
        self.message = message


@app.errorhandler(HttpError)
def http_error_handler(error: HttpError):
    error_message = {"status": "error", "description": error.message}
    response = jsonify(error_message)
    response.status_code = error.status_code
    return response


def validate_json(json_data: dict, validation_model: VALIDATION_CLASS):
    try:
        model_obj = validation_model(**json_data)
        model_obj_dict = model_obj.dict(exclude_none=True)
    except ValidationError as err:
        raise HttpError(400, message=err.errors())
    return model_obj_dict


def get_ad(session: Session, ad_id: int):
    ad = session.get(Ad, ad_id)
    if ad is None:
        raise HttpError(404, message="ad doesn't exist")
    return ad


def hash_password(password: str):
    password = password.encode()
    password_hash = md5(password)
    password_hash_str = password_hash.hexdigest()
    return password_hash_str


class AdView(MethodView):
    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(session, ad_id)
            return jsonify(
                {
                    "id": ad.id,
                    "title": ad.title,
                    "description": ad.description,
                    "owner": ad.owner,
                    "creation_date": ad.creation_date.isoformat(),
                }
            )

    def post(self):
        json_data = validate_json(request.json, CreateAd)
        # json_data["password"] = hash_password(json_data["password"])
        with Session() as session:
            ad = Ad(**json_data)
            session.add(ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["title"]} с таким заголовком уже есть')
            return jsonify({"id": ad.id})

    def patch(self, ad_id: int):
        json_data = validate_json(request.json, PatchAd)
        # if "password" in json_data:
        #     json_data["password"] = hash_password(json_data["password"])
        with Session() as session:
            ad = get_ad(session, ad_id)
            for field, value in json_data.items():
                setattr(ad, field, value)
            session.add(ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, f'{json_data["title"]} с таким заголовком уже есть')
            return jsonify(
                {
                    "id": ad.id,
                    "title": ad.title,
                    "description": ad.description,
                    "owner": ad.owner,
                    "creation_date": ad.creation_date.isoformat(),
                }
            )

    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(session, ad_id)
            session.delete(ad)
            session.commit()
            return jsonify({"status": "success"})


app.add_url_rule(
    "/ad/<int:ad_id>",
    view_func=AdView.as_view("with_ad_id"),
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule("/ad/", view_func=AdView.as_view("create_ad"), methods=["POST"])
if __name__ == "__main__":
    app.run()
