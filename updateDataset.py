#! /usr/bin/env python
# -*- coding: UTF-8 -*-
#

mapDict = {}
accessedMapDict = {}
mapArr = ["Zero Page", "6502 Processor Stack", "GETLN Line Input Buffer", "Free Space for Machine Language, Shape Table, etc.", "DOS, ProDOS, and Interrupt Vectors", "Text Video Page and Peripheral Screenholes", "Text Video Page 2 or Applesoft Program and Variables", "Free Space for Machine Language, Shapes, etc.", "High Resolution Graphics Page 1", "High Resolution Graphics Page 2", "Applesoft String Data", "Soft Switches and Status Locations", "Peripheral Card Memory", "Extended Memory for Peripheral Card in Use", "Extensions to System Monitor", "80-Column Display Routines", "Self-Test Routines", "Applesoft Interpreter", "System Monitor", "Other"]
accessedMapArr = ["6502 Processor Stack", "Zero Page", "Free Space for Machine Language, Shape Table, etc.", "Free Space for Machine Language, Shapes, etc.", "Text Video Page and Peripheral Screenholes", "GETLN Line Input Buffer", "DOS, ProDOS, and Interrupt Vectors", "Text Video Page 2 or Applesoft Program and Variables"]

limit = 200000


def init():
	for map in mapArr:
		mapDict[map] = 0

	for map in accessedMapArr:
		accessedMapDict[map] = []

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

def reduceDataSet():
	file  = open("marblemadness.trace", "r")
	f = open("reducedSet.txt", "w+")
	count = 0
	
	for line in file:
		# Split line into an array of string with " " as the delimeter
		el = line.split(" ")
		
		if count > limit: break
		
		if len(el) > 1:
			addr = el[1][2:]
			try:
				addrInt = int(addr, 16)
			except ValueError:
				continue
			mem = calcMemMap(addrInt)
			
			# Retrieve the PC counter element while ignoring the '/n' character
			el[2] = el[2][0:7]
			s = el[0] + "  " + el[1] + "  " + el[2] + "  " + mem + "\n"
			f.write(s)
			count += 1

	file.close()


def addMapToTrace():
	file  = open("marblemadness.trace", "r") 
	f = open("modDataSet.txt", "w+")

	for line in file:
		# Split line into an array of string with " " as the delimeter
		el = line.split(" ")
	
		if len(el) > 1:
			addr = el[1][2:]
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


def createMapAccessesFile():
	file = open("modDataSet.txt", "r")
	f = open("mapAccesses.txt" ,"w+")
	l = 0
	for line in file:
		el = line.split("  ")
		if len(el) > 1:
			addr = el[1][2:]
			addr = int(addr, 16)
			map = el[3].split("\n")
			map = map[0]
			t = (l, addr)
			accessedMapDict[map].append(t)
			l += 1
	for map in accessedMapDict:
		m = accessedMapDict[map]
		for els in m:
			s = "{ x: " + str(els[0]) + ", y: " + str(els[1]) + "}," + "\n"
			f.write(s)

def createChartMapCount():
	file = open("reducedSet.txt", "r")
	s = 'var chart1 = new CanvasJS.Chart("chartContainer1", { \
			animationEnabled: true, \
			theme: "light2", \
			title:{ \
			text: "Memory Map Total Accesses (Read and Write)" \
			}, \
			axisY: { \
					title: "Number of Accesses" \
					}, \
					data: [{ \
						   type: "column", \
						   dataPoints: ['
	
	for line in file:
		el = line.split("  ")
		
		if len(el) > 1:
			map = el[3].split("\n")
			mapDict[map[0]] += 1

	for map in mapDict:
		if (mapDict[map] != 0):
			s += '{ y: ' + str(mapDict[map]) + ', label: "' + map + '"},'

	s = s[:-1]
	s += '] \
		 }] \
		 });'

	return s


def createChartMapAccesses():
	file = open("reducedSet.txt" , "r")
	Dict = {'Zero Page':""}
	l = 0
	
	for line in file:
		el = line.split("  ")
		
		if len(el) > 1:
			addr = el[1][2:]
			addr = int(addr, 16)

			map = el[3].split("\n")
			map = map[0]
			
			if map not in Dict:
				Dict.update({map:""})
			#continue

			Dict[map] += "{ x: " + str(l) + ", y: " + str(addr) + " },"
			l += 1
	
	
	s = 'var chart2 = new CanvasJS.Chart("chartContainer2", { \
										animationEnabled: true, \
										title: { \
										text: "Memory Map Accesses" \
										}, \
										axisX: { \
										title: "Position Within Trace (Line Number)", \
										valueFormatString: "#", \
										minimum: 0, \
										maximum:' + str(limit) + ' \
										}, \
										axisY: { \
										title: "Memory Address (in Decimal)", \
										minimum: 0, \
										maximum: 100000 \
										}, \
										legend: { \
										verticalAlign: "top", \
										horizontalAlign: "right", \
										dockInsidePlotArea: true \
										}, \
										data: ['
	for key in Dict:
		s += '{name:"' + key + '", \
		   showInLegend: true, \
		   legendMarkerType: "square", \
		   type: "line", \
		dataPoints: [' + Dict[key][:-1] + ']},'
	
	s = s[:-1]
	s += ']});'

	return s

