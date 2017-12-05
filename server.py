from PIL import Image as pillow

from flask import Flask
from flask import make_response, render_template, redirect, request

import os
import urllib2

import datetime

from model import connect_to_db, db
from model import Image

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World!"


# GET routes
@app.route("/v1/image")
def display_metadata():
    """List metadata for stored images."""
    images = Image.query.all()
    return render_template('images_metadata.html', images=images)

@app.route("/v1/image/<int:img_id>")
def display_img_metadata(img_id):
    """View metadata about image with id <id> ."""
    image = Image.query.get(img_id)
    return render_template('image_metadata.html', image=image)

@app.route("/v1/image/<int:img_id>/data")
def display_image(img_id):
    """View image with id <id> .
    optional parameter: bbox=<x>,<y>,<w>,<h> to get a cutout of the image.
    """
    image = Image.query.get(img_id)
    return render_template('image_view.html', image=image)

# POST routes
@app.route("/v1/image", methods=['POST'])
def upload_image():
    """Upload new image. Request body should be image data."""
    url = request.form.get('image', '')

    image = get_image_data(url)

    try:
        db.session.add(image)
        db.session.commit()
    except:
        print('Duplicate image')

    return render_template('image_metadata.html', image=image)

# PUT routes
@app.route("/v1/image/<int:img_id>", methods=['POST'])
def update_image(img_id):
    """Update image. Request body should be image data."""
    url = request.form.get('image', '')

    image = Image.query.filter_by(id=img_id).first()

    if not image:
        image = get_image_data(url)
        db.session.add(image)
    else:
        image.url = url
        db.session.merge(image)

    try:
        db.session.commit()
    except:
        print('Update could not be saved')

    return render_template('image_metadata.html', image=image)


@app.errorhandler(403)
def not_auth(error):
    resp = make_response(render_template('error/403.html'), 403)
    resp.headers['X-Something'] = 'A value'
    return resp

@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error/404.html'), 404)
    resp.headers['X-Something'] = 'A value'
    return resp


def get_image_data(url):
    """Create image instance from url, including metadata from pillow."""

    response = urllib2.urlopen(url)

    try:
        image_res = pillow.open(response)
    except:
        print('Error')

    ext = image_res.format
    xdim, ydim = image_res.size

    meta = response.info()
    size = int(meta.get(name="Content-Length"))

    return Image(filesize=size, xdim=xdim, ydim=ydim, imgtype=ext, uploaded=datetime.datetime.now(), url=url)


if __name__ == "__main__":

    from flask_debugtoolbar import DebugToolbarExtension
    DebugToolbarExtension(app)

    connect_to_db(app, os.environ.get("DATABASE_URL"))
    db.create_all()

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
