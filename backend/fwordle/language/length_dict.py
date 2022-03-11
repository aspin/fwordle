import random
from collections import defaultdict
from typing import Dict, List, Set


class LengthDictionary:
    _lists: Dict[int, List[str]]
    _sets: Dict[int, Set[str]]

    def __init__(self):
        self._lists = defaultdict(list)
        self._sets = defaultdict(set)

    def __len__(self):
        return sum(len(word_list) for word_list in self._lists.values())

    def add_word(self, word: str):
        sanitized = word.strip()
        self._lists[len(sanitized)].append(sanitized)
        self._sets[len(sanitized)].add(sanitized)

    def generate(self, word_length: int) -> str:
        return random.choice(self._lists[word_length])

    def is_word(self, word: str) -> bool:
        return word in self._sets[len(word)]
