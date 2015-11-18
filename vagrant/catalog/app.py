from flask import Flask, render_template, request, jsonify, make_response
from flask import session as user_session
import random
import string
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Type, Pokemon, User
import urllib2
from datetime import datetime
import httplib2
import json

app = Flask(__name__, static_url_path='')
app.secret_key = "VdGkZBnjl2TBxCZKDzwA"

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

CLIENT_ID = json.loads(open('data/client_secret.json', 'r').read())
CLIENT_ID = CLIENT_ID['web']['client_id']


@app.route('/')
def main():
    """GET main page, rendering latest items"""
    return mainRender("latest_item")


@app.route('/<type_name>')
def mainTypeName(type_name):
    """GET main page, rendering by type name"""
    return mainRender(type_name)


@app.route('/<int:type_id>')
def mainTypeId(type_id):
    """GET main page, rendering by type id"""
    route = session.query(Type).filter_by(id=type_id).all()
    if len(route) != 1:
        return mainRender("latest_item")
    else:
        return mainRender(route[0].name)


def mainRender(route):
    """Render main page with a state token for current session, and all contents
    to be displayed on main page
    """
    state = ''
    for x in xrange(32):
        state += random.choice(string.ascii_uppercase + string.digits)
    user_session["state"] = state
    types = session.query(Type).all()
    latestEntries = session.query(Pokemon)\
        .order_by(desc(Pokemon.date_entered)).limit(20)
    return render_template(
        'index.html', types=types, latestEntries=latestEntries,
        route=route, state=state)


@app.route('/favicon.ico')
def favicon():
    """Serve favicon.ico"""
    return app.send_static_file('favicon.ico')


def verifyAccessToken(state, access_token, user_id):
    """Verify whether the user is properly authenticated"""
    # Check if the provided state token is valid
    if state != user_session['state']:
        return False
    # Check if the provided access token is valid
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    http = httplib2.Http()
    result = json.loads(http.request(url, 'GET')[1])
    if result.get('error') is not None:
        return False
    # Check if the provided user_id is valid
    elif user_id != result['user_id']:
        return False
    # Check if the access token corresponds to correct client id
    elif result['issued_to'] != CLIENT_ID:
        return False
    else:
        return True


@app.route('/modify', methods=['DELETE', 'PUT', 'POST'])
def modify():
    """API Endpoint that performs all administrative actions (add, update,
    delete)
    """

    # Add user to database if not already exists
    user_email = request.form['user_email']
    user = session.query(User).filter_by(email=user_email).first()
    if user is None:
        user = User(email=user_email)
        session.add(user)
        session.commit()
        print(user.id)

    # Verify if the user is authenticated
    if not verifyAccessToken(request.form['state'],
                             request.form['access_token'],
                             request.form['user_id']):
        return jsonify(message="Unable to verify user login information"), 400

    # Respond to DELETE request to delete entry
    elif request.method == 'DELETE':
        pokemonId = request.form['id']
        pokemon = session.query(Pokemon).filter_by(id=pokemonId,
                                                   user_id=user.id).first()
        # Verify if the user is authorized to delete this pokemon by id
        if pokemon is not None:
            session.delete(pokemon)
            session.commit()
            return jsonify(id=pokemonId)
        else:
            return jsonify(message="Either that Pokemon does not exists, or you"
                           " don't have the permission to delete"
                           " this pokemon"), 400

    # Respond to POST request to update entry
    elif request.method == 'POST':
        # Verify if provided image url is valid
        img_url = request.form['img_url']
        if not verifyImage(img_url):
            return jsonify(message="Invalid Image URL or Image Type, "
                           "Pokedex only accepts jpg, png or gif"), 400

        pokemonId = request.form['id']
        pokemon = session.query(Pokemon).filter_by(id=pokemonId,
                                                   user_id=user.id).first()
        # Verify if user is authorized to update this pokemon by id
        if pokemon is not None:
            pokemon.name = request.form['name']
            type = request.form['type']
            typeId = session.query(Type).filter_by(name=type).one().id
            pokemon.type_id = typeId
            pokemon.img_url = img_url
            pokemon.description = request.form['description']
            session.add(pokemon)
            session.commit()
            return jsonify(pokemon=pokemon.getJSON())
        else:
            return jsonify(message="Either that Pokemon does not exists, or you"
                           " don't have the permission to update"
                           " this pokemon"), 400

    # Respond to PUT request to add new entry
    else:
        # Verify if provided image url is valid
        img_url = request.form['img_url']
        if not verifyImage(img_url):
            return jsonify(message="Invalid Image URL or Image Type, "
                           "Pokedex only accepts jpg, png or gif"), 400

        type = session.query(Type).filter_by(name=request.form['type']).one()
        newPokemon = Pokemon(name=request.form['name'], type=type,
                             user_id=user.id, img_url=img_url,
                             description=request.form['description'])
        session.add(newPokemon)
        session.commit()
        return jsonify(id=newPokemon.id)


def verifyImage(img_url):
    """Verify if provided image url is valid and of type either jpg, png or gif
    """
    img_url = request.form['img_url']
    prefix = img_url.startswith(('http:', 'https:'))
    suffix = img_url.endswith(('.jpg', '.png', '.gif'))
    if (not prefix) or (not suffix):
        return False
    try:
        urllib2.urlopen(img_url)
        return True
    except (ValueError, urllib2.HTTPError, urllib2.URLError):
        return False


@app.route('/v1/pokemon')
def pokemonInfo():
    """GET pokemon information by id"""
    pokemonId = request.args.get('id')
    user_email = request.args.get('user_email')
    if pokemonId is None:
        return jsonify(message="No pokemon ID specified"), 404
    else:
        pokemon = session.query(Pokemon).filter_by(id=pokemonId).first()
        if pokemon is None:
            return jsonify(message="Nothing found"), 404
        else:
            # Verify if the user is authorized to modify or delete this entry
            if pokemon.user is not None and pokemon.user.email == user_email:
                return jsonify(pokemon=pokemon.getJSON(), authorized=True)
            else:
                return jsonify(pokemon=pokemon.getJSON())


@app.route('/v1/types')
def types():
    """GET all available types"""
    types = session.query(Type).all()
    return jsonify(types=[t.name for t in types])


@app.route('/rss')
def latestEntriesRss():
    """GET an RSS Feed that contains latest entries to Pokedex"""
    now = datetime.now()
    latestEntries = session.query(Pokemon).order_by(desc(Pokemon.date_entered))\
        .limit(20)
    rss = render_template('rss.xml', lastBuildDate=now, entries=latestEntries)
    response = make_response(rss)
    response.headers["Content-Type"] = "application/xml"
    return response


# Launch application
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
