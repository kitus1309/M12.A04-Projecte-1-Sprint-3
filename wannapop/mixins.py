from . import db_manager as db

class BaseMixin():
    
    @classmethod
    def create(cls, **kwargs):
        r = cls(**kwargs)
        return r.save()

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self.save()
    
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            return False
        
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except:
            return False

    @classmethod
    def get(cls, id):
        return db.session.query(cls).get(id)
    
    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_filtered_by(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).one_or_none()

    @classmethod
    def get_all_filtered_by(cls, **kwargs):
        return db.session.query(cls).filter_by(**kwargs).order_by(cls.id.asc()).all()

    @classmethod
    def get_with(cls, id, join_cls):
        return db.session.query(cls, join_cls).join(join_cls).filter(cls.id == id).one_or_none()

    @classmethod
    def get_all_with(cls, join_cls):
        return db.session.query(cls, join_cls).join(join_cls).order_by(cls.id.asc()).all()

from collections import OrderedDict
from sqlalchemy.engine.row import Row

class SerializableMixin():

    exclude_attr = []

    def to_dict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            if key not in self.__class__.exclude_attr:
                result[key] = getattr(self, key)
        return result

    @staticmethod
    def to_dict_collection(collection):
        result = []
        for x in collection:  
            if (type(x) is Row):
                obj = {}
                first = True
                for y in x:
                    if first:
                        # model
                        obj = y.to_dict()
                        first = False
                    else:
                        # relationships
                        key = y.__class__.__name__.lower()
                        del obj[key + '_id']
                        obj[key] = y.to_dict()
                result.append(obj)
            else:
                # only model
                result.append(x.to_dict())
        return result