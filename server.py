from flask import Flask, render_template, redirect, url_for, session, request
from random import randrange
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def index():
   if 'gold' not in session:
        session['gold'] = 0

   if 'activites' not in session:
        session['activites'] = []

   #sort activites
   sorted_activites = sorted(session['activites'], key=lambda log: log['creationTime'] ,reverse=True)

   return render_template('index.html', activites=sorted_activites)

@app.route('/process_money', methods=['POST'])
def process_money():
   building = request.form.get('building')
   min_gold = request.form.get('min')
   max_gold = request.form.get('max')

   #random random number within range
   earned_gold = randrange(int(min_gold), int(max_gold))
   color = 'green' if earned_gold > 0 else 'red'

   now = datetime.now()  
   current_time = now.strftime("%Y-%m-%d %H:%M:%S")
   
   active_log = {'building' :building,'earnedGold': earned_gold, 
                 'color':  color, 'creationTime': current_time}
   
   #Update Session
   session['gold'] += earned_gold
   session['activites'].append(active_log)
   print("session['activites']" , session['activites'])

   #Redirect back to index page
   return redirect('/')


@app.route('/reset', methods=['POST'])
def reset():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)