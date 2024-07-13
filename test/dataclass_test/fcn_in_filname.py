from datafiles import datafile

@datafile("data_fcn/{self.name_upper}.json", defaults=True)
class Person:
    name: str

    name_upper = property(fget=lambda self: self.name.upper())
    
Joe = Person("Joe2")

