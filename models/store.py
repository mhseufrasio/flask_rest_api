from ..db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Interger, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    itens = db.relationship("ItemModel", back_populates="store", lazy="dynamic")