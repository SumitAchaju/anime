from django.conf import settings

BASE = settings.CLOUDINARY_BASE_UPLOAD_ROOT

if not BASE:
    raise AttributeError("CLOUDINARY_BASE_UPLOAD_ROOT must be set in settings")
if not BASE.endswith("/"):
    BASE += "/"

DEFAULT_TRANSFORMATIONS = {
    "width": 1200,
    "height": 1200,
    "crop": "fit",
}


class BaseCloudinaryUploadPreset:
    folder = BASE
    tags = ["flow"]
    transformation = DEFAULT_TRANSFORMATIONS

    def __init__(self, upload_to, transform=None, **kwargs):
        if transform is None:
            transform = {}
        self.folder += upload_to
        self.tags = [path for path in upload_to.split("/") if path] + self.tags
        if transform:
            self.transformation = self.generate_transformation(transform)
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get(self):
        cls = self.__class__

        # Start with class-level attributes
        custom_attrs = {
            k: v
            for k, v in cls.__dict__.items()
            if not k.startswith("__") and not callable(v)
        }
        # Add instance-level attributes
        custom_attrs.update(self.__dict__)

        return custom_attrs

    def generate_transformation(self, transform):
        transformation = self.transformation.copy()
        for k, v in transform.items():
            if k in transformation:
                transformation[k] = v
        return transformation


anime_thumbnail = BaseCloudinaryUploadPreset("anime/thumbnails").get()

profile_image = BaseCloudinaryUploadPreset(
    "profile", {"width": 500, "height": 500}
).get()
