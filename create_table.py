from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itertools import count

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:12345678@localhost/flask_ass'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.secret_key = 'login'

# cnt=count(start=1,step=1)

class User(db.Model):
        # __tablename__ = 'PRODUCT_MASTER'

        user_id = db.Column('User_Id',db.Integer(),primary_key= True)
        role = db.Column('Role', db.String(30))
        firstname = db.Column('First Name', db.String(30))
        lastname = db.Column('Last Name',db.String(30))
        contact = db.Column ('Contact',db.BigInteger())
        address = db.Column('Address', db.String(30))
        DOB = db.Column('DOB', db.String(30))
        age = db.Column('Age', db.Integer())
        emailid = db.Column('Email ID',db.String(30))
        password = db.Column('Password', db.String(30))
        conform_password = db.Column('Conform Password', db.String(30))
        gender = db.Column('Gender', db.String(30))
        country = db.Column('Country', db.String(30))
        city =db.Column('City',db.String(30))


class Product(db.Model):
        prod_S_NO = db.Column('S_No', db.Integer(),primary_key=True)
        product_id = db.Column('User_Id', db.Integer())
        name = db.Column('First Name', db.String(30))
        price = db.Column('Last Name', db.Float())
        quantity = db.Column('Contact', db.Integer())
        vendor = db.Column('Address', db.String(30))
        category = db.Column('DOB', db.String(30))

db.create_all()


if __name__=="__main__":
    app.run(debug=True,port=5000)