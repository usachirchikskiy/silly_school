from project.model import Achievement
from project.schema import ma

class AchievementSchema(ma.SQLAlchemyAutoSchema): # convert DB object to Json

    class Meta:
        model = Achievement
        oredered = True