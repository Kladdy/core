from typing import Optional
from datafiles import datafile, Missing

@datafile("data/{self.name}.json")
class Person:
    name: str
    age: int
    is_alive: Optional[bool]
    pets: list[str]


#fredrik = Person("Fredrik", 30, True, ["dog", "cat"])

fredrik = Person("Fredrik", Missing, Missing, Missing)

fredrik.age = 600

print(fredrik)