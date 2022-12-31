from webconnect import app,db

# Connection Data Model
class ConnectionDB(db.Model):
    __bind_key__ = 'connectiondb'
    id = db.Column(db.Integer,primary_key=True)
    connection_name = db.Column(db.String(15),nullable=False)
    address = db.Column(db.String(20))
    protocol = db.Column(db.String(10),nullable=False)
    parameters = db.Column(db.String(100),nullable=True)
