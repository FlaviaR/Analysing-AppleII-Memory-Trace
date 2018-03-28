#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#

mapDict = {}
mapArr = ["Zero Page", "6502 Processor Stack", "GETLN Line Input Buffer", "Free Space for Machine Language, Shape Table, etc.", "DOS, ProDOS, and Interrupt Vectors", "Text Video Page and Peripheral Screenholes", "Text Video Page 2 or Applesoft Program and Variables", "Free Space for Machine Language, Shapes, etc.", "High Resolution Graphics Page 1", "High Resolution Graphics Page 2", "Applesoft String Data", "Soft Switches and Status Locations", "Peripheral Card Memory", "Extended Memory for Peripheral Card in Use", "Extensions to System Monitor", "80-Column Display Routines", "Self-Test Routines", "Applesoft Interpreter", "System Monitor", "Other"]

def init():
	for map in mapArr:
		mapDict[map] = 0

def calcMemMap(addr):
	if   (addr >= 0 and addr <= 255): return "Zero Page"
	elif (addr >= 256 and addr <= 511): return "6502 Processor Stack"
	elif (addr >= 512 and addr <= 767): return "GETLN Line Input Buffer"
	elif (addr >= 768 and addr <= 975): return "Free Space for Machine Language, Shape Table, etc."
	elif (addr >= 976 and addr <= 1023): return "DOS, ProDOS, and Interrupt Vectors"
	elif (addr >= 1024 and addr <= 2047): return "Text Video Page and Peripheral Screenholes"
	elif (addr >= 2048 and addr <= 3071): return "Text Video Page 2 or Applesoft Program and Variables"
	elif (addr >= 3072 and addr <= 8191): return "Free Space for Machine Language, Shapes, etc."
	elif (addr >= 8192 and addr <= 16383): return "High Resolution Graphics Page 1"
	elif (addr >= 16384 and addr <= 24575): return "High Resolution Graphics Page 2"
	elif (addr >= 24576 and addr <= 38399): return "Applesoft String Data"
	elif (addr >= 49152 and addr <= 49407): return "Soft Switches and Status Locations"
	elif (addr >= 49408 and addr <= 51199): return "Peripheral Card Memory"
	elif (addr >= 51200 and addr <= 53247): return "Extended Memory for Peripheral Card in Use"
	elif (addr >= 49408 and addr <= 49919): return "Extensions to System Monitor"
	elif (addr >= 49920 and addr <= 50175): return "80-Column Display Routines"
	elif (addr >= 50176 and addr <= 51199): return "Self-Test Routines"
	elif (addr >= 53248 and addr <= 63487): return "Applesoft Interpreter"
	elif (addr >= 63488 and addr <= 65535): return "System Monitor"

	else: return "Other"

def addMapToTrace():
	file  = open("marblemadness.trace", "r") 
	f = open("modDataSet.txt", "w+")

	for line in file:
		# Split line into an array of string with " " as the delimeter
		el = line.split(" ")
	
		if len(el) > 1:
			addr = el[1][3:]
			try:
				addrInt = int(addr, 16)
			except ValueError:
				continue
			mem = calcMemMap(addrInt)
		
			# Retrieve the PC counter element while ignoring the '/n' character
			el[2] = el[2][0:7]
			s = el[0] + "  " + el[1] + "  " + el[2] + "  " + mem + "\n"
			f.write(s)

	file.close() 

def countMapAccesses():
	file = open("modDataSet.txt", "r")
	f = open("numberOfAccessToMap.txt", "w+")

	for line in file:
		el = line.split("  ")

		if len(el) > 1:
			map = el[3].split("\n")
			mapDict[map[0]] += 1
	for map in mapDict:
		s = map + " " + str(mapDict[map]) + "\n"
		f.write(s)

def main():
	init()
	countMapAccesses()
	#addMapToTrace()

if __name__ == "__main__":
    main()

