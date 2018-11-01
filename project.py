#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect,\
                    url_for, flash, jsonify, make_response
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Selection, MenuItem, User
from flask import session as login_session
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError, \
    AccessTokenCredentials
import random
import string
import httplib2
import json
import requests

app = Flask(__name__)
CLIENT_ID = json.loads(
                open("client_secrets.json", "r").read()
                )["web"]["client_id"]
engine = create_engine(
                "sqlite:///menu.db",
                connect_args={'check_same_thread': False}, echo=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route("/selections/<int:selection_id>/menu/JSON/")
def selectionMenuJSON(selection_id):
    """
    Implements a JSON endpoint for items in an arbitrary selection.
    Args:
        selection_id(int): Selection ID
    Returns:
        A JSON response
    """
    selection = session.query(Selection).filter_by(id=selection_id).one()
    items = session.query(MenuItem).filter_by(selection_id=selection_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route("/selections/<int:selection_id>/menu/<int:menu_id>/JSON/")
def menuItemJSON(selection_id, menu_id):
    """
    Implements a JSON endpoint for an arbitrary item in an arbitrary selection.
    Args:
        selection_id(int): selection ID of an existing menu item
        menu_id(int): ID of an existing menu item
    Returns:
        A JSON response
    """
    menuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menuItem.serialize)


@app.route("/login")
def showLogin():
    """
    Generate a random state and pass it to the login page.
    Args:
        Not applicable
    Returns:
        Renders a template with a state variable available in the context of
        the template
    """
    state = "".join(
                random.choice(string.ascii_uppercase + string.digits)
                for i in range(32))
    login_session["state"] = state
    return render_template("login.html", STATE=state)


def getUserID(email):
    """
    Get user ID.
    Args:
        email(str): email
    Returns:
        User ID
    """
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


def getUserInfo(user_id):
    """
    Get user information.
    Args:
        user_id(int): user ID
    Returns:
        User information
    """
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    """
    Create a new user.
    Args:
        login_session(dict): Login session
    Returns:
        ID of the newly created user
    """
    newUser = User(
        name=login_session["username"],
        email=login_session["email"],
        picture=login_session["picture"])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session["email"]).first()
    return user.id


