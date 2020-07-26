"""This is where the Project schema is defined"""
import json

from sqlalchemy import Column, String, Integer

from src.database.persistence import db


class Project(db.Model):
    """
    Project
    a persistent Project entity, extends the base SQLAlchemy Model
    """

    __tablename__ = "project"
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True)
    # json string blob of array format
    meta = Column(String(300))
    description = Column(String(300))
    # Holds a cdn link
    image = Column(String(300))
    git_repo = Column(String(300))
    demo_link = Column(String(300))

    @property
    def to_json(self):
        """JSON form representation of the project model"""
        return {
            "id": self.id,
            "title": self.title,
            "meta": json.loads(self.meta),
            "description": self.description,
            "image": self.image,
            "git_repo": self.git_repo,
            "demo_link": self.demo_link,
        }

    def insert(self):
        """inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        Examples:
            TODO
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a new model into a database
            the model must exist in the database
            Examples:
                TODO
        """
        db.session.delete(self)
        db.session.commit()

    def update(self, title, meta, description, image, git_repo, demo_link):
        """updates a new model into a database
            the model must exist in the database
            Examples:
                TODO
        """
        self.title = title
        self.meta = json.dumps(meta)
        self.description = description
        self.image = image
        self.git_repo = git_repo
        self.demo_link = demo_link
        db.session.commit()

    def __repr__(self):
        return f"<Project title: {self.title}>"
