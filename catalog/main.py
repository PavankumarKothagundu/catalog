from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, BoatCompanyName, BoatName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///boats.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "BoatSaleCompany"

DBSession = sessionmaker(bind=engine)
session = DBSession()
# Create anti-forgery state token
kps_pks = session.query(BoatCompanyName).all()


# login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    kps_pks = session.query(BoatCompanyName).all()
    pspk = session.query(BoatName).all()
    return render_template('login.html',
                           STATE=state, kps_pks=kps_pks, pspk=pspk)
    # return render_template('myhome.html', STATE=state
    # kps_pks=kps_pks,pspk=pspk)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


# User Helper Functions
def createUser(login_session):
    User1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(User1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session

##
# Home


@app.route('/')
@app.route('/home')
def home():
    kps_pks = session.query(BoatCompanyName).all()
    return render_template('myhome.html', kps_pks=kps_pks)

#####
# Boat Category for admins


@app.route('/BoatsStore')
def BoatsStore():
    try:
        if login_session['username']:
            name = login_session['username']
            kps_pks = session.query(BoatCompanyName).all()
            kpk = session.query(BoatCompanyName).all()
            pspk = session.query(BoatName).all()
            return render_template('myhome.html', kps_pks=kps_pks,
                                   kpk=kpk, pspk=pspk, uname=name)
    except:
        return redirect(url_for('showLogin'))

######
# Showing boats based on boat category


@app.route('/BoatsStore/<int:pkid>/AllCompanys')
def showBoats(pkid):
    kps_pks = session.query(BoatCompanyName).all()
    kpk = session.query(BoatCompanyName).filter_by(id=pkid).one()
    pspk = session.query(BoatName).filter_by(boatcompanynameid=pkid).all()
    try:
        if login_session['username']:
            return render_template('showBoats.html', kps_pks=kps_pks,
                                   kpk=kpk, pspk=pspk,
                                   uname=login_session['username'])
    except:
        return render_template('showBoats.html',
                               kps_pks=kps_pks, kpk=kpk, pspk=pspk)

#####
# Add New Boat


@app.route('/BoatsStore/addBoatCompany', methods=['POST', 'GET'])
def addBoatCompany():
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        company = BoatCompanyName(name=request.form['name'],
                                  user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('BoatsStore'))
    else:
        return render_template('addBoatCompany.html', kps_pks=kps_pks)

########
# Edit Boat Category


@app.route('/BoatsStore/<int:pkid>/edit', methods=['POST', 'GET'])
def editBoatCategory(pkid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editedBoat = session.query(BoatCompanyName).filter_by(id=pkid).one()
    creator = getUserInfo(editedBoat.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Boat Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('BoatsStore'))
    if request.method == "POST":
        if request.form['name']:
            editedBoat.name = request.form['name']
        session.add(editedBoat)
        session.commit()
        flash("Boat Category Edited Successfully")
        return redirect(url_for('BoatsStore'))
    else:
        # kps_pks is global variable we can them in entire application
        return render_template('editBoatCategory.html',
                               pk=editedBoat, kps_pks=kps_pks)

######
# Delete Boat Category


@app.route('/BoatsStore/<int:pkid>/delete', methods=['POST', 'GET'])
def deleteBoatCategory(pkid):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    pk = session.query(BoatCompanyName).filter_by(id=pkid).one()
    creator = getUserInfo(pk.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Boat Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('BoatsStore'))
    if request.method == "POST":
        session.delete(pk)
        session.commit()
        flash("Boat Category Deleted Successfully")
        return redirect(url_for('BoatsStore'))
    else:
        return render_template('deleteBoatCategory.html',
                               pk=pk, kps_pks=kps_pks)

######
# Add New Boat Name Details


@app.route('/BoatsStore/addCompany/addBoatDetails/<string:pkname>/add',
           methods=['GET', 'POST'])
def addBoatDetails(pkname):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    kpk = session.query(BoatCompanyName).filter_by(name=pkname).one()
    # See if the logged in user is not the owner of boat
    creator = getUserInfo(kpk.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBoats', pkid=kpk.id))
    if request.method == 'POST':
        name = request.form['name']
        year = request.form['year']
        color = request.form['color']
        capacity = request.form['capacity']
        area = request.form['area']
        volume = request.form['volume']
        boatdetails = BoatName(name=name, year=year,
                               color=color, capacity=capacity,
                               area=area,
                               volume=volume,
                               date=datetime.datetime.now(),
                               boatcompanynameid=kpk.id,
                               user_id=login_session['user_id'])
        session.add(boatdetails)
        session.commit()
        return redirect(url_for('showBoats', pkid=kpk.id))
    else:
        return render_template('addBoatDetails.html',
                               pkname=kpk.name, kps_pks=kps_pks)

######
# Edit Boat details


@app.route('/BoatsStore/<int:pkid>/<string:pkename>/edit',
           methods=['GET', 'POST'])
def editBoat(pkid, pkename):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    pk = session.query(BoatCompanyName).filter_by(id=pkid).one()
    boatdetails = session.query(BoatName).filter_by(name=pkename).one()
    # See if the logged in user is not the owner of boat
    creator = getUserInfo(pk.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBoats', pkid=pk.id))
    # POST methods
    if request.method == 'POST':
        boatdetails.name = request.form['name']
        boatdetails.year = request.form['year']
        boatdetails.color = request.form['color']
        boatdetails.capacity = request.form['capacity']
        boatdetails.area = request.form['area']
        boatdetails.volume = request.form['volume']
        boatdetails.date = datetime.datetime.now()
        session.add(boatdetails)
        session.commit()
        flash("Boat Edited Successfully")
        return redirect(url_for('showBoats', pkid=pkid))
    else:
        return render_template('editBoat.html',
                               pkid=pkid, boatdetails=boatdetails,
                               kps_pks=kps_pks)

#####
# Delte Boat Edit


@app.route('/BoatsStore/<int:pkid>/<string:pkename>/delete',
           methods=['GET', 'POST'])
def deleteBoat(pkid, pkename):
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    pk = session.query(BoatCompanyName).filter_by(id=pkid).one()
    boatdetails = session.query(BoatName).filter_by(name=pkename).one()
    # See if the logged in user is not the owner of boat
    creator = getUserInfo(pk.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You can't delete this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showBoats', pkid=pk.id))
    if request.method == "POST":
        session.delete(boatdetails)
        session.commit()
        flash("Deleted Boat Successfully")
        return redirect(url_for('showBoats', pkid=pkid))
    else:
        return render_template('deleteBoat.html',
                               pkid=pkid, boatdetails=boatdetails,
                               kps_pks=kps_pks)

####
# Logout from current user


@app.route('/logout')
def logout():
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type': 'application/x-www-form-urlencoded'}
                  )[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully'
                                            'disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#####
# Json


@app.route('/BoatsStore/JSON')
def allBoatsJSON():
    boatcategories = session.query(BoatCompanyName).all()
    category_dict = [c.serialize for c in boatcategories]
    for c in range(len(category_dict)):
        boats = [i.serialize for i in session.query(
                 BoatName).filter_by
                 (boatcompanynameid=category_dict[c]["id"]).all()]
        if boats:
            category_dict[c]["boat"] = boats
    return jsonify(BoatCompanyName=category_dict)

####


@app.route('/boatsStore/boatCategories/JSON')
def categoriesJSON():
    boats = session.query(BoatCompanyName).all()
    return jsonify(boatCategories=[c.serialize for c in boats])

####


@app.route('/boatsStore/boats/JSON')
def itemsJSON():
    items = session.query(BoatName).all()
    return jsonify(boats=[i.serialize for i in items])

#####


@app.route('/BoatsStore/<path:boatcompanyname>/boats/JSON')
def categoryitemsJSON(boatcompanyname):
    boatCompanyName = session.query(BoatCompanyName).filter_by(
        name=boatcompanyname).one()
    boats = session.query(BoatName).filter_by(
        boatcompanyname=boatCompanyName).all()
    return jsonify(boatCompanyName=[i.serialize for i in boats])

#####


@app.route('/BoatsStore/<path:boatcompanyname>/<path:edition_name>/JSON')
def ItemJSON(boatcompanyname, edition_name):
    boatCompanyName = session.query(BoatCompanyName).filter_by(
        name=boatcompanyname).one()
    boatEdition = session.query(BoatName).filter_by(
        name=edition_name, boatcompanyname=boatCompanyName).one()
    return jsonify(boatEdition=[boatEdition.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
