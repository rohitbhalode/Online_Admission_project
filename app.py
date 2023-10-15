from flask import flash,Flask,render_template,request,redirect,session,jsonify,url_for
from cat import UniqueID
from database import insert_data,login_validation
from mail import send_otp

app=Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'


@app.route('/')
def welcome():
    return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    user_data=None
    if 'user' in session:
        # User is already logged in, redirect them to the profile page.
        active_tab = request.args.get('active_tab', 'course')
        print('login',active_tab) 
        return render_template('student_profile.html', user_data=session.get('user_data'),active_tab=active_tab)

    if request.method == 'POST':
        Username = request.form.get("username")
        Password = request.form.get("password")
        session['user_data']=login_validation(Username, Password)
        # user_data=user_data.upper()
        print(user_data) 
        if session.get('user_data'):
            active_tab = request.args.get('active_tab', 'course')
            session['user'] = Username
            return render_template('student_profile.html', user_data=session.get('user_data'),active_tab=active_tab)
        else:
            return "Unsuccessful"

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register1.html')

@app.route("/submit1", methods=['POST'])
def result():
  print('Rohit') 
  if request.method=='POST':
    data = request.form.values()
    l=[i for i in data]
    print(l)
    a=UniqueID()
      
    a=a.Create_UniqueId()
    if insert_data(l,a):
        flash("Succesful")
        return render_template('success.html')
    else:
      flash("Unsuccessful with some exception")
      redirect('/register')
      
  else:
    flash("Unsuccessful ")  
    return redirect('/register')
  

 

@app.route("/logout")
def logout():
  session.pop('user', None)
    # Redirect to the login or home page (replace '/login' with the appropriate URL)
  return redirect("/login")


@app.route("/save", methods=['POST'])
def save_personal():
  form_value = list(request.form.values())
  print(form_value) 
  active_tab = request.form.get('active_tab','course')
  print(active_tab) 
  return redirect(url_for('login',active_tab=active_tab)) 


@app.route("/send", methods=['GET'])
def send():
    email = request.args.get('email')
    otpcode = send_otp(email)
    print(otpcode)
    print(email)
  
    session['otpcode'] = otpcode
    return "Verification Successful"


@app.route('/verify_code', methods=['POST'])
def verify_verification_code():
    # Get the code from the request as JSON
    code = request.json.get('code')
    stored_otpcode = session.get('otpcode')
    # Check the code (you should implement this logic)
    if code == stored_otpcode:
        return '', 200  # Code is correct, return a 200 status code
    else:
        return '', 403  # Code is incorrect, return a 403 status code


if __name__=='__main__':
    
    app.run(debug=True)