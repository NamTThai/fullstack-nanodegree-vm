from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Type, Pokemon
import json

app = Flask(__name__, static_url_path='')

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/Types/<int:Type_id>/menu/JSON')
def TypeMenuJSON(Type_id):
    Type = session.query(Type).filter_by(id=Type_id).one()
    items = session.query(Pokemon).filter_by(
        Type_id=Type_id).all()
    return jsonify(Pokemons=[i.serialize for i in items])


# ADD JSON ENDPOINT HERE
@app.route('/Types/<int:Type_id>/menu/<int:menu_id>/JSON')
def PokemonJSON(Type_id, menu_id):
    Pokemon = session.query(Pokemon).filter_by(id=menu_id).one()
    return jsonify(Pokemon=Pokemon.serialize)


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


@app.route('/modify', methods=['DELETE', 'PUT', 'POST'])
def modify():
    if request.method == 'DELETE':
        pokemonId = request.form['id']
        pokemon = session.query(Pokemon).filter_by(id=pokemonId).one()
        session.delete(pokemon)
        session.commit()
        return jsonify(id=pokemonId)


@app.route('/v1/pokemon')
def pokemonInfoV1():
    pokemonId = request.args.get('id')
    if pokemonId is None:
        return jsonify(error="No pokemon ID specified"), 404
    else:
        pokemons = session.query(Pokemon).filter_by(id=pokemonId).all()
        if (len(pokemons) != 1):
            return jsonify(error="No pokemon ID specified"), 404
        else:
            return jsonify(pokemon=pokemons[0].getJSON())


@app.route('/v1/types')
def typesV1():
    types = session.query(Type).all()
    return jsonify(types=[t.name for t in types])


@app.route('/Types/<int:Type_id>/new', methods=['GET', 'POST'])
def newPokemon(Type_id):

    if request.method == 'POST':
        newItem = Pokemon(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], Type_id=Type_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('TypeMenu', Type_id=Type_id))
    else:
        return render_template('newPokemon.html', Type_id=Type_id)


@app.route('/Types/<int:Type_id>/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editPokemon(Type_id, menu_id):
    editedItem = session.query(Pokemon).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('TypeMenu', Type_id=Type_id))
    else:

        return render_template(
            'editPokemon.html', Type_id=Type_id, menu_id=menu_id, item=editedItem)


@app.route('/Types/<int:Type_id>/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deletePokemon(Type_id, menu_id):
    itemToDelete = session.query(Pokemon).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('TypeMenu', Type_id=Type_id))
    else:
        return render_template('deleteconfirmation.html', item=itemToDelete)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
