#!/usr/bin/pyton
# -*- coding: utf-8 -*-


import pprint
 
import xml.dom.minidom
from xml.dom.minidom import Node
import xml.dom.ext
import xml.dom.minidom


def write_to_screen(doc):
    xml.dom.ext.PrettyPrint(doc)
	
def write_to_file(doc, name="fetDelGestib2009.fet"):
    file_object = open(name, "w")
    xml.dom.ext.PrettyPrint(doc, file_object)
    file_object.close()
 
#<?xml version="1.0" encoding="ISO-8859-1"?>
#<HORARI>
  #<SESSIONS>
    #<SESSIO placa="" curs="62" grup="21121" dia="3" hora="8:55" durada="55" aula="" materia="38374" activitat=""/>
doc= xml.dom.minidom.Document() #destiny doc with GESTIB format output
gestib = xml.dom.minidom.parse("ExportacioDadesHoraris.xml") #file that contains gestib exportation
fet = xml.dom.minidom.parse("fetDelGestib2009.fet") #file created with transformaAFet.py plus timetable generation
activities=xml.dom.minidom.parse("fetDelGestib2009_activities.xml") #activities in timetable

days={"Lunes":"1","Martes":"2",u'Mi\xe9rcoles':"3","Jueves":"4","Viernes":"5"}
activityTranslate={}

#teachers and MATERIES codes
for activity in fet.getElementsByTagName("Activity"):
	Teacher=activity.getElementsByTagName("Teacher").item(0).childNodes[0].data
	Activity_Tag=activity.getElementsByTagName("Activity_Tag").item(0).childNodes[0].data
	Id=activity.getElementsByTagName("Id").item(0).childNodes[0].data
	Students=activity.getElementsByTagName("Students").item(0).childNodes[0].data
	print Teacher,Activity_Tag,Id,Students

#for each activity
for activity in activities.getElementsByTagName("Activity"):
	Id=activity.getElementsByTagName("Id").item(0).childNodes[0].data
	Day=days[activity.getElementsByTagName("Day").item(0).childNodes[0].data]
	Hour=activity.getElementsByTagName("Hour").item(0).childNodes[0].data
	#print "id: ", Id, " Day: ",Day," Hour: ",Hour
	#print '<SESSIO placa="x" curs="x" grup="x" dia="',Day,'" hora="',Hour,'" durada="55" aula="" materia="x" activitat="x"/>'







