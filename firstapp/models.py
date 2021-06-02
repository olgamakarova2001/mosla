from django.db import models

# Create your models here.


class person:
    place = ''
    number = -1
    lastname = ""
    firstname = ""
    school = ""
    rounds = ''
    localnum = -1
    gennum = -1

    def __init__(self, number, lastname, firstname, school, roundnum, groupnum, rez, localnum):
        self.localnum = localnum
        self.lastname = lastname
        self.firstname = firstname
        self.number = number
        self. school = school
        self.rounds = [[], [], []]
        self.rounds[int(roundnum) - 1] = [rez, groupnum]

