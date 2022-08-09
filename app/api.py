import json

import os.path
from flask import request, current_app
from flask import Blueprint, jsonify
from PyKakao import KakaoLocal
from app.db import get_db
bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/contents')
def contents(): #all-contents
    db=get_db()
    page = int(request.args.get('page'))
    offset = (page-1)*10
    results = db.execute(
        "SELECT * "
        "FROM test_contents "
        "LIMIT 10 OFFSET :num;",{"num":offset},
    ).fetchall()

    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/district/<district_name>')
def district_contents(district_name):
    db=get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents INNER JOIN test_center "
        "ON test_contents.center_name=test_center.center_name and test_center.district_name = :dcn "
        "LIMIT 10 OFFSET :num;", {"dcn": district_name, "num":offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/category/<category_name>')
def category_contents(category_name):
    db=get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents "
        "WHERE test_contents.category = :ctg "
        "LIMIT 10 OFFSET :num", {"ctg":category_name, "num":offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/district/<district_name>/category/<category_name>')
def district_category_contents(district_name, category_name):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents INNER JOIN test_center "
        "ON test_contents.center_name = test_center.center_name and test_center.district_name=:dcn "
        "WHERE test_contents.category=:ctg "
        "LIMIT 10 OFFSET :num",{"dcn":district_name, "ctg":category_name, "num":offset}
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/center/<center_name>')
def center_contents(center_name):
    db = get_db()
    page = int(request.args.get('page'))
    offset = (page - 1) * 10
    results = db.execute(
        "SELECT * "
        "FROM test_contents " 
        "WHERE test_contents.center_name= :cn "
        "LIMIT 10 OFFSET :num;", {"cn":center_name, "num":offset},
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
        "LIMIT 10 OFFSET :num;", {'cid':contents_id, 'num':offset},
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/logo')
def logo():
    db=get_db()
    results=db.execute(
        "SELECT * "
        "FROM logo;"
    ).fetchall()
    return json.dumps([dict(ix) for ix in results], ensure_ascii=False)

@bp.route('/contents/surround')
def surround():
    db=get_db()
    page = int(request.args.get('page'))
    latitude=float(request.args.get('latitude'))
    longitude=float(request.args.get('longitude'))
    base_path= os.path.dirname(__file__)
    with open(os.path.join(base_path,'../config.json')) as json_file:
        json_data = json.load(json_file)
        key = json_data['REST_KEY']
    KL = KakaoLocal(key)
    x,y = longitude, latitude
    placement_list = db.execute(
        "SELECT placement_name "
        "FROM test_placement; "
    ).fetchall()
    placement_list = [ix['placement_name'] for ix in placement_list]
    results=[]
    for i in placement_list:
        tmp=KL.search_keyword(query=i,x=x,y=y,radius=15)
        if tmp['meta']['pageable_count']!=0:
            results.append(i)
    surround_result=[]
    for i in results:
        tmp_list = db.execute(
            "SELECT * "
            "FROM test_contents "
            "WHERE placement_name=:ct",{'ct':i},
        ).fetchall()
        surround_result+=[dict(ix) for ix in tmp_list]
    if 10*page<len(surround_result):
        return json.dumps(surround_result[10*(page-1):10*(page)], ensure_ascii=False)
    else:
        return json.dumps(surround_result[10*(page):], ensure_ascii=False)