@app.route("/gconnect", methods=["POST"])
def gconnect():
    """
    Connect to Google authetication.
    Args:
        Not applicable
    Returns:
        HTML display of a logged-in user's name and profile picture
    """
    if request.args.get("state") != login_session["state"]:
        response = make_response(json.dumps("Invalid state parameter"), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets("client_secrets.json", scope="")
        oauth_flow.redirect_uri = "postmessage"
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps("Failed to upgrade the authorization code."), 401)
        response.headers["Content-Type"] = "application/json"
        return response
    access_token = credentials.access_token
    url = (
        "https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}".
        format(access_token)
    )
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1].decode("utf-8"))
    if result.get("error") is not None:
        response = make_response(json.dumps(result.get("error")), 500)
        response.headers["Content-Type"] = "application/json"
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
        response = make_response(json.dumps(
            "Token's User ID doesn't match given user ID"
                ), 401
            )
        print("Token's client ID doesn't match app's")
        response.headers["Content-Type"] = "application/json"
        return response
    stored_credentials = login_session.get("credentials")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            "Current user is already connected."), 200
        )
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
    user_id = getUserID(login_session["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session["user_id"] = user_id
    output = ""
    output += "<h1>Welcome, "
    output += login_session["username"]
    output += "!</h1>"
    output += "<img src='"
    output += login_session["picture"]
    output += " style='width: 300px; height: 300px; border-radius: 150px;"\
        " -webkit-border-radius: 150px; -moz-border-radius: 150px;'>"
    flash("you are now logged in as {}".format(login_session["username"]))
    return output


@app.route("/gdisconnect")
def gdisconnect():
    """
    Disconnect a user from the login session.
    Args:
        Not applicable
    Returns:
        Disconnect from the login session and redirect the user to the homepage
    """
    credentials = login_session.get("credentials")
    if credentials is None:
        response = make_response(json.dumps(
            "Current user not connected."
                ), 401
            )
        response.headers["Content-Type"] = "application/json"
        return response
    access_token = credentials
    url = "https://accounts.google.com/o/oauth2/revoke?token={}".format(
        access_token
        )
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
        return redirect("/home")
    else:
        response = make_response(json.dumps(
            "Failed to revoke token for the given user."
                ), 400
            )
        response.headers["Content-Type"] = "application/json"
        return redirect("/home")


@app.route("/")
@app.route("/home/")
def homepage():
    """
    Display selections and menu items on the homepage.
    Args:
        Not applicable
    Returns:
        Renders a template with selections and menu items readily available
    """
    selections = session.query(Selection).all()
    selection = session.query(Selection).first()
    creator = getUserInfo(selection.user_id)
    items = (session.query(MenuItem.name, Selection.name)).\
        join(Selection, MenuItem.selection_id == Selection.id).\
        order_by(MenuItem.id.desc()).filter(MenuItem.id > 43).all()
    if ("username" not in login_session or
            creator.id != login_session["user_id"]):
                return render_template(
                    "publicHome.html",
                    selections=selections,
                    creator=creator,
                    items=items
                    )
    else:
        return render_template(
            "home.html",
            selections=selections,
            items=items,
            creator=creator
            )


@app.route("/selections/<int:selection_id>/")
def selectionMenu(selection_id):
    """
    Display menu items of an arbitrary selection.
    Args:
        selection_id(int): ID of an existing selection
    Returns:
        Renders a template with menu items of an arbitrary selection
    """
    selections = session.query(Selection).all()
    selection = session.query(Selection).filter_by(id=selection_id).one()
    items = session.query(MenuItem).filter_by(selection_id=selection.id)
    return render_template(
        "selectionMenu.html",
        selections=selections,
        selection=selection,
        items=items
        )


@app.route("/selections/<int:selection_id>/<int:menu_id>/")
def menuDetails(selection_id, menu_id):
    """
    Display the price and description of an arbitrary menu item of an arbitrary
    selection.
    Args:
        selection_id(int): selection ID of existing menu items
        menu_id(int): menu ID of existing menu items
    Returns:
        Renders a template with detailed description and price information of
        an arbitrary menu item of an arbitrary selection.
    """
    item = session.query(MenuItem).filter(
        and_(
            MenuItem.selection_id == selection_id,
            MenuItem.id == menu_id
            )
        ).one()
    creator = getUserInfo(item.user_id)
    if ("username" not in login_session or
            creator.id != login_session["user_id"]):
            return render_template("publicDetails.html", item=item)
    else:
        return render_template("details.html", item=item)


@app.route("/new/", methods=["GET", "POST"])
def newMenuItem():
    """
    Create a new menu item.
    Args:
        Not applicable
    Returns:
        Renders a template that enables a user to fill in the information of a
        menu item.
    """
    selections = session.query(Selection).all()
    if "username" not in login_session:
        return redirect("/login")
    if request.method == "POST":
        newItem = MenuItem(
            name=request.form["name"],
            price=request.form["price"],
            description=request.form["description"],
            selection_id=request.form.get("comp_select"),
            user_id=login_session["user_id"]
            )
        session.add(newItem)
        session.commit()
        return redirect(url_for("homepage"))
    else:
        return render_template("newMenuItem.html", selections=selections)


@app.route(
    "/selection/<int:selection_id>/<int:menu_id>/edit/",
    methods=["GET", "POST"]
    )
def editMenuItem(selection_id, menu_id):
    """
    Edit an arbitrary menu item of an arbitrary selection.
    Args:
        selection_id(int): selection ID of the menu item to be edited
        menu_id(int): menu ID of the menu item to be edited
    Returns:
        Renders a template that directs a user to edit an arbitrary menu item
        of an arbitrary selection.
    """
    selections = session.query(Selection).all()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if "username" not in login_session:
        return redirect("/login")
    if editedItem.user_id != login_session["user_id"]:
        return (
            "<script>function myFunction() "
            "{alert('You are not authorized to edit this menu item. "
            "You can only edit menu items that you created.');}"
            "</script><body onload='myFunction()'>"
            )
    if request.method == "POST":
        if request.form["name"]:
            editedItem.name = request.form["name"]
        if request.form["price"]:
            editedItem.price = request.form["price"]
        if request.form["description"]:
            editedItem.description = request.form["description"]
        if request.form.get("comp_select"):
            editedItem.selection_id = request.form.get("comp_select")
        session.add(editedItem)
        session.commit()
        return redirect(url_for("selectionMenu", selection_id=selection_id))
    else:
        return render_template(
                "editMenuItem.html",
                selections=selections,
                selection_id=selection_id,
                menu_id=menu_id,
                item=editedItem
                )


@app.route(
    "/selection/<int:selection_id>/<int:menu_id>/delete/",
    methods=["GET", "POST"]
    )
def deleteMenuItem(selection_id, menu_id):
    """
    Delete an arbitrary menu item of an arbitrary selection.
    Args:
        selection_id(int): selection ID of the menu item to be deleted
        menu_id(int): menu ID of the menu item to be deleted
    Returns:
        Renders a template that directs a user to delete an arbitrary menu item
        of an arbitrary selection.
    """
    itemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if "username" not in login_session:
        return redirect("/login")
    if itemToDelete.user_id != login_session["user_id"]:
        return (
            "<script>function myFunction() "
            "{alert('You are not authorized to delete this menu item. "
            "You can only delete menu items that you created.');}"
            "</script><body onload='myFunction()'>"
            )
    if request.method == "POST":
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for("selectionMenu", selection_id=selection_id))
    else:
        return render_template("deleteMenuItem.html", item=itemToDelete)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
