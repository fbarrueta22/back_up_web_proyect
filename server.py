from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
import threading
from datetime import datetime

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

cache = {}
key_users = "users"
key_games = "games"
key_reviews = "reviews"
contador = 0
lock = threading.Lock()

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)

@app.route('/index', methods=['GET'])
def get_index():
    return render_template('/html/index.html')

@app.route('/', methods=['GET'])
def get_home():
    return render_template('/html/home.html')

@app.route('/juegos')
def get_juegosPage():
    return render_template('/html/juegosPage.html')

@app.route('/resenas')
def get_resenasPage():
    return render_template('/html/resenasPage.html')

@app.route('/contacto')
def get_contactoPage():
    return render_template('/html/contacto.html')

@app.route('/signup')
def get_signuppage():
    return render_template('/html/signup.html')

@app.route('/login')
def get_loginpage():
    return render_template('/html/login.html')



#------------------------------------------------------------------------------#
#---------------------Login Logout Current User--------------------------------#
#------------------------------------------------------------------------------#
@app.route('/authenticate', methods=['POST'])
def authenticate():
    if str(request.data) == "b''":
        c = request.form
    else:
        c = json.loads(request.data)
    username = c['username']
    password = c['password']
    db_session = db.getSession(engine)
    respuesta = db_session.query(entities.User).filter(
        entities.User.username == username
    ).filter(entities.User.password == password)
    db_session.close()
    users = respuesta[:]
    if len(users) > 0:
        session['logged'] = json.dumps(users[0], cls=connector.AlchemyEncoder)
        r_msg = {'msg': 'WELCOME', 'id': users[0].id, 'username': users[0].username, 'name': users[0].name, 'lastname': users[0].lastname}
        return Response(json.dumps(r_msg), status = 201)
    r_msg = {'msg': 'Error de inicio de sesion'}
    return Response(json.dumps(r_msg), status = 401)

@app.route('/logout', methods = ['GET'])
def logout():
    if 'logged' in session:
        session.pop('logged')
    msg = {'msg':'Saliste de la sesión'}
    json_msg = json.dumps(msg)
    return Response(json_msg, status=201, mimetype='application/json')

@app.route('/current_user', methods = ['GET'])
def current_user():
    if 'logged' in session:
        current = session['logged']
        msg = {'msg': 'OK', 'current': json.loads(current)}
        json_msg = json.dumps(msg)
        return Response(json_msg, status=201, mimetype='application/json')
    msg = {'msg':'NOT'}
    json_msg = json.dumps(msg)
    return Response(json_msg, status=401, mimetype='application/json')

#------------------------------------------------------------------------------#
#---------------------------CRUD user------------------------------------------#
#------------------------------------------------------------------------------#
@app.route('/users', methods = ['GET'])
def get_users():
    lock.acquire()
    data = []
    if key_users in cache and (datetime.now() - cache[key_users]['datetime']).total_seconds() < 10:
        data = cache[key_users]['data']
    else:
        db_session = db.getSession(engine)
        db_response = db_session.query(entities.User)
        data = db_response[:]
        now = datetime.now()
        cache[key_users] = {'data': data, 'datetime': now}
        db_session.close()
    lock.release()
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')

@app.route('/users', methods = ['POST'])
def create_user():
    if str(request.data) == "b''":
        c = request.form
        if 'values' in request.form:
            c = json.loads(request.form['values'])
    else:
        c = json.loads(request.data)

    db_session = db.getSession(engine)
    userRepited = db_session.query(entities.User).filter(entities.User.username == c['username']).first()

    if not userRepited:
        user = entities.User(
            username = c['username'],
            name = c['name'],
            lastname = c['lastname'],
            password = c['password']
        )
        db_session.add(user)
        db_session.commit()
        db_session.close()
        return Response(json.dumps({'msg':'User created'}), status=201)
    else:
        db_session.close()
        return Response(json.dumps({'msg':'Ya existe este username'}), status=401)

@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id).first()
    for user in users:
        jsonObject = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(jsonObject, status=200, mimetype='application/json')
    db_session.close()
    return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')

@app.route('/users', methods = ['PUT'])
def update_user():
    id = request.form['key']
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == id).first()
    if not user:
        return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    db_session.add(user)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'User updated'}), status=200)

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == id).first()
    if not user:
        return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')
    db_session.delete(user)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'User deleted'}), status=204)



#------------------------------------------------------------------------------#
#---------------------------CRUD game------------------------------------------#
#------------------------------------------------------------------------------#
@app.route('/games', methods = ['GET'])
def get_games():
    lock.acquire()
    data = []
    if key_games in cache and (datetime.now() - cache[key_games]['datetime']).total_seconds() < 10:
        data = cache[key_games]['data']
    else:
        db_session = db.getSession(engine)
        dbresponse = db_session.query(entities.Game)
        data = dbresponse[:]
        now = datetime.now()
        cache[key_games] = {'data': data, 'datetime': now}
        db_session.close()
    lock.release()
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), status=200, mimetype='application/json')

@app.route('/games', methods = ['POST'])
def create_game():
    if str(request.data) == "b''":
        c = request.form
        if 'values' in request.form:
            c = json.loads(request.form['values'])
    else:
        c = json.loads(request.data)
    game = entities.Game(
        title = c['title'],
        category = c['category'],
        description = c['description'],
        trailer = c['trailer'],
        version = c['version'],
        company = c['company'],
        price = c['price'],
        quantity = c['quantity'],
        valoration = c['valoration']
    )
    db_session = db.getSession(engine)
    db_session.add(game)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'Game created'}), status=201)

