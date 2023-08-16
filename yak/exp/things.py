"""
>>> s = Thing.dog.new(name='spike')
>>> s
dog.(name: 'spike')
>>> Thing.cat
cat.()
>>>
"""

# TODO
# - Thing.dog.all
# - Thing.dog.find_one
# - Thing.dog.find_many
# - nested "Thing"(s) linked by reference
# - replace pickle (json?)
# - configurable store
#   - fs?
#   - sqlite?
#   - fs backed triplet store?

import nanoid
import pickle
import time

STORE_DIR = '/tmp/'


class Things(type):
    def __new__(meta, name, bases, class_dict):
        return type.__new__(meta, name, bases, class_dict)

    def __getattribute__(self, tag):
        return Record(tag)

class Thing(metaclass=Things):
    pass


class Record:
    def __init__(self, tag):
        self.tag = tag
        self.slots = []

    def new(self, **fields):
        self.uid = nanoid.generate()
        self._initialize_fields(fields)
        return self

    def all(self):
        # load all records with self.tag and return them as a list
        pass

    def find_one(self, **query):
        # return the first record with self.tag that matches query
        pass

    def find_many(self, **query):
        # return all records with self.tag that match query
        pass

    def __eq__(self, other):
        if not isinstance(other, Thing):
            return False
        return self.uid == other.uid

    def __repr__(self):
        def show(slot):
            value = getattr(self, slot)
            return f'{slot}: {repr(value)}' 

        fields = ', '.join(show(slot) for slot in self.slots)
        return f'{self.tag}.({fields})'

    def _initialize_fields(self, fields):
        for k, v in fields.items():
            self.slots.append(k)
            setattr(self, 'updated_at', int(time.time() * 1000))
            setattr(self, k, v)
            self._persist()

    def _persist(self):
        pathname = f'{STORE_DIR}/{self.tag}-{self.uid}.p' 
        with open(pathname, 'wb') as f:
            pickle.dump(self.__dict__, f)