def createChartPC():
	s = ''
	
	c3 = 'var chart3 = new CanvasJS.Chart("chartContainer3", { \
							   animationEnabled: true, \
							   theme: "light2", \
							   title:{ \
							   text: "PC Values Throughout the Trace" \
							   }, \
							   axisX: { \
							   title: "Position Within Trace (Line Number)", \
							   includeZero: false \
							   },\
							   axisY:{ \
							   title: "Memory Address (in Decimal)", \
							   includeZero: false \
							   }, \
							   data: [{ \
									  type: "line",  \
									  dataPoints: ['
									  
	c3_2 = 'var chart3_2 = new CanvasJS.Chart("chartContainer3_2", { \
						  animationEnabled: true, \
						  theme: "light2", \
						  title:{ \
						  text: "PC Values Throughout the Trace" \
						  }, \
						  axisX: { \
						  title: "Position Within Trace (Line Number)", \
						  includeZero: false \
						  },\
						  axisY:{ \
						  title: "Memory Address (in Decimal)", \
						  includeZero: false \
						  }, \
						  data: [{ \
						  type: "line",  \
							  dataPoints: ['

	c3_3 = 'var chart3_3 = new CanvasJS.Chart("chartContainer3_3", { \
				animationEnabled: true, \
				theme: "light2", \
				title:{ \
				text: "PC Values Throughout the Trace" \
				}, \
				axisX: { \
				title: "Position Within Trace (Line Number)", \
				includeZero: false \
				},\
				axisY:{ \
				title: "Memory Address (in Decimal)", \
				includeZero: false \
				}, \
				data: [{ \
				type: "line",  \
				dataPoints: ['

	c3_4 = 'var chart3_4 = new CanvasJS.Chart("chartContainer3_4", { \
				animationEnabled: true, \
				theme: "light2", \
				title:{ \
				text: "PC Values Throughout the Trace" \
				}, \
				axisX: { \
				title: "Position Within Trace (Line Number)", \
				includeZero: false \
				},\
				axisY:{ \
				title: "Memory Address (in Decimal)", \
				includeZero: false \
				}, \
				data: [{ \
				type: "line",  \
				dataPoints: ['

	file = open("reducedSet.txt" , "r")
	l = 0
	
	start1 = 27000
	end1 = 40000
	
	start2 = 120000
	end2 = 125000

	
	start3 = 140000
	end3 = 200000
	
	for line in file:
		el = line.split("  ")
		
		if len(el) > 1:
			PC = el[2][3:]
			PC = int(PC, 16)

			c3 += "{ x: " + str(l) + ", y: " + str(PC) + " },"
			
		if start1 <= l and l <= end1:
			c3_2 += "{ x: " + str(l) + ", y: " + str(PC) + " },"

		elif start2 <= l and l <= end2:
			c3_3 += "{ x: " + str(l) + ", y: " + str(PC) + " },"

		elif start3 <= l and l <= end3:
			c3_4 += "{ x: " + str(l) + ", y: " + str(PC) + " },"


		l += 1

	c3 = c3[:-1]
	c3_2 = c3_2[:-1]
	c3_3 = c3_3[:-1]
	c3_4 = c3_4[:-1]

	s = (c3 +  ']}]});' + c3_2 + ']}]});' + c3_3 + ']}]});' + c3_4 + ']}]});')

	return s

