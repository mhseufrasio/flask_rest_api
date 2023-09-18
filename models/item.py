from db import db


class ItemModel(db.Model):
    __tablename__ = "itens"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    description = db.Column(db.String(250))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)

    store = db.relationship("StoreModel", back_populates="itens")
    tags = db.relationship("TagModel", back_populates="itens", secondary="itens_tags")