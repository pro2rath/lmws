from app import db

class Worker(db.Model):
    __tablename__ = 'workers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    contact = db.Column(db.String(15), unique=True, nullable=False)
    address = db.Column(db.String(255))
    skill = db.Column(db.String(100))  # e.g., Mason, Electrician, Plumber, etc.
    joined_date = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<Worker {self.name}>"
