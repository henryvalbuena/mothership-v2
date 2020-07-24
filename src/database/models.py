# import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

db = SQLAlchemy()
migrate = Migrate()


"""
Latte
a persistent Latte entity, extends the base SQLAlchemy Model
"""


class Latte(db.Model):
    __tablename__ = "latte"
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    ingredients = Column(String(300), nullable=False)

    def long(self):
        """long form representation of the Latte model"""
        return {
            "id": self.id,
            "title": self.title,
            "ingredients": json.loads(self.ingredients),
        }

    def insert(self):
        """inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        Examples:
            Latte = Latte(title=req_title, ingredients=req_ingredients)
            Latte.insert()
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a new model into a database
            the model must exist in the database
            Examples:
                Latte = Latte(title=req_title, ingredients=req_ingredients)
                Latte.delete()
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """updates a new model into a database
            the model must exist in the database
            Examples:
                Latte = Latte.query.filter(Latte.id == id).one_or_none()
                Latte.title = 'Black Coffee'
                Latte.update()
        """
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.long())
