import json

import os.path
import requests
from flask import request, current_app, Response, redirect, url_for
from flask import Blueprint, jsonify
from PyKakao import KakaoLocal
from app.db import get_db
from haversine import haversine

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/recommends', methods=["POST"])
def recommends():
    db = get_db()
    data = request.get_json()
    token = data["token"]
    category = data["category"]
    sex = data["sex"]
    age = data["age"]

    db.execute(
        "INSERT INTO user (token, sex, age) "
        "values (?,?,?);", (token, sex, age),
    )

    for i in category:
        db.execute(
            "INSERT INTO test_user_category (token, category)"
            "values (?,?);", (token, i)
        )

    db.commit()

    return Response("success")


@bp.route('/contents')
def contents():  # all-contents
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents "
        "ORDER BY contents_id DESC "
        "LIMIT 10 OFFSET :num;", {"num": offset},
    ).fetchall()
    k = json.dumps([dict(ix) for ix in results], ensure_ascii=False)

    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/contents/district/<district_name>')
def district_contents(district_name):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents INNER JOIN test_center "
        "ON test_contents.center_name=test_center.center_name and test_center.district_name = :dcn "
        "ORDER BY test_contents.contents_id DESC "
        "LIMIT 10 OFFSET :num;", {"dcn": district_name, "num": offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/contents/category/<category_name>')
def category_contents(category_name):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents INNER JOIN test_category "
        "ON test_contents.category = test_category.category "
        "WHERE test_category.main_category = :ctg "
        "ORDER BY contents_id DESC "
        "LIMIT 10 OFFSET :num", {"ctg": category_name, "num": offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/contents/district/<district_name>/category/<category_name>')
def district_category_contents(district_name, category_name):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents INNER JOIN test_center, test_category "
        "ON test_contents.center_name = test_center.center_name and test_center.district_name=:dcn "
        "and test_contents.category = test_category.category "
        "WHERE test_category.main_category=:ctg "
        "ORDER BY test_contents.contents_id DESC  "
        "LIMIT 10 OFFSET :num", {"dcn": district_name, "ctg": category_name, "num": offset}
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/contents/center/<center_name>')
def center_contents(center_name):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents INNER JOIN test_placement_loc "
        "ON test_placement_loc.placement_name = test_contents.placement_name "
        "WHERE test_placement_loc.real_placement_name= :cn "
        "ORDER BY contents_id DESC "
        "LIMIT 10 OFFSET :num;", {"cn": center_name, "num": offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/contents/id/<contents_id>')
def id_contents(contents_id):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents "
        "WHERE test_contents.contents_id= :cid "
        "ORDER BY contents_id DESC "
        "LIMIT 10 OFFSET :num;", {'cid': contents_id, 'num': offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/logo')
def logo():
    db = get_db()
    results = db.execute(
        "SELECT * "
        "FROM logo;"
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)


@bp.route('/contents/surround')
def surround():
    db = get_db()
    page = int(request.args.get('page'))
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    x, y = longitude, latitude
    current=(y,x)
    placement_list = db.execute(
        "SELECT * "
        "FROM test_placement_loc; "
    ).fetchall()
    placement_list = [dict(ix) for ix in placement_list]
    results = []
    for i in placement_list:
        placement = (i['latitude'], i['longitude'])
        results.append((i, haversine(placement, current, unit='km')))
    results.sort(key=lambda x:x[1])
    if 10 * page < len(results):
        return json.dumps(results[10 * (page - 1):10 * (page)], ensure_ascii=False)
    else:
        return json.dumps(results[10 * (page):], ensure_ascii=False)


@bp.route('/get_district')
def current_district():
    base_path = os.path.dirname(__file__)
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    with open(os.path.join(base_path, '../config.json')) as json_file:
        json_data = json.load(json_file)
        key = json_data['REST_KEY']
    header = {"Authorization": "KakaoAK {}".format(key)}

    url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json"
    response = requests.get(url, headers=header, params={"x":f"{longitude}", "y":f"{latitude}"})
    document = json.loads(response.text)
    return document['documents'][0]['region_2depth_name']
