from project.model import Gallery
from project.schema import ma

class GallerySchema(ma.SQLAlchemyAutoSchema): # convert DB object to Json

    class Meta:
        model = Gallery
        oredered = True