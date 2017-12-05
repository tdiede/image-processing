GET /v1/image
List metadata for stored images.
GET /v1/image/<id>
View metadata about image with id <id> .
GET /v1/image/<id>/data
View image with id <id> .
Optional GET parameter: bbox=<x>,<y>,<w>,<h> to get a cutout of the image

POST /v1/image
Upload new image. Request body should be image data.

PUT /v1/image/<id>
Update image. Request body should be image data.

Image metadata
Image metadata should be the following fields:

Filesize of the image
Image dimensions
Image type (gif, jpg etc)
Date/time image was uploaded
Extra fields of your choice

It is up to you how you want to represent the image metadata in your API.