def createChartNonInstRW():
	Dict = {"r":"", "w":""}
	Dict2 = {"r":"", "w":""}
	Dict3 = {"r":"", "w":""}

	file = open("reducedSet.txt" , "r")
	l = 0
	start1 = 118000
	end1 = 132000
	start2 = 118000
	end2 = 119500
	
	for line in file:
		el = line.split("  ")
		
		if len(el) > 1:
			access = str(el[0])
			
			addr = el[1][2:]
			addr = int(addr, 16)

			PC = el[2][3:]
			PC = int(PC, 16)

			if abs(PC - addr) >= 5:
				if access == "r":
					if start1 <= l and l <= end1:
						Dict2["r"] += "{ x: " + str(l) + ", y: " + str(addr) + "}, "
					if start2 <= l and l <= end2:
						Dict3["r"] += "{ x: " + str(l) + ", y: " + str(addr) + "}, "
					
					Dict["r"] += "{ x: " + str(l) + ", y: " + str(addr) + "}, "
				elif access == "w":
					if start1 <= l and l <= end1:
						Dict2["w"] += "{ x: " + str(l) + ", y: " + str(addr) + "}, "
					if start2 <= l and l <= end2:
						Dict3["w"] += "{ x: " + str(l) + ", y: " + str(addr) + "}, "

					Dict["w"] += "{ x: " + str(l) + ", y: " + str(addr) + "}, "
			l += 1

	# Remove the extra ,
	Dict['r'] = Dict['r'][:-1]
	Dict['w'] = Dict['w'][:-1]

	Dict2['r'] = Dict2['r'][:-1]
	Dict2['w'] = Dict2['w'][:-1]

	Dict3['r'] = Dict3['r'][:-1]
	Dict3['w'] = Dict3['w'][:-1]


	s = 'var chart4 = new CanvasJS.Chart("chartContainer4", { \
		animationEnabled: true, \
		title:{ \
			text: "Non-Instruction Read and Write Accesses" \
		}, \
		axisX: { \
			title:"Position Within Trace (Line Number)" \
		}, \
		axisY:{ \
			title: "Memory Address (in Decimal)" \
		}, \
		data: [{ \
			   type: "scatter", \
			   name: "Non-Instruction Reads", \
			   showInLegend: true, \
			   dataPoints: [' + Dict['r'] + '] \
			   }, \
			   { \
				type: "scatter", \
				name: "Non-Instruction Writes", \
				showInLegend: true, \
				dataPoints: [' + Dict['w'] + ']}]});'
	
	chart4_1 ='var chart4_1 = new CanvasJS.Chart("chartContainer4_1", { \
			animationEnabled: true, \
			title:{ \
			text: "Non-Instruction Read and Write Accesses" \
			}, \
			axisX: { \
			title:"Position Within Trace (Line Number)" \
			}, \
			axisY:{ \
			title: "Memory Address (in Decimal)" \
			}, \
			data: [{ \
			type: "scatter", \
			name: "Non-Instruction Reads", \
			showInLegend: true, \
			dataPoints: [' + Dict2['r'] + '] \
			}, \
			{ \
			type: "scatter", \
			name: "Non-Instruction Writes", \
			showInLegend: true, \
			dataPoints: [' + Dict2['w'] + ']}]});'
			
	chart4_2 ='var chart4_2 = new CanvasJS.Chart("chartContainer4_2", { \
			animationEnabled: true, \
			title:{ \
			text: "Non-Instruction Read and Write Accesses" \
			}, \
			axisX: { \
			title:"Position Within Trace" \
			}, \
			axisY:{ \
			title: "Memory Address (in Decimal)" \
			}, \
			data: [{ \
			type: "scatter", \
			name: "Non-Instruction Reads", \
			showInLegend: true, \
			dataPoints: [' + Dict3['r'] + '] \
			}, \
			{ \
			type: "scatter", \
			name: "Non-Instruction Writes", \
			showInLegend: true, \
				dataPoints: [' + Dict3['w'] + ']}]});'



	return s + chart4_1 + chart4_2

def createChartInstFetch():
	points = ""
	file = open("reducedSet.txt" , "r")
	l = 0
	for line in file:
		el = line.split("  ")
		if len(el) > 1:
			access = str(el[0])

			addr = el[1][2:]
			addr = int(addr, 16)
			
			PC = el[2][3:]
			PC = int(PC, 16)
			
			if access == "r" and PC == addr:
				points += "{ x: " + str(l) + ", y: " + str(addr) + "}, "
			l += 1

	s = 'var chart5 = new CanvasJS.Chart("chartContainer5", { \
		animationEnabled: true, \
		title:{ \
		text: "Instruction Fetches" \
		}, \
		axisX: { \
		title:"Position Within Trace (Line Number)" \
		}, \
		axisY:{ \
		title: "Memory Address (in Decimal)", \
		minimum: 49000, \
		maximum: 66000,\
		}, \
		data: [{ \
		type: "line", \
		name: "Instruction Fetches", \
		showInLegend: true, \
		dataPoints: [' + points + '] \
		}]});'

	return s


def createCharts():
	f = open("Charts.js", "w+")
	s = "window.onload = function () {"
	chart1 = createChartMapCount()
	chart2 = createChartMapAccesses()
	chart3 = createChartPC()
	chart4 = createChartNonInstRW()
	chart5 = createChartInstFetch()
	s += chart1 + chart2 + chart3 + chart4 + chart5
#	s += chart3
	s += "chart1.render(); chart2.render(); chart3.render(); chart3_2.render(); chart3_3.render(); chart3_4.render(); chart4.render(); chart4_1.render(); chart4_2.render(); chart5.render();}"
#	s += "chart3.render(); chart3_2.render(); chart3_3.render(); chart3_4.render();}"
	f.write(s)


def main():
	init()
	#countMapAccesses()
	#addMapToTrace()
	#createMapAccessesFile()
	#reduceDataSet()
	createCharts()
	#reduceDataSet()

if __name__ == "__main__":
    main()

