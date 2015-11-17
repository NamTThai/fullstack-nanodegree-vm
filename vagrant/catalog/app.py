from flask import Flask, render_template, request, jsonify, make_response
from flask import session as login_session
import random
import string
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Type, Pokemon
import urllib2
from datetime import datetime

app = Flask(__name__, static_url_path='')

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def main():
    return mainRender("latest_item")


@app.route('/<type_name>')
def mainTypeName(type_name):
    return mainRender(type_name)


@app.route('/<int:type_id>')
def mainTypeId(type_id):
    route = session.query(Type).filter_by(id=type_id).all()
    if len(route) != 1:
        return mainRender("latest_item")
    else:
        return mainRender(route[0].name)


def mainRender(route):
    types = session.query(Type).all()
    latestEntries = session.query(Pokemon).order_by(desc(Pokemon.date_entered)).limit(20)
    return render_template(
        'index.html', types=types, latestEntries=latestEntries, route=route)


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session["state"] = state
    return jsonify(state=state)


@app.route('/modify', methods=['DELETE', 'PUT', 'POST'])
def modify():
    if request.method == 'DELETE':
        pokemonId = request.form['id']
        pokemon = session.query(Pokemon).filter_by(id=pokemonId).one()
        session.delete(pokemon)
        session.commit()
        return jsonify(id=pokemonId)
    elif request.method == 'POST':
        img_url = request.form['img_url']
        if not verifyImage(img_url):
            return jsonify(message="Invalid Image URL or Image Type, "
                           "Pokedex only accepts jpg, png or gif"), 400
        pokemonId = request.form['id']
        pokemon = session.query(Pokemon).filter_by(id=pokemonId).one()
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
        img_url = request.form['img_url']
        isImage = verifyImage(img_url)
        if not isImage:
            return jsonify(message="Invalid Image URL or Image Type, "
                           "Pokedex only accepts jpg, png or gif"), 400

        type = request.form['type']
        typeId = session.query(Type).filter_by(name=type).one()
        newPokemon = Pokemon(name=request.form['name'], type=typeId,
                             img_url=img_url, description=request.form['description'])
        session.add(newPokemon)
        session.commit()
        return jsonify(id=newPokemon.id)


def verifyImage(img_url):
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
    pokemonId = request.args.get('id')
    if pokemonId is None:
        return jsonify(message="No pokemon ID specified"), 404
    else:
        pokemons = session.query(Pokemon).filter_by(id=pokemonId).all()
        if (len(pokemons) != 1):
            return jsonify(message="Nothing found"), 404
        else:
            return jsonify(pokemon=pokemons[0].getJSON())


@app.route('/v1/types')
def types():
    types = session.query(Type).all()
    return jsonify(types=[t.name for t in types])


@app.route('/rss')
def latestEntriesRss():
    now = datetime.now()
    latestEntries = session.query(Pokemon).order_by(desc(Pokemon.date_entered)).limit(20)
    rss = render_template('rss.xml', lastBuildDate=now, entries=latestEntries)
    response = make_response(rss)
    response.headers["Content-Type"] = "application/xml"
    return response


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
