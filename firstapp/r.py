from firstapp.models import person
from copy import copy as cp


def search(number, lastname, firstname, plist):
   x = 0
   al = ''
   for i in plist:
       x +=1
       if i.number == number:
           if i.lastname == lastname and i.firstname == firstname:
               return x, al
           else:
               al += 'Номера участников ' + lastname + ' ' + firstname + ' и ' + i.lastname + ' ' + i.firstname + ' совпадают.'
   return False, al

def time(st):
   if st.find(':') != -1:
       a = st.split(':')
       x = 0
       a.reverse()
       for i in range(0, len(a)):
           x += float(a[i]) * (60 ** i)
       return x
   else:
       return float(st)
def comp(p1, p2, r):
   iarr = ['ФС', 'НФ', 'НС', 'ДК','?']
   if p1.rounds[r-1][0] not in iarr and p2.rounds[r-1][0] not in iarr:
       if time(p1.rounds[r-1][0]) > time(p2.rounds[r-1][0]):
           return True
       else:
           return False
   else:
       if p1.rounds[r-1][0] in iarr and p2.rounds[r-1][0] in iarr:
           if p1.rounds[r-1][0] == p2.rounds[r-1][0]:
               if r>1:
                   return comp(p1, p2, r-1)
               else:
                   return False
           else:
               if iarr.index(p1.rounds[r-1][0]) >  iarr.index(p2.rounds[r-1][0]):
                   return True
               else:
                   return False
       if p1.rounds[r-1][0] not in iarr and p2.rounds[r-1][0] in iarr:
           return False
       else:
           return True

def num(list, r, startnum):
   place = startnum
   prevrez = list[0].rounds[r-1][0]
   prevrun = list[0].rounds[r-1][1]
   for i in list:
       if i.rounds[r-1][0] != prevrez:
           place +=1
       else:
           if i.rounds[r-1][1] == prevrun:
               place +=1
       i.gennum = place
       prevrez = i.rounds[r-1][0]
       prevrun = i.rounds[r-1][1]

   return place


def bubblesort(list, r):
   for i in range(len(list) - 1):
       for j in range(len(list) - i - 1):
           if comp(list[j], list[j+1], r):
               list[j], list[j + 1] = list[j + 1], list[j]
def insertsort(list, r):
    for i in range(len(list)):
        value = cp(list[i])
        j = i - 1
        while (j >= 0 and comp(list[j], value, r)):
            list[j], list[j + 1] = list[j + 1], list[j]
            j -= 1
        list[j+1] = cp(value)
def showlist(plist):
   for i in plist:
       print(i.gennum, i.localnum, i.number, i.firstname, i.lastname, i.school, i.rounds)
def parc(RESULT_SOURCE_PATH, fold, type):
   elist = ['ФС', 'НФ', 'НС', 'ДК', '?']
   note = ''
   roundcheck = ['','','']
   types = []
   curtype = -1
   curround = -1
   maxround = 0
   curgroup = -1
   import os
   data = {}
   resDict = {}
   sorted_resDict = {}
   linkDict = {}
   slnotDict = {}
   partlist = []
   partcatlist = [[], [], []]
   resultlist = []
   FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), RESULT_SOURCE_PATH[0], RESULT_SOURCE_PATH[1], fold, RESULT_SOURCE_PATH[2])
   fList = os.listdir(FULL_SOURCE_PATH)
   i = 1
   for fName in fList:
       if (not fName.endswith(".lif")) or int(fName[0:3]) != int(type):
           continue
       pathName = os.path.join(FULL_SOURCE_PATH, fName)
       with open(pathName, 'r', encoding='utf16') as f:
           c = 0
           al = ''
           s = 0
           for line in f:
               if c == 0:
                   headrow = line.split(',')
                   curround = headrow[1]
                   roundcheck[int(curround)-1] = '.'
                   if int(curround) > int(maxround):
                       maxround = curround
                   curgroup = headrow[2]
                   c = 1

               else:
                   if line[0] == ',':
                       line = ' ' + line
                   row = line.split(',')
                   if row[0] == '':
                       al += 'Номер участника' + row[3] + ' ' + row[4] + ' остутствует!\n'
                       row[0] = '?'
                   else:
                       if row[6] == '' and row[0] not in elist:
                           al += 'Результат' + row[3] + ' ' + row[4] + ' остутствует!\n'
                           row[6] = '?'
                   if row[6] == '':
                       row[6] = row[0]
                   ptemp = person(row[1], row[3], row[4], row[5],curround, curgroup,row[6], row[0])
                   s, al = search(ptemp.number, ptemp.lastname, ptemp.firstname, partlist)
                   if s == False:
                       partlist.append(ptemp)
                   else:
                       partlist[s - 1].rounds[
                           int(curround) - 1] = [row[6], curgroup]
                       partlist[s - 1].localnum = row[0]
       note += al

   for i in range(0, int(maxround)):
       if roundcheck[i] != '.':
           data['header'] = 'Ошибка: отсутствуют результаты одного из кругов.\n'
           data['tablehead'] = ''
           data['rows'] = ''
           return data, ''
   for i in partlist:
       if i.rounds[2] != []:
           partcatlist[2].append(i)
       else:
           if i.rounds[1] != []:
               partcatlist[1].append(i)
           else:
               if i.rounds[0] != []:
                   partcatlist[0].append(i)
   for i in range(int(maxround), 0, -1):
      insertsort(partcatlist[i-1], i)
   c = 0
   for t in range(int(maxround), 0, -1):
       c = num(partcatlist[t - 1], t, c)
   resultlist = partcatlist[2] + partcatlist[1] + partcatlist[0]
   for i in range(0, int(maxround)):
       if roundcheck[i] != '.':
           data['header'] = 'ERROR'
           data['tablehead'] = ''
           data['rows'] = ''
           return data, note
   strlist = []
   data['header'] = headrow[3]
   if int(maxround) == 1:
       data['tableHead'] = ['№ п\п', 'ФИО', 'Школа', 'Результат']
   else:
       if int(maxround) == 2:
           data['tableHead'] = ['№ п\п', 'ФИО', 'Школа', 'Отборочный этап','Заключительный этап']
       else:
           data['tableHead'] = ['№ п\п', 'ФИО', 'Школа', 'Отборочный этап', 'Полуфинал', 'Финал']

   for p in range(len(resultlist)):
       templist = [str(resultlist[p].gennum), resultlist[p].lastname + ' ' + resultlist[p].firstname, resultlist[p].school]
       for z in range(int(maxround)):
           if resultlist[p].rounds[z] != []:
               templist.append(resultlist[p].rounds[z][0])
           else:
               templist.append('')
       strlist.append(templist)
   data['rows'] = strlist
   print(note)
   data['button_class'] = 'result'
   return data, note
