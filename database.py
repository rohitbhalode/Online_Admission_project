from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


import bcrypt

Database_URL='mysql+mysqlconnector://dhtzrvctzv9jmljjn6b3:pscale_pw_i7L4DOMdEQlBwcdYw8FXPMLqcLSAatht8VJdqK2GbVU@aws.connect.psdb.cloud/project_database'

engine=create_engine(Database_URL)

Session=sessionmaker(bind=engine)
session=Session()
Base=declarative_base()

class User(Base):
    __tablename__='registration'
    F_name=Column(String(25))
    L_name=Column(String(25))
    Mobile_NO=Column(String(10))
    email=Column(String(25),primary_key=True)
    Registration_Id=Column(String(8))
    Password=Column(String(100))

    

def insert_data(l,a):
    try:
        pwd=bytes(l[5],'utf-8')
        hashed=bcrypt.hashpw(pwd,bcrypt.gensalt())
        new_User=User(F_name=l[0].upper(),L_name=l[1].upper(),Mobile_NO=l[2],email=l[3],Registration_Id=a,Password=hashed)
        session.add(new_User)
        session.commit()
        session.close()
    except Exception as e:
    # Handle the exception or log it as needed
        print(f"An error occurred: {e}")
        
        # Rollback the current transaction to clean up
        session.rollback() 
        return False  
    return True 



def login_validation(Username, Password):
    try:
        user = session.query(User).filter(User.email == Username).first()
        session.close()
        
        
        stored_password=user.Password
        stored_password_bytes = stored_password.encode('utf-8')
        print(bcrypt.checkpw(Password.encode('utf-8'),stored_password_bytes))
        if bcrypt.checkpw(Password.encode('utf-8'),stored_password_bytes):
            return {"name" :user.F_name+" "+user.L_name,'id': user.Registration_Id}
        else :
            return False  
    except Exception as e:
        print(f"An error occurred2: {e}")   
        session.rollback()
        return False  
       
    
    
    
