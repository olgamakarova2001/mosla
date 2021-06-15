from django.shortcuts import render

# Create your views here.

from firstapp.r import parc
import os
psp = ['', '', '', 'primary']
rsp = ['', '', '', 'results']
confpath = os.path.join(str(os.getcwd()), "config.txt")
with open(confpath, 'r') as conf:
    for line in conf:
        if line.find('\n') != -1:
            line = line[:-1]
        if line.startswith('$'):
            break
        l = line.split('=')
        if l[0] == 'FOLDER NAME':
           psp[1] = l[1]
           rsp[1] = l[1]
        if l[0] == 'DIRECTORY NAME':
            psp[0] = l[1]
            rsp[0] = l[1]
        if l[0] == 'PROTOCOLS':
            psp[2] = l[1]
        if l[0] == 'RESULTS':
            rsp[2] = l[1]
PRIMARY_SOURCE_PATH = psp
RESULT_SOURCE_PATH = rsp



def Mseek(row):
   indexM = row.find('м')
   markM = 0

   # Ищем "м"

   while 0 < indexM < len(row):
       if (indexM > 0) and (row[indexM - 1 - markM].isdigit()):
           markM += 1
       elif markM > 0:
           break
       else:
           indexM = row[indexM + 1:].find('м')
   return indexM, markM


def rightFolder(pathx, x):
   import os
   return (PRIMARY_SOURCE_PATH[2] in os.listdir(os.path.join(str(os.getcwd()), pathx[0], pathx[1], x))) or (RESULT_SOURCE_PATH[2] in os.listdir(os.path.join(str(os.getcwd()), pathx[0], pathx[1], x)))


def folder_seek(PATH):
   folderList = []
   import os
   FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), PATH[0], PATH[1])
   pathList = os.listdir(FULL_SOURCE_PATH)
   for foldNum, foldName in enumerate(filter(lambda x: rightFolder(PATH, x), pathList)):
       pfolder = ('/' + PATH[3] + '/' + str(foldNum))
       if foldName.isdigit():
           foldName = 'Турнир ' + foldName
       folderList.append((foldName, pfolder))
   return folderList


def seekNumFold(PATH, num):
   import os
   FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), PATH[0], PATH[1])
   pathList = os.listdir(FULL_SOURCE_PATH)
   for foldNum, foldName in enumerate(filter(lambda x: rightFolder(PATH, x), pathList)):
       if foldNum == int(num):
           return foldName


def index(request):
    try:
       primres = []
       primary_menu = folder_seek(PRIMARY_SOURCE_PATH)
    #    result_menu = folder_seek(RESULT_SOURCE_PATH) "result_menu": result_menu
       for cort in primary_menu:
           folnum = '/' + RESULT_SOURCE_PATH[3] + '/' + ((cort[1].split('/'))[-1:][0])
           primres.append((cort[0], cort[1], folnum))
       data = {"menu": primres}
    except Exception as e:
        errordat = {"exception": e}
        return render(request, "eroha.html", errordat)
    return render(request, "main.html", data)


