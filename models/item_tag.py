from db import db

class ItensTagsModel(db.Model):
    __tablename__ = "itens_tags"

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("itens.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))