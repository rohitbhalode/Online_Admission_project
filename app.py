from flask import flash,Flask,render_template,request,redirect,session,jsonify,url_for
from cat import UniqueID
from database import insert_data,login_validation,upload_image,registered,update_pass,update_data,get_image_database,submit
from mail import send_otp
from bson.binary import Binary
import io
app=Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'


app.config['user_data']=None

@app.route('/')
def welcome():
    return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if 'user' in session  :

        # User is already logged in, redirect them to the profile page.
        active_tab = request.args.get('active_tab','personal')
        print('login',active_tab) 
        print('User is already logged in,',session['user'] ) 
        user_data=login_validation(session['user'] , session['Password'])
        app.config['user_data']=user_data
        if user_data['form_status']=="Submitted":
            return render_template('form_submited.html')
        else:
            return render_template('student_profile.html', user_data=user_data,active_tab=active_tab)

    if request.method == 'POST':
        Username = request.form.get("username")
        Password = request.form.get("password")
        print('Username',Username)
        user_data=login_validation(Username, Password)
        # user_data=user_data.upper()
        # session['user_data'] = user_data
        app.config['user_data']=user_data
        # print(app.config['user_data'] ) 
        if user_data:
            active_tab = request.args.get('active_tab', 'personal')
            print(active_tab) 
            
            session['user'] = Username
            session['Password'] = Password

            print(session['user']) 
            print(user_data['form_status'])  

            # print(session.get('email')) 


            if user_data['form_status']=="Submitted":
                return render_template('form_submited.html')
            else:
                return render_template('student_profile.html', user_data=user_data,active_tab=active_tab)
        else:
            return "Please wait our Database is having connection issue wait for some time... "

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register1.html')

@app.route("/submit1", methods=['POST'])
def result():
  
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
      return "Our site is getting due to much user please refresh  "
      
  else:
    flash("Unsuccessful ")  
    return redirect('/register')
  

 

@app.route("/logout")
def logout():
#   print(session['email'] ) 
  session.pop('user', None)
    # Redirect to the login or home page (replace '/login' with the appropriate URL)
  return redirect("/login")


@app.route('/save', methods=['POST','GET'])
def save_data():
    print('we are in save button ')
    data = request.form  # This will contain the form data from the POST request
    # Process and save the data as needed (e.g., store it in a database)
    # You can return a response, but for now, let's just return a success message
    active_tab=data['tabName']
    
    if data['tabName']=='document':
        if 'image1' in request.files:
            image0 = request.files['image0']
            image1 = request.files['image1']
            image2 = request.files['image2']
            image3 = request.files['image3']
            image4 = request.files['image4']
            image5 = request.files['image5']


            data = {
                        'User': session['user'],
                        'image0': Binary(image0.read()),
                        'image1': Binary(image1.read()),
                        'image2': Binary(image2.read()),
                        'image3': Binary(image3.read()),
                        'image4': Binary(image4.read()),
                        'image5': Binary(image5.read())
}
            # image_name = request.form['image_name']
            upload_image(data)

    # if data['tabName']=='personal':        
            
    else: 
        for i in data:
            print (i,data[i])
        # print('sess ',session['user_data'] ) 
        print('sess ',session['user'] )    
        update_data(session['user'],data)
    return render_template('student_profile.html', user_data=session.get('user_data'),active_tab=active_tab)




@app.route("/send", methods=['GET'])
def send():
    email = request.args.get('email')
       
    if  email:
        if registered(email):
            
        
            return '', 999
        else:
            session['email'] = email
        
    otpcode = send_otp(session['email'])
    print(otpcode)
    
    session['otpcode'] = otpcode
    return "Verification Successful"


@app.route("/send2", methods=['GET'])
def send2():
    email = request.args.get('email')
    print('email in send2',email)   
    
    if registered(email):
        session['email'] = email
        session['otpcode'] = send_otp(session['email'])
       
        return '', 200
    else:
        print('user is not registered') 
        print("UnSuccesful")
        return  '', 403 
             
    
        
    
    
    
    

@app.route('/verify_code', methods=['POST'])
def verify_verification_code():
    # Get the code from the request as JSON
    code = request.json.get('code')
    stored_otpcode = session.get('otpcode')
    
    # Check the code (you should implement this logic)
    if code == stored_otpcode:
        print("code is correct")
        return '', 200  # Code is correct, return a 200 status code
    else:
        print("code is not correct")
        return '', 403  # Code is incorrect, return a 403 status code



@app.route('/password_reset')
def password_reset():
    return render_template('password_reset.html')


@app.route('/update_password', methods=["POST"])
def update_password():
    if request.method=='POST':
        password =  request.form.get('password')
        print(session['email'])
        user=session['email']
        update_pass(user,password)
    return render_template('success1.html')




@app.route('/get_image/<image_id>',methods=["POST","GET"])
def get_image(image_id):
    # Retrieve the image binary data from MongoDB
    
    print('Image ID:', image_id)
    print('Email:', session['user'])
    # get_image_database(image_id,email)  
    return get_image_database(image_id,session['user'])
    
@app.route('/confirmation')
def confirmation():
    # Retrieve user data from your database or session
    user_data = login_validation(session['user'], session['Password'])
    return render_template('confirmation_page.html', user_data=user_data)


@app.route('/submitted')
def submitted():
    submit(session['user'])
    user_data = login_validation(session['user'], session['Password'])
    print('length', len(user_data))
    return render_template('form_submited.html')


if __name__=='__main__':
    
    app.run(debug=True)