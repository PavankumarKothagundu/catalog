from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

engine = create_engine('sqlite:///boats.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete BoatCompanyName if exisitng.
session.query(BoatCompanyName).delete()
# Delete BoatName if exisitng.
session.query(BoatName).delete()
# Delete User if exisitng.
session.query(User).delete()

# Create sample users data
User1 = User(name="Pavankumar Kothagundu",
             email="pavankumarsince2000@gmail.com",
             picture='http://www.enchanting-costarica.com/wp-content/'
                     'uploads/2018/02/jcarvaja17-min.jpg')
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample boat companys
Company1 = BoatCompanyName(name="SEA RAY",
                           user_id=1)
session.add(Company1)
session.commit()

Company2 = BoatCompanyName(name="BAYLINER",
                           user_id=1)
session.add(Company2)
session.commit

Company3 = BoatCompanyName(name="MASTERCRAFT",
                           user_id=1)
session.add(Company3)
session.commit()

Company4 = BoatCompanyName(name="RANGER",
                           user_id=1)
session.add(Company4)
session.commit()

Company5 = BoatCompanyName(name="BOSTON WHALER",
                           user_id=1)
session.add(Company5)
session.commit()

Company6 = BoatCompanyName(name="MALIBU",
                           user_id=1)
session.add(Company6)
session.commit()

# Populare a boats with models for testing
# Using different users for boats names year also
Name1 = BoatName(name="REGAL 28 EXPRESS",
                 year="2016",
                 color="black",
                 capacity="15tonnes",
                 area="100sqft",
                 volume="1000m3",
                 motortype="wingfan",
                 stormpower="1000watt",
                 date=datetime.datetime.now(),
                 boatcompanynameid=1,
                 user_id=1)
session.add(Name1)
session.commit()

Name2 = BoatName(name="VIKING YACHTS 42 CONVERTIBLE",
                 year="2019",
                 color="blue",
                 capacity="20tonnes",
                 area="150sqft",
                 volume="2000m3",
                 motortype="steamer",
                 stormpower="10000watt",
                 date=datetime.datetime.now(),
                 boatcompanynameid=2,
                 user_id=1)
session.add(Name2)
session.commit()

Name3 = BoatName(name="GRAND BANKS 43 EU",
                 year="2018",
                 color="ash",
                 capacity="30tonnes",
                 area="200sqft",
                 volume="5000m3",
                 motortype="Electric",
                 stormpower="50000watt",
                 date=datetime.datetime.now(),
                 boatcompanynameid=3,
                 user_id=1)
session.add(Name3)
session.commit()

Name4 = BoatName(name="SEA RAY 450 SUNDANCER",
                 year="2017",
                 color="purple",
                 capacity="25tonnes",
                 area="250sqft",
                 volume="4000m3",
                 motortype="MagneticDisc",
                 stormpower="100000watt",
                 date=datetime.datetime.now(),
                 boatcompanynameid=4,
                 user_id=1)
session.add(Name4)
session.commit()

Name5 = BoatName(name="BACK COVE 34",
                 year="2014",
                 color="blue",
                 capacity="20tonnes",
                 area="500sqft",
                 volume="8000m3",
                 motortype="FuelBased",
                 stormpower="2000watt",
                 date=datetime.datetime.now(),
                 boatcompanynameid=5,
                 user_id=1)
session.add(Name5)
session.commit()

Name6 = BoatName(name="INTREPID 400 CUDDY",
                 year="2019",
                 color="white",
                 capacity="100tones",
                 area="250sqft",
                 volume="3000m3",
                 motortype="HydroPower",
                 stormpower="20000watt",
                 date=datetime.datetime.now(),
                 boatcompanynameid=6,
                 user_id=1)
session.add(Name6)
session.commit()

print("Your boat database has been inserted!")
