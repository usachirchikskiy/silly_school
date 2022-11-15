from .AchievementRoute import achievement_bp
from .AdministrationRoute import administration_bp
from .AuthRoute import auth_bp
from .DepartmentRoute import department_bp
from .DocumentRoute import document_bp
from .FaqRoute import faq_bp
from .GalleryRoute import gallery_bp
from .NewsRoute import news_bp
from .ProfessionRoute import profession_bp
from .SchoolInfoRoute import school_info_bp
from .TeacherRoute import teacher_bp


def init_app(app):
    app.register_blueprint(achievement_bp)
    app.register_blueprint(administration_bp)
    app.register_blueprint(document_bp)
    app.register_blueprint(gallery_bp)
    app.register_blueprint(news_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(department_bp)
    app.register_blueprint(faq_bp)
    app.register_blueprint(school_info_bp)
    app.register_blueprint(profession_bp)
    app.register_blueprint(auth_bp)