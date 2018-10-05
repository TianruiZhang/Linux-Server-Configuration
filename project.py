#!/usr/bin/env python3

from flask import Flask, render_template, request,\
    redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Selection, MenuItem

app = Flask(__name__)
engine = create_engine("sqlite:///menu.db",
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/")
@app.route("/home/")
def homepage():
    selections = session.query(Selection).all()
    items = (session.query(MenuItem.name, Selection.name)).\
        join(Selection, MenuItem.selection_id == Selection.id).\
        order_by(MenuItem.time_created.desc()).limit(5).all()
    return render_template("home.html", selections=selections, items=items)

#@app.route("/selections/<int:selection_id>/")
#def selectionMenu(selection_id):
    #selection = session.query(Selection).filter_by(id=selection_id).one()
    #items = session.query(MenuItem).filter_by(selection_id=selection.id)
    #return render_template("menu.html", selection=selection, items=items)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
