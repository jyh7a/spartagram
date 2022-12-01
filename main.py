from flask import Flask, render_template, request
import pymysql
import json

app = Flask(__name__)


#  튜플에서 딕셔너리로 cursor= db.cursor(pymysql.cursors.DictCursor)

# db 연결
# 참고 - https://problem-solving.tistory.com/10
# 참고 - https://shanepark.tistory.com/64


# route
@app.route('/')
def root():
    return render_template('index.html', component_name='groups')


# get layout
@app.route('/groups-layout')
def groupsLayout():
    return render_template('index.html', component_name='groups')


@app.route('/users-layout')
def usersLayout():
    return render_template('index.html', component_name='users')


@app.route('/images-layout')
def imagesLayout():
    return render_template('index.html', component_name='images')


# user
@app.route('/user', methods=['POST'])
def insert_user():
    db = pymysql.connect(host='localhost', user='root', db='spartagram', password='12345678', charset='utf8')
    curs = db.cursor()

    user = request.json

    first_name = user['first_name']
    last_name = user['last_name']
    user_name = user['user_name']
    email = user['email']
    avatar = user['avatar']
    city_id = user['city_id']
    group_id = user['group_id']
    print(city_id)
    print(type(city_id))

    sql = """insert into user (first_name, last_name, user_name, email, avatar, city_id, group_id)
         values (%s,%s,%s,%s,%s,%s,%s)
        """
    curs.execute(sql, (first_name, last_name, user_name, email, avatar, city_id, group_id))

    rows = curs.fetchall()

    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return 'insert success', 200


@app.route('/user', methods=['GET'])
def get_users():
    print('get_users')
    db = pymysql.connect(host='localhost', user='root', db='spartagram', password='12345678', charset='utf8')
    curs = db.cursor()

    sql = """
    SELECT *
    FROM user as u
    LEFT JOIN `group` as g
    ON u.group_id = g.id
    """

    # sql = """
    #  SELECT *
    #  FROM `user` as u
    #  LEFT JOIN `group` as g
    #    ON u.group_id = g.id
    #   """
    curs.execute(sql)

    rows = curs.fetchall()
    print(rows)

    json_str = json.dumps(rows, indent=4, sort_keys=True, default=str)
    db.commit()
    db.close()
    return json_str, 200


# photo

# group
# @app.route('/group')
# def getGroup():


# 서버실행
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
