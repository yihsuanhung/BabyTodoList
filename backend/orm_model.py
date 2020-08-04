from app import db

class Todo(db.Model):
    __tablename__ = 'todolist_orm'

    uid = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200))
    status = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, uid, content, status):
        self.uid = uid
        self.content = content
        self.status = status

    def __repr__(self):
        return '<Task %r>' % self.uid
