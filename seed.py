
import datetime

import os
# Whenever seeding, drop existing database and create a new database.
os.system("dropdb imgdatabase")
print("dropdb imgdatabase")
os.system("createdb imgdatabase")
print("createdb imgdatabase")


from server import app

from model import connect_to_db, db
from model import Image


def load_example_images():
	"""Load a few example images into the database."""

	print("Images")

	Image.query.delete()

	images = [
    	Image(filesize=800, xdim=1200, ydim=1080, imgtype='jpg', uploaded=datetime.datetime.now(), url='https://res.cloudinary.com/demo/image/upload/Sample.jpg'),
    	Image(filesize=400, xdim=300, ydim=200, imgtype='jpg', uploaded=datetime.datetime.now(), url='http://cdn3.craftsy.com/blog/wp-content/uploads/2015/03/Coneflower.png'),
    	Image(filesize=1000, xdim=1600, ydim=1280, imgtype='png', uploaded=datetime.datetime.now(), url='https://winblogs.azureedge.net/devices/2012/09/808sample.jpg'),
	    Image(filesize=600, xdim=800, ydim=600, imgtype='jpg', uploaded=datetime.datetime.now(), url='http://a4.pbase.com/g9/34/632434/2/150123376.gdGIYwbh.jpg')
	]

	for image in images:
		db.session.add(image)
		db.session.flush()

	db.session.commit()


if __name__ == "__main__":

	connect_to_db(app, os.environ.get("DATABASE_URL"))
	db.drop_all()
	db.create_all()
	load_example_images()
