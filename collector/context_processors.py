import cloudinary
def consts(request):
    return dict(
        THUMBNAIL = {
            "class": "thumbnail inline", "format": "jpg", "crop": "fill", "height": 150, "width": 150,
        },
        CLOUDINARY_CLOUD_NAME = cloudinary.config().cloud_name
    )