def showPrimaryData(request, foldnum):
   fold = seekNumFold(PRIMARY_SOURCE_PATH, foldnum)
   data = {}
   resDict = {}
   sorted_resDict = {}
   unsortedDict = {}
   linkDict = {}
   slnotDict = {}
   fList = []
   pfList = ''
   try:
       import os
       if PRIMARY_SOURCE_PATH[2] not in os.listdir(os.path.join(str(os.getcwd()), PRIMARY_SOURCE_PATH[0], PRIMARY_SOURCE_PATH[1], fold)):
           folder_menu = folder_seek(PRIMARY_SOURCE_PATH)
           datala = {"folders": folder_menu, "button_class": "primary", "Name": (fold, foldnum), "alert_class": PRIMARY_SOURCE_PATH[2]}
           return render(request, "no_files.html", datala)
       FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), PRIMARY_SOURCE_PATH[0], PRIMARY_SOURCE_PATH[1], fold, PRIMARY_SOURCE_PATH[2])
       fList = os.listdir(FULL_SOURCE_PATH)

       folder_menu = folder_seek(PRIMARY_SOURCE_PATH)

       i = 1
       for fName in fList:
           if not fName.endswith(".evt"):
               continue
           pathName = os.path.join(FULL_SOURCE_PATH, fName)
           with open(pathName, 'r', encoding='utf16') as f:
               for line in f:
                   row = line.split(',')
                   if (row[0]).isdigit():
                       indexM = Mseek(row[3])

                       if ((row[9][-1]).isdigit()) or (indexM[1] > 0):
                           if (row[9][-1]).isdigit():
                               sline = int(row[9][-1])
                           else:
                               sline = int(row[3][indexM[0] - indexM[1]: indexM[0]])
                           link = ('./' + fName[: fName.index(".")] + '/' + str(i),
                                   row[1] + ' круг, ' + row[2] + ' забег')
                           linkDict.setdefault(row[3], []).append(link)
                           resDict.setdefault(sline, [])
                           if (row[3], linkDict.get(row[3])) not in resDict.get(sline):
                               resDict.get(sline).append((row[3], linkDict.get(row[3])))
                       else:
                           link = ('./' + fName[: fName.index(".")] + '/' + str(i),
                                   row[1] + ' круг, ' + row[2] + ' забег')
                           slnotDict.setdefault(row[3], []).append(link)
                       unlink = ('./' + fName[: fName.index(".")] + '/' + str(i),
                               row[1] + ' круг, ' + row[2] + ' забег')
                       unsortedDict.setdefault(row[3], []).append(unlink)
                       i += 1
       sorted_keys = sorted(resDict.keys())
       for element in sorted_keys:
           sorted_resDict[element] = resDict[element]
       if fold.isdigit():
           fold = 'Турнир ' + fold
       data = {"resultCountDict": sorted_resDict, "resultDict": slnotDict, "resultNotCount": unsortedDict, "button_class": "primary", "folders": folder_menu, "Name": (fold, foldnum), "Marker": len(slnotDict)}
   except Exception as e:
       errordat = {"exception": e}
       return render(request, "eroha.html", errordat)
   return render(request, "result_list.html", data)


def showResultData(request, foldnum):
   fold = seekNumFold(PRIMARY_SOURCE_PATH, foldnum)
   data = {}
   sorted_resDict = {}
   linkDict = {}
   slnotDict = {}
   resDict = {}
   unsortedDict = {}
   try:
       import os
       if RESULT_SOURCE_PATH[2] not in os.listdir(os.path.join(str(os.getcwd()), RESULT_SOURCE_PATH[0], RESULT_SOURCE_PATH[1], fold)):
           folder_menu = folder_seek(RESULT_SOURCE_PATH)
           if fold.isdigit():
               fold = 'Турнир ' + fold
           datala = {"folders": folder_menu, "button_class": "results", "Name": (fold, foldnum), "alert_class": RESULT_SOURCE_PATH[2]}
           return render(request, "no_files.html", datala)
       FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), RESULT_SOURCE_PATH[0], RESULT_SOURCE_PATH[1], fold, RESULT_SOURCE_PATH[2])
       fList = os.listdir(FULL_SOURCE_PATH)

       folder_menu = folder_seek(RESULT_SOURCE_PATH)

       generatork = -1
       for fName in fList:
           if not fName.endswith(".lif"):
               continue

           pathName = os.path.join(FULL_SOURCE_PATH, fName)
           with open(pathName, 'r', encoding='utf16') as f:
               for line in f:
                   row = line.split(',')

                   indexM = Mseek(row[3])

                   if ((row[9]).isdigit()) or (indexM[1] > 0):
                       if (row[9]).isdigit():
                           sline = int(row[9])
                       else:
                           sline = int(row[3][indexM[0] - indexM[1]: indexM[0]])

                       if generatork != int(fName[:3]):
                           generatork = int(fName[:3])
                           reslink = ('./result_table/' + fName[:3], 'Итоговая таблица')
                           linkDict.setdefault(row[3], []).append(reslink)
                           unsortedDict.setdefault(row[3], []).append(reslink)

                       if (line[0]).isdigit() or (line[0]).isalpha():
                           link = ('./' + fName[: fName.index(".")], row[1] + ' круг, ' + row[2] + ' забег')
                           linkDict.setdefault(row[3], []).append(link)
                           unsortedDict.setdefault(row[3], []).append(link)
                       resDict.setdefault(sline, [])
                       if (row[3], linkDict.get(row[3])) not in resDict.get(sline):
                           resDict.get(sline).append((row[3], linkDict.get(row[3])))
                          

                   else:
                       if generatork != int(fName[:3]):
                           generatork = int(fName[:3])
                           reslink = ('./result_table/' + fName[:3], 'Итоговая таблица')
                           slnotDict.setdefault(row[3], []).append(reslink)
                           unsortedDict.setdefault(row[3], []).append(reslink)
                       if (line[0]).isdigit() or (line[0]).isalpha():
                           link = ('./' + fName[: fName.index(".")], row[1] + ' круг, ' + row[2] + ' забег')
                           slnotDict.setdefault(row[3], []).append(link)
                   break
       sorted_keys = sorted(resDict.keys())
       for element in sorted_keys:
           sorted_resDict[element] = resDict[element]
       if fold.isdigit():
           fold = 'Турнир ' + fold
       data = {"resultCountDict": sorted_resDict, "resultDict": slnotDict, "resultNotCount": unsortedDict, "button_class": "results", "folders": folder_menu, "Name": (fold, foldnum), "Marker": len(slnotDict)}
   except Exception as e:
       errordat = {"exception": e}
       return render(request, "eroha.html", errordat)
   return render(request, "result_list.html", data)


def showResult(request, foldnum, source):
   fold = seekNumFold(PRIMARY_SOURCE_PATH, foldnum)
   data = {}
   try:
           import os
           links = []
           FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), RESULT_SOURCE_PATH[0], RESULT_SOURCE_PATH[1], fold, RESULT_SOURCE_PATH[2])
           pathName = os.path.join(FULL_SOURCE_PATH, source + ".lif")
           with open(pathName, 'r', encoding='utf16') as f:
               i = 0
               for line in f:
                   row = line.split(',')
                   if i == 0:
                       data['header'] = row[3] + ', ' + row[1] + ' круг, ' + row[2] + ' забег'
                   else:
                       links.append([row[0], row[1], row[3] + ' ' + row[4], row[5], row[6]])
                   i += 1
               data['rows'] = links
               data['tableHead'] = ['№ п\п', '№ уч.', 'ФИО', 'Организация', 'Результат']
               data['button_class'] = 'results'
               data['alert'] = (0, '')
               data["style_buttons"] = foldnum

   except Exception as e:
       errordat = {"exception": e}
       return render(request, "eroha.html", errordat)
   return render(request, "simple_table.html", data)


def showPrimary(request, foldnum, source, number):
   fold = seekNumFold(PRIMARY_SOURCE_PATH, foldnum)
   data = {}
   try:
       num = int(number)
       import os
       FULL_SOURCE_PATH = os.path.join(str(os.getcwd()), PRIMARY_SOURCE_PATH[0], PRIMARY_SOURCE_PATH[1], fold, PRIMARY_SOURCE_PATH[2])
       pathName = os.path.join(FULL_SOURCE_PATH, source + ".evt")
       rows = []
       with open(pathName, 'r', encoding='utf16') as f:
           lines = f.readlines()
           i = 0
           k = 0
           while i < num and k < len(lines):
               if (lines[k][0]).isdigit():
                   i += 1
               k += 1
           row = lines[k-1].split(',')
           data['header'] = row[3] + ', ' + row[1] + ' круг, ' + row[2] + ' забег'
           if k < len(lines):
               while not(lines[k][0].isdigit()):
                   row = lines[k].split(',')
                   rows.append([row[1], row[2], row[3] + ' ' + row[4], row[5], row[6]])
                   k += 1
           data['rows'] = rows
           data['tableHead'] = ['Номер', 'Дорожка', 'ФИО', 'Организация', 'Лицензия']
           data['button_class'] = 'primary'
           data['alert'] = (0, '')
           data["style_buttons"] = foldnum

   except Exception as e:
       errordat = {"exception": e}
       return render(request, "eroha.html", errordat)
   return render(request, "simple_table.html", data)


def showJoinedResult(request, foldnum, number):
   alert = ''
   fold = seekNumFold(PRIMARY_SOURCE_PATH, foldnum)
   try:
       a = int(number)
       data, alert = parc(RESULT_SOURCE_PATH, fold, a)

       data["button_class"] = "results"
       data["style_buttons"] = foldnum

       if len(alert) != 0:
           alert = alert.split('\n')[:-1]
           data['alert'] = (1, alert)
       else:
           data['alert'] = (0, '')

   except Exception as e:
       errordat = {"exception": e}
       return render(request, "eroha.html", errordat)
   return render(request, "simple_table.html", data)


