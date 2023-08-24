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
import os
import pathlib
import pickle
import re
import time

STORE_DIR = '/tmp/'


class FileBackedStorage:
    INSTANCE = None

    def __init__(self, directory):
        self.db = pathlib.Path(directory)

    def read(self, uid):
        pattern = f'.*-{uid}.p'
        matching_files = [name for name in os.listdir(self.db) if re.match(pattern, name)]
        return self._read_from_file(matching_files[0])

    def find_all(self, tag):
        pattern = f'{tag}-.*.p'
        return [
            self._read_from_file(name)
            for name
            in os.listdir(self.db)
            if re.match(pattern)
        ]

    def _read_from_file(self, pathname):
        instance_dict = pickle.load(pathname)

    def write_to_file(self, pathname):
        pass

    @classmethod
    def instance(cls, directory):
        if cls.INSTANCE is None:
            cls.INSTANCE = cls(directory)
        return cls.INSTANCE

class Things(type):
    def __new__(meta, name, bases, class_dict):
        return type.__new__(meta, name, bases, class_dict)

    def __getattribute__(self, tag):
        return RecordManager(tag)


class Thing(metaclass=Things):
    pass


class RecordManager:
    def __init__(self, tag):
        self.tag = tag

    def __call__(self, **slots):
        return Record(uid, tag, **slots)

    def all(self):
        # load all records with self.tag and return them as a list
        pass

    def find_one(self, **query):
        # return the first record with self.tag that matches query
        pass

    def find_many(self, **query):
        # return all records with self.tag that match query
        pass


class Record:
    def new(self, uid, tag, **slots):
        self.uid = uid
        self.tag = tag
        self._initialize_slots(slots)
        return self

    def __eq__(self, other):
        if not isinstance(other, Record):
            return False
        return self.uid == other.uid

    def __repr__(self):
        def show(slot):
            value = getattr(self, slot)
            return f'{slot}: {repr(value)}'

        slots = ', '.join(show(slot) for slot in self.slots)
        return f'{self.tag}.({slots})'

    def _initialize_slots(self, slots):
        for slot_name, slot_value in slots.items():
            self._initialize_slot(name, value)

    def _initialize_slot(self, name, value):
        self.slots.append(name)
        setattr(self, name, value)
        setattr(self, 'updated_at', int(time.time() * 1000))
        self._persist()

    def _persist(self):
        pathname = f'{STORE_DIR}/{self.tag}-{self.uid}.p'
        with open(pathname, 'wb') as f:
            pickle.dump(self.__dict__, f)
