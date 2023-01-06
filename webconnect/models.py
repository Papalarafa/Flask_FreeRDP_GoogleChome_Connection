from webconnect import app,db

# Connection Data Model
class ConnectionDB(db.Model):
    __bind_key__ = 'connectiondb'
    id = db.Column(db.Integer,primary_key=True)
    connection_name = db.Column(db.String(15),nullable=False)
    address = db.Column(db.String(20))
    protocol = db.Column(db.String(10),nullable=False)

# FreeRDP Connection Database Model
class FreerdpDB(db.Model):
    __bind_key__ = 'freerdpdb'
    id = db.Column(db.Integer,primary_key=True)
    connection_name = db.Column(db.String(15),nullable=False)
    server = db.Column(db.String(20))
    restricadminmode = db.Column(db.Boolean)
    resolutionfullscreen = db.Column(db.Boolean,default=True)
    resolutionmultimon = db.Column(db.Boolean,default=False)
    resolutionspan = db.Column(db.Boolean,default=False)
    secnla = db.Column(db.Boolean,default=False)
    secrdp = db.Column(db.Boolean,default=False)
    sectls = db.Column(db.Boolean,default=False)
    floatbar = db.Column(db.Boolean,default=True)
    networkconnectiontype = db.Column(db.String(10))