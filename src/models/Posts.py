from main import db


class Posts(db.Model):
	__tablename__ = "posts"

	id = db.Column(db.Integer, primary_key=True)


	def __repr__(self):
		return f"<Book {self.title}>"