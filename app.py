from flask import flash,Flask,render_template,request,redirect,session,jsonify,url_for
from cat import UniqueID
from database import insert_data,login_validation,upload_image,registered,update_pass,update_data,get_image_database,submit
from mail import send_otp
from bson.binary import Binary
from logger_config import logger
import io
app=Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key_here'




@app.route('/')
def welcome():
    return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    
    if 'user' in session  :

        # User is already logged in, redirect them to the profile page.
        active_tab = request.args.get('active_tab','personal')
        
        app.logger.info('User is in session reloading the page.')
        
        
        user_data=login_validation(session['user'] , session['Password'])
        app.config['user_data']=user_data
        if user_data['form_status']=="Submitted":
            return render_template('form_submited.html')
        else:
            return render_template('student_profile.html', user_data=user_data,active_tab=active_tab)

    if request.method == 'POST':
        Username = request.form.get("username")
        Password = request.form.get("password")
        
        user_data=login_validation(Username, Password)
        # user_data=user_data.upper()
        # session['user_data'] = user_data
        app.logger.info(f'User: {Username} is login to server ')
        
        if user_data:
            active_tab = request.args.get('active_tab', 'personal')
            
            
            session['user'] = Username
            session['Password'] = Password

            
             

            

            if user_data['form_status']=="Submitted":
                app.logger.info(f'User: {Username} is logged to server and form_status is submitted  ')
                return render_template('form_submited.html')
            else:
                app.logger.info(f'User: {Username} is successfully logged to server and form_status is not submitted  ')

                return render_template('student_profile.html', user_data=user_data,active_tab=active_tab)
        else:
            app.logger.error(f'There is database exception in login_validation funtion')
            
            return "Please wait our Database is having connection issue wait for some time... "

    return render_template('login.html')

@app.route('/register')
def register():
    app.logger.info('New Registration form is opened. ')

    return render_template('register1.html')

@app.route("/submit1", methods=['POST'])
def result():
  
  if request.method=='POST':
    data = request.form.values()
    l=[i for i in data]
    # print(l)
    a=UniqueID()
      
    id=a.Create_UniqueId()
    if insert_data(l,id):
        app.logger.info(f'New Registration Id has been created {id}. ')
        
        return render_template('success.html')
    else:
        app.logger.info(f'Database timeout error occur not critical refreshing the page will normalize . ')
        return "Our site is getting due to much user please refresh  "
      
  else:
    
    return redirect('/register')
  

 

@app.route("/logout")
def logout():
#   print(session['email'] )
    user=session['user']
    app.logger.debug(f'The user is getting logout from session {user}.')
      
    session.pop('user', None)
    # Redirect to the login or home page (replace '/login' with the appropriate URL)
    return redirect("/login")


@app.route('/save', methods=['POST','GET'])
def save_data():
    app.logger.info(f'The data is saving as saved button clicked')

    data = request.form  # This will contain the form data from the POST request
    # Process and save the data as needed (e.g., store it in a database)
    # You can return a response, but for now, let's just return a success message
    active_tab=data['tabName']
    app.logger.debug(f'The data is saving for tab {active_tab}')
    
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
                        'image5': Binary(image5.read())}

            # image_name = request.form['image_name']
            upload_image(data)

    # if data['tabName']=='personal':        
            
    else: 
        update_data(session['user'],data)
    return render_template('student_profile.html', user_data=session.get('user_data'),active_tab=active_tab)




@app.route("/send", methods=['GET'])
def send():
    email = request.args.get('email')
    app.logger.info(f'The send button for registration has clicked for sending otpcode to {email} ')
       
    if  email:
        if registered(email):
            app.logger.info(f'{email} is registered email')

            return '', 999
        else:
            app.logger.info(f'{email} is not registered email')

            session['email'] = email
            otpcode = send_otp(email)
            session['otpcode'] = otpcode
            app.logger.debug(f'The otpcode has been sent to {email} is {otpcode} ')
    else:
        flash("Please enter email ID")
        app.logger.debug(f'Email is not given')

    
    return "Email sent Successful"


@app.route('/password_reset')
def password_reset():
    app.logger.info(f'The user has opened a password reset form ')

    return render_template('password_reset.html')

@app.route("/send2", methods=['GET'])
def send2():
    email = request.args.get('email')
    app.logger.info(f'The send button for password reset is clicked for sending otpcode to {email} ')
    if registered(email):
        app.logger.info(f'The  {email} is registered user ')

        session['email'] = email
        session['otpcode'] = send_otp(session['email'])
        return '', 200
    else:
        app.logger.info(f'{email} is not registered email id  ')
        return  '', 403 
             

    

@app.route('/verify_code', methods=['POST'])
def verify_verification_code():
    # Get the code from the request as JSON
    code = request.json.get('code')
    stored_otpcode = session.get('otpcode')
    app.logger.debug(f'The Code enter by user is {code} and code sent to user is {stored_otpcode}.')
    
    # Check the code (you should implement this logic)
    if code == stored_otpcode:
        app.logger.info("The verification is successfull")

        return '', 200  # Code is correct, return a 200 status code
    else:
        app.logger.info("The verification is Unsuccessfull")

        return '', 403  # Code is incorrect, return a 403 status code





@app.route('/update_password', methods=["POST"])
def update_password():
    if request.method=='POST':
        password =  request.form.get('password')
        app.logger.info("The password is getting update")

        user=session['email']
        update_pass(user,password)
        app.logger.info("The password is updated successfully")
    return render_template('success1.html')




@app.route('/get_image/<image_id>',methods=["POST","GET"])
def get_image(image_id):
    # Retrieve the image binary data from MongoDB
    
    print('Image ID:', image_id)
    print('Email:', session['user'])
    app.logger.info(f"User is watching image {image_id}")
    # get_image_database(image_id,email)  
    return get_image_database(image_id,session['user'])
    
@app.route('/confirmation')
def confirmation():
    # Retrieve user data from your database or session
    app.logger.info(f"Details are confirming. ")

    user_data = login_validation(session['user'], session['Password'])
    return render_template('confirmation_page.html', user_data=user_data)


@app.route('/submitted')
def submitted():
    
    user_data = login_validation(session['user'], session['Password'])
    
    if len(user_data)==34:
        submit(session['user'])
        app.logger.info(f"Form is submitted successfully")

        return render_template('form_submited.html')
    else :
        flash('Please save all the details!', 'success')
        return render_template('confirmation_page.html', user_data=user_data)



if __name__=='__main__':
    
    app.run(debug=True)