@app.route('/games/<id>', methods = ['GET'])
def get_game(id):
    db_session = db.getSession(engine)
    games = db_session.query(entities.Game).filter(entities.Game.id == id)
    for game in games:
        jsonObject = json.dumps(game, cls=connector.AlchemyEncoder)
        return  Response(jsonObject, status=200, mimetype='application/json')
    db_session.close()
    return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')

@app.route('/games', methods = ['PUT'])
def update_game():
    id = request.form['key']
    db_session = db.getSession(engine)
    game = db_session.query(entities.Game).filter(entities.Game.id == id).first()
    if not game:
        return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(game, key, c[key])
    db_session.add(game)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'Game updated'}), status=200)

@app.route('/games', methods = ['DELETE'])
def delete_game():
    id = request.form['key']
    db_session = db.getSession(engine)
    game = db_session.query(entities.Game).filter(entities.Game.id == id).first()
    if not game:
        return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')
    db_session.delete(game)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'Game deleted'}), status=204)

#------------------------------------------------------------------------------#
#---------------------------CRUD review----------------------------------------#
#------------------------------------------------------------------------------#
@app.route('/reviews', methods = ['GET'])
def get_reviews():
    lock.acquire()
    data = []
    if key_reviews in cache and (datetime.now() - cache[key_reviews]['datetime']).total_seconds() < 10:
        data = cache[key_reviews]['data']
    else:
        db_session = db.getSession(engine)
        db_response = db_session.query(entities.Review)
        reviews = db_response[:]
        for review in reviews:
            d = {'id': review.id,
                 'content': review.content,
                 'write_on': str(review.write_on),
                 'valoration': review.valoration,
                 'user_id': str(review.user_id),
                 'user': review.user.username,
                 'game_id': str(review.game_id),
                 'game': review.game.title}
            data.append(d)
        now = datetime.now()
        cache[key_reviews] = {'data': data, 'datetime': now}
        db_session.close()
    lock.release()
    return Response(json.dumps(data), status=200, mimetype='application/json')

@app.route('/reviews', methods = ['POST'])
def create_review():
    if str(request.data) == "b''":
        c = request.form
        if 'values' in request.form:
            c = json.loads(request.form['values'])
    else:
        c = json.loads(request.data)
    db_session = db.getSession(engine)
    _user_username = c['user']
    user = db_session.query(entities.User).filter(entities.User.username == _user_username).first()
    _game_title = c['game']
    game = db_session.query(entities.Game).filter(entities.Game.title == _game_title).first()

    review = entities.Review(
        content = c['content'],
        write_on = datetime.now(),
        valoration = c['valoration'],
        user_id = user.id,
        game_id = game.id
    )
    db_session.add(review)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'Review created'}), status=201)

@app.route('/reviews/<game_id>', methods = ['POST'])
def create_review2(game_id):
    #c = json.loads(request.data)
    c = json.loads(request.form['values'])
    db_session = db.getSession(engine)
    _user_username = c['user']
    user = db_session.query(entities.User).filter(entities.User.username == _user_username).first()
    _game_title = c['game']
    game = db_session.query(entities.Game).filter(entities.Game.title == _game_title).first()

    review = entities.Review(
        content = c['content'],
        write_on = datetime.now(),
        valoration = c['valoration'],
        user_id = user.id,
        game_id = id
    )
    db_session.add(review)
    db_session.commit()
    db_session.close()
    return render_template('/html/resenasPage.html')

@app.route('/reviews/<id>', methods = ['GET'])
def get_review(id):
    db_session = db.getSession(engine)
    reviews = db_session.query(entities.Review).filter(entities.Review.id == id)
    for review in reviews:
        jsonObject = json.dumps(review, cls=connector.AlchemyEncoder)
        return  Response(jsonObject, status=200, mimetype='application/json')
    db_session.close()
    return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')

@app.route('/reviews', methods = ['PUT'])
def update_review():
    id = request.form['key']
    db_session = db.getSession(engine)
    review = db_session.query(entities.Review).filter(entities.Review.id == id).first()
    if not review:
        return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(review, key, c[key])
    db_session.add(review)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'Review updated'}), status=200)

@app.route('/reviews', methods = ['DELETE'])
def delete_review():
    id = request.form['key']
    db_session = db.getSession(engine)
    review = db_session.query(entities.Review).filter(entities.Review.id == id).first()
    if not review:
        return Response(json.dumps({'msg': 'NOT FOUND'}), status=404, mimetype='application/json')
    db_session.delete(review)
    db_session.commit()
    db_session.close()
    return Response(json.dumps({'msg':'Review deleted'}), status=204)

@app.route('/get_reviews/<game_id>', methods = ['GET'])
def get_reviews2(game_id):
    db_session = db.getSession(engine)
    reviews = db_session.query(entities.Review).filter(entities.Review.game_id == game_id)
    all_reviews = reviews[:]
    return Response(json.dumps(all_reviews, cls=connector.AlchemyEncoder), mimetype='application/json')


if __name__ == '__main__':
    app.secret_key = ".."
    app.run(port=8080, threaded=True, host=('127.0.0.1'))
