from __future__ import annotations

import os
import sqlite3

from dataclasses import dataclass, field
from pathlib import Path


CODEBASE_DIR = f'{os.getenv("home")}/.yak/'
DEFAULT_NAME = 'user.yakimg'

CREATE_WORDS_TABLE = '''
CREATE TABLE words (
  id INTEGER PRIMARY KEY,
  name TEXT,
  version INTEGER,
  source_text TEXT,
  code_object BLOB
)
'''

CREATE_WORD_DEPS = '''
CREATE TABLE word_deps (
  word_id INTEGER,
  dep_id INTEGER
)
'''

CREATE_WORD_USAGES = '''
  word_id INTEGER,
  used_by INTEGER
)
'''


@dataclass
class Codebase:
    name: str
    path: Path

    def __post_init__(self):
        
        pass

    @staticmethod
    def open(name: str = DEFAULT_CODEBASE,
             dir: str = CODEBASE_DIR) -> Codebase:
        codebases = Path(dir)
        codebase_path = codebases / name

        if codebase_path.exists():
            return Codebase(name, codebase_path)
        return Codebase.create(name, codebase_path)

    @staticmethod
    def create(name: str, path: Path) -> Codebase:
        with sqlite3.connect(str(path)) as conn:
             conn.execute(CREATE_WORDS_TABLE)
             conn.execute(CREATE_WORD_DEPS)
             conn.execute(CREATE_WORD_USAGES)
        return Codebase(name, path)