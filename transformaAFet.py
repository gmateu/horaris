#!/usr/bin/python
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
 
 
doc= xml.dom.minidom.Document()
arrel = doc.createElement("FET")
arrel.setAttribute("version","5.9.1")
doc.appendChild(arrel)
llistaProfes = doc.createElement("Teachers_List")
Students_List=doc.createElement("Students_List")
Activity_Tags_List=doc.createElement("Activity_Tags_List")
arrel.appendChild(llistaProfes)
arrel.appendChild(Students_List)
arrel.appendChild(Activity_Tags_List)
gestib = xml.dom.minidom.parse("ExportacioDadesHoraris.xml")
fet = xml.dom.minidom.parse("fet2009.fet")

#professors

for node in gestib.getElementsByTagName("PLACA"):
	curta = node.getAttribute("curta")
	descripcio=node.getAttribute("descripcio")
	codi=node.getAttribute("codi")
	descripcio+="("+codi+")" #per matenir el codi del professor a l'hora de tornar cap el GESTIB
	t=doc.createElement("Teacher")
	nom=doc.createElement("Name")
	t.appendChild(nom)
	t.setAttribute("curta",curta)
	t.setAttribute("codi",codi)
	description = doc.createTextNode(descripcio)
	nom.appendChild(description)
	llistaProfes.appendChild(t)


#cursos
#<Students_List>
	#<Year>
		#<Name>1rESO</Name>
		#<Number_of_Students>0</Number_of_Students>
		#<Group>
			#<Name>1rESO - A</Name>
			#<Number_of_Students>0</Number_of_Students>
		#</Group>
		#<Group>
			#<Name>1rESO - B</Name>
			#<Number_of_Students>0</Number_of_Students>
		#</Group>
	#</Year>
	#<Year>
		#<Name>2n ESO</Name>
		#<Number_of_Students>0</Number_of_Students>
		#<Group>
			#<Name>2n ESO - A</Name>
			#<Number_of_Students>0</Number_of_Students>
		#</Group>
		#<Group>
			#<Name>2n ESO - B</Name>
			#<Number_of_Students>0</Number_of_Students>
		#</Group>
	#</Year>
#</Students_List>
for node in gestib.getElementsByTagName("CURS"):
	descripcio=node.getAttribute("descripcio")
	grups=node.getElementsByTagName("GRUP")
	Year=doc.createElement("Year")
	Students_List.appendChild(Year)
	courseName=doc.createElement("Name")
	courseName.appendChild(doc.createTextNode(descripcio))
	Year.appendChild(courseName)
	Number_of_Students=doc.createElement("Number_of_Students")
	Number_of_Students.appendChild(doc.createTextNode("0"))
	Year.appendChild(Number_of_Students)
	for grup in grups:
		Group=doc.createElement("Group")
		desFinal=descripcio+" "+ grup.getAttribute("nom")
		nom=doc.createTextNode(desFinal)
		name=doc.createElement("Name")
		name.appendChild(nom)
		Group.appendChild(name)
		Year.appendChild(Group)
		
		Number_of_StudentsGrup=doc.createElement("Number_of_Students")
		Number_of_StudentsGrup.appendChild(doc.createTextNode("0"))
		Group.appendChild(Number_of_Students)

		
#materies
#<Activity_Tags_List>
#<Activity_Tag>
	#<Name>Llengua estrangera - anglès-A</Name>
#</Activity_Tag>
#</Activity_Tags_List>
#<MATERIA
	#codi="83994"
	#curs="45"
	#descripcio="Coneixement de l&#039;entorn-A"
	#curta="Coneix. de l&#039;entorn-A"
	#departament=""
#/>
listmat=[]
for node in gestib.getElementsByTagName("MATERIA"):
	descripcio=node.getAttribute("descripcio")
	curta=node.getAttribute("curta")
	codi=node.getAttribute("codi")
	codeCourse=node.getAttribute("curs")
	cursos=gestib.getElementsByTagName("CURS")
	courseOfMateria=""
	#we need a better method to travessing an xml to get the description for a known attribute
	for curs in cursos: #searching course description of subject to put in listMat, avoid create duplicates
		keys=curs.attributes["codi"]
		desc=curs.attributes["descripcio"]
		if keys.value==codeCourse:
			courseOfMateria=desc.value #now we have course where the subject is done
	curta=curta+" ("+codi+")-"+courseOfMateria
	if curta not in listmat:
		listmat.append(curta)
		a=doc.createElement("Activity_Tag")
		a.setAttribute("descripcio",descripcio)
		a.setAttribute("codi",codi)
		name=doc.createElement("Name")
		nom=doc.createTextNode(curta)
		name.appendChild(nom)
		a.appendChild(name)
		Activity_Tags_List.appendChild(a)
	
