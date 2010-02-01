#!/usr/bin/pyton
# -*- coding: utf-8 -*-


import pprint
 
import xml.dom.minidom
from xml.dom.minidom import Node
import xml.dom.ext
import xml.dom.minidom
import re

def write_to_screen(doc):
    xml.dom.ext.PrettyPrint(doc)
	
def write_to_file(doc, name="GestibDelFet2009.xml"):
    file_object = open(name, "w")
    xml.dom.ext.PrettyPrint(doc, file_object)
    file_object.close()
 
#<?xml version="1.0" encoding="ISO-8859-1"?>
#<HORARI>
  #<SESSIONS>
    #<SESSIO placa="" curs="62" grup="21121" dia="3" hora="8:55" durada="55" aula="" materia="38374" activitat=""/>
doc= xml.dom.minidom.Document() #destiny doc with GESTIB format output
HORARI = doc.createElement("HORARI")
doc.appendChild(HORARI)

SESSIONS=doc.createElement("SESSIONS")
HORARI.appendChild(SESSIONS)

gestib = xml.dom.minidom.parse("ExportacioDadesHoraris.xml") #file that contains gestib exportation
fet = xml.dom.minidom.parse("fetDelGestib2009.fet") #file created with transformaAFet.py plus timetable generation
activities=xml.dom.minidom.parse("fetDelGestib2009_activities.xml") #activities in timetable

days={"Lunes":"1","Martes":"2",u'Mi\xe9rcoles':"3","Jueves":"4","Viernes":"5"}
activityTeacher={}#relacionam les id de les activitats amb els profes
activityGroup={}#relacionam les id de les activitas amb el grup on es fan
activityMateria={}#relacionam les id de les activitas amb les materies
pattCodi='.+?\((\d+)\)'

#teachers and MATERIES codes
for activity in fet.getElementsByTagName("Activity"):
	Teacher=activity.getElementsByTagName("Teacher").item(0).childNodes[0].data
	codiProfe=re.match(pattCodi,Teacher).group(1)
	Activity_Tag=activity.getElementsByTagName("Activity_Tag").item(0).childNodes[0].data
	codiActivity=re.match(pattCodi,Activity_Tag).group(1)
	Id=activity.getElementsByTagName("Id").item(0).childNodes[0].data
	Students=activity.getElementsByTagName("Students").item(0).childNodes[0].data #groups
	codiStudents=re.match(pattCodi,Students).group(1)#codi del group
	activityTeacher[Id]=codiProfe
	activityGroup[Id]=codiStudents
	activityMateria[Id]=codiActivity
	
print "activityTeacher",activityTeacher
print "activityGroup",activityGroup

#for each activity
for activity in activities.getElementsByTagName("Activity"):
	Id=activity.getElementsByTagName("Id").item(0).childNodes[0].data
	Day=days[activity.getElementsByTagName("Day").item(0).childNodes[0].data]
	Hour=activity.getElementsByTagName("Hour").item(0).childNodes[0].data
	Teacher=activityTeacher[Id]
	group=activityGroup[Id]
	materia=activityMateria[Id]
	SESSIO=doc.createElement("SESSIO")
	SESSIONS.appendChild(SESSIO)
	#print "id: ", Id, " Day: ",Day," Hour: ",Hour
	#print '<SESSIO placa="',Teacher,'" curs="x" grup="',group,'" dia="',Day,'" hora="',Hour,'" \
	#durada="55" aula="" materia="',materia,'" activitat=""/>'
	SESSIO.setAttribute("placa",Teacher)
	SESSIO.setAttribute("curs","")
	SESSIO.setAttribute("grup",group)
	SESSIO.setAttribute("dia",Day)
	SESSIO.setAttribute("hora",Hour)
	SESSIO.setAttribute("durada","55")
	SESSIO.setAttribute("aula","")
	SESSIO.setAttribute("materia",materia)
	SESSIO.setAttribute("activitat","")
write_to_file(doc)







