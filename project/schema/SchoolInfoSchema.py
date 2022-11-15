from project.model.SchoolInfo import SchoolInfo
from project.schema import ma

class SchoolInfoSchema(ma.SQLAlchemyAutoSchema): # convert DB object to Json

    class Meta:
        model = SchoolInfo
        oredered = True