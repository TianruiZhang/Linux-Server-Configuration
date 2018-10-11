#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect,\
                    url_for, flash, jsonify, make_response
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Selection, MenuItem
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError, \
    AccessTokenCredentials
import random, string, httplib2, json, requests

app = Flask(__name__)
CLIENT_ID = json.loads(open("client_secrets.json", "r").read())["web"]["client_id"]
engine = create_engine("sqlite:///menu.db",
    connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route("/login")
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase + string.digits) \
        for i in range(32))
    login_session["state"] = state
    return render_template("login.html", STATE=state)

@app.route("/gconnect", methods=["POST"])
def gconnect():
    if request.args.get("state") != login_session["state"]:
        response = make_response(json.dumps("Invalid state parameter"), 401)
        response.headers["Content-Type"]="application/json"
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets("client_secrets.json", scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}".format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1].decode("utf-8"))
    if result.get("error") is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers["Content-Type"] = "application/json"
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
        response = make_response(json.dumps("Token's User ID doesn't match given user ID"), 401)
        print("Token's client ID doesn't match app's")
        response.headers["Content-Type"] = "application/json"
        return response
    stored_credentials = login_session.get("credentials")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers["Content-Type"] = "application-json"
    login_session["credentials"] = credentials.access_token
    login_session["gplus_id"] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)
    login_session["username"] = data["name"]
    login_session["picture"] = data["picture"]
    login_session["email"] = data["email"]
    output = ""
    output += "<h1>Welcome, "
    output += login_session["username"]
    output += "!</h1>"
    output += "<img src='"
    output += login_session["picture"]
    output += " style='width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;'>"
    flash("you are now logged in as {}".format(login_session["username"]))
    return output

@app.route("/gdisconnect")
def gdisconnect():
    credentials = login_session.get("credentials")
    if credentials is None:
        response = make_response(json.dumps("Current user not connected."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    access_token = credentials
    url = "https://accounts.google.com/o/oauth2/revoke?token={}".format(access_token)
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
    if result["status"] == "200":
        del login_session["credentials"]
        del login_session["gplus_id"]
        del login_session["username"]
        del login_session["email"]
        del login_session["picture"]
        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers["Content-Type"] = "application/json"
        return response
    else:
        response = make_response(json.dumps("Failed to revoke token for the given user."), 400)
        response.headers["Content-Type"] = "application/json"
        return response

@app.route("/")
@app.route("/home/")
def homepage():
    selections = session.query(Selection).all()
    items = (session.query(MenuItem.name, Selection.name)).\
        join(Selection, MenuItem.selection_id == Selection.id).\
        order_by(MenuItem.id.desc()).filter(MenuItem.id > 43).all()
    return render_template("home.html", selections=selections, items=items)

@app.route("/selections/<int:selection_id>/")
def selectionMenu(selection_id):
    selections = session.query(Selection).all()
    selection = session.query(Selection).filter_by(id=selection_id).one()
    items = session.query(MenuItem).filter_by(selection_id=selection.id)
    return render_template("selectionMenu.html", selections=selections,\
                            selection=selection, items=items)

@app.route("/selections/<int:selection_id>/<int:menu_id>/")
def menuDetails(selection_id, menu_id):
    item = session.query(MenuItem).\
        filter(and_(MenuItem.selection_id == selection_id, \
        MenuItem.id == menu_id)).one()
    return render_template("details.html", item=item)

@app.route("/new/", methods=["GET", "POST"])
def newMenuItem():
    selections = session.query(Selection).all()
    if request.method == "POST":
        newItem = MenuItem(name=request.form["name"], \
                           price=request.form["price"], \
                           description=request.form["description"], \
                           selection_id=request.form.get("comp_select"))
        session.add(newItem)
        session.commit()
        return redirect(url_for("homepage"))
    else:
        return render_template("newMenuItem.html", selections=selections)

if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
