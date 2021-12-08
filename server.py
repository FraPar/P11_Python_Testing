import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        return render_template('welcome.html',club=club, clubs=clubs, competitions=competitions)
    except IndexError:
        error = 'No email founded, please try again!'
        return render_template('index.html', error=error)

@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]

    CurrentDate = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

    if str(CurrentDate) < str(competition['date']):
        try:
            pointFactor = 1
            clubPoints = int(club['points'])/pointFactor
            placesRequired = int(request.form['places'])
            if placesRequired <= 12 and placesRequired > 0 and clubPoints >= placesRequired:
                placeCalculation = int(competition['numberOfPlaces'])-placesRequired
                if placeCalculation >= 0:
                    club['points'] = int(clubPoints*pointFactor - placesRequired*pointFactor)
                    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
                    flash('Great-booking complete!')
                else:
                    flash('There is not enough place for that many, sorry!')
            else:
                flash("Booking not complete! Places must be between 0 and 12 and under your current club's points.")
        except ValueError:
            flash('Please enter a number!')
    else:
        flash('The date of the competition is in the past')

    return render_template('welcome.html', club=club, competitions=competitions)

@app.route('/displayPoints/<club>')
def displayPoints(club):
    try:
        foundClub = [c for c in clubs if c['name'] == club][0]
        return render_template('points.html',club=foundClub, clubs=clubs)
    except IndexError:
        return render_template('points.html', clubs=clubs)

@app.route('/logout')
def logout():
    return redirect(url_for('index'))