#<Time_Constraints_List>
#<ConstraintMinNDaysBetweenActivities>
	#<Weight_Percentage>95</Weight_Percentage>
	#<Consecutive_If_Same_Day>true</Consecutive_If_Same_Day>
	#<Number_of_Activities>4</Number_of_Activities>
	#<Activity_Id>1</Activity_Id>
	#<Activity_Id>2</Activity_Id>
	#<Activity_Id>3</Activity_Id>
	#<Activity_Id>4</Activity_Id>
	#<MinDays>1</MinDays>
#</ConstraintMinNDaysBetweenActivities>
#<ConstraintBasicCompulsoryTime>
	#<Weight_Percentage>100</Weight_Percentage>
#</ConstraintBasicCompulsoryTime>
#</Time_Constraints_List>
Time_Constraints_List=doc.createElement("Time_Constraints_List")
arrel.appendChild(Time_Constraints_List)
ConstraintMinNDaysBetweenActivities=doc.createElement("ConstraintMinNDaysBetweenActivities")
Time_Constraints_List.appendChild(ConstraintMinNDaysBetweenActivities)

Weight_Percentage=doc.createElement("Weight_Percentage")
ConstraintMinNDaysBetweenActivities.appendChild(Weight_Percentage)
Weight_Percentage.appendChild(doc.createTextNode("95"))
Consecutive_If_Same_Day=doc.createElement("Consecutive_If_Same_Day")
ConstraintMinNDaysBetweenActivities.appendChild(Consecutive_If_Same_Day)
Consecutive_If_Same_Day.appendChild(doc.createTextNode("true"))
Number_of_Activities=doc.createElement("Number_of_Activities")
ConstraintMinNDaysBetweenActivities.appendChild(Number_of_Activities)
Number_of_Activities.appendChild(doc.createTextNode("4"))

Activity_Id=doc.createElement("Activity_Id")
ConstraintMinNDaysBetweenActivities.appendChild(Activity_Id)
Activity_Id.appendChild(doc.createTextNode("1"))

Activity_Id2=doc.createElement("Activity_Id")
ConstraintMinNDaysBetweenActivities.appendChild(Activity_Id2)
Activity_Id2.appendChild(doc.createTextNode("2"))

Activity_Id3=doc.createElement("Activity_Id")
ConstraintMinNDaysBetweenActivities.appendChild(Activity_Id3)
Activity_Id3.appendChild(doc.createTextNode("3"))

Activity_Id4=doc.createElement("Activity_Id")
ConstraintMinNDaysBetweenActivities.appendChild(Activity_Id4)
Activity_Id4.appendChild(doc.createTextNode("4"))

MinDays=doc.createElement("MinDays")
ConstraintMinNDaysBetweenActivities.appendChild(MinDays)
MinDays.appendChild(doc.createTextNode("1"))


ConstraintBasicCompulsoryTime=doc.createElement("ConstraintBasicCompulsoryTime")
Time_Constraints_List.appendChild(ConstraintBasicCompulsoryTime)
Weight_Percentage2=doc.createElement("Weight_Percentage")
ConstraintBasicCompulsoryTime.appendChild(Weight_Percentage2)
Weight_Percentage2.appendChild(doc.createTextNode("100"))


#<Space_Constraints_List>
#<ConstraintBasicCompulsorySpace>
	#<Weight_Percentage>100</Weight_Percentage>
#</ConstraintBasicCompulsorySpace>
#</Space_Constraints_List>


Space_Constraints_List=doc.createElement("Space_Constraints_List")
arrel.appendChild(Space_Constraints_List)
ConstraintBasicCompulsorySpace=doc.createElement("ConstraintBasicCompulsorySpace")
Space_Constraints_List.appendChild(ConstraintBasicCompulsorySpace)
Weight_Percentage100=doc.createElement("Weight_Percentage")
Weight_Percentage100.appendChild(doc.createTextNode("100"))
ConstraintBasicCompulsorySpace.appendChild(Weight_Percentage100)



	

		


write_to_file(doc)