
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Image(db.Model):
    """Images."""

    __tablename__ = "images"

    def __repr__(self):
        """Show metadata about the image."""

        return "<Image filesize={} xdim={} ydim={} imgtype={} uploaded={} url={}>".format(self.filesize, self.xdim, self.ydim, self.imgtype, self.uploaded, self.url)

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    filesize = db.Column(db.Integer)
    xdim = db.Column(db.Integer)
    ydim = db.Column(db.Integer)
    imgtype = db.Column(db.String(8))
    uploaded = db.Column(db.DateTime(timezone=True))
    url = db.Column(db.String(2083), unique=True)


def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database.
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///imgdatabase'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    from server import app
    connect_to_db(app)
