from app import db
from app.exceptions import NotFound


class Model(db.Model):
    __abstract__ = True

    # Return a model instance by id
    @classmethod
    def get(cls, id):
        model = cls.query.get(id)
        if model:
            return model
        raise NotFound

    # Return all model instances
    @classmethod
    def get_all(cls, owner_id=None):
        if owner_id:
            return cls.query.filter_by(account_id=owner_id).all()
        return cls.query.all()

    # Create a new model instance and save it to the database
    def create(self):
        db.session.add(self)
        self.save()
        return self

    # Save changes to the database
    def save(self):
        db.session.commit()
        return self

    # Delete the model instance from the database
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    # Return a dictionary representation of the model instance
    def to_dict(self, include=[], exclude=[]):
        _dict = {}
        for c in self.__table__.columns:
            if c.name not in exclude or c.name in include:
                _dict[c.name] = getattr(self, c.name)
        return _dict
