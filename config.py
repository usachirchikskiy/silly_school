ACHIEVEMENT_FILE_SEND = "/photos/achievement_photos/"
ADMINISTRATION_FILE_SEND = "/photos/administration_photos/"
DEPARTMENT_FILE_SEND = "/photos/department_photos/"
NEWS_FILE_SEND = "/photos/news_photos/"
TEACHER_FILE_SEND = "/photos/teacher_photos/"
GALLERY_FILE_SEND = "/photos/gallery_photos/"

class Config:
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/silly_school'
    UPLOAD_FOLDER_ACHIEVEMENT = 'photos/achievement_photos/'
    UPLOAD_FOLDER_ADMINISTRATION = 'photos/administration_photos/'
    UPLOAD_FOLDER_GALLERY = 'photos/gallery_photos/'
    UPLOAD_FOLDER_DOCUMENT = 'files/document_files/'
    UPLOAD_FOLDER_NEWS = 'photos/news_photos/'
    UPLOAD_FOLDER_TEACHER = 'photos/teacher_photos/'
    UPLOAD_FOLDER_TEACHER_TIMETABLE = 'files/teacher_timetable/'
    UPLOAD_FOLDER_DEPARTMENT = 'photos/department_photos/'
    NEWS_PER_PAGE = 5
    GALLERY_PER_PAGE = 6
    SECRET_KEY = 'a23c36266d504b8d84e99bb58c150786'

# HOME_FOLDER = "/C:/Users/usmon/PycharmProjects/silly_school/"