import os.path

from web import db


class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, unique=True, nullable=False)
    pdf_path = db.Column(db.String, unique=True, nullable=False)
    cat_path = db.Column(db.String, unique=True)
    task_id = db.Column(db.String, unique=True)

    def __repr__(self):
        return f"<Paper {self.id} {self.title} {self.pdf_path} {self.cat_path} {self.task_id}>"

    def set_task_id(self, task_id):
        self.task_id = task_id
        db.session.add(self)
        db.session.commit()

    def set_cat_path(self, cat_path):
        self.cat_path = cat_path
        db.session.add(self)
        db.session.commit()

    @property
    def has_cat(self):
        try:
            has_cat = os.path.isfile(self.cat_path)
        except TypeError:
            has_cat = False
        return has_cat

    @property
    def has_pdf(self):
        try:
            has_pdf = os.path.isfile(self.pdf_path)
        except TypeError:
            has_pdf = False
        return has_pdf
