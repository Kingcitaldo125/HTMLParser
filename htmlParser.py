import re
import urllib.request
from html.parser import HTMLParser

lastStartTag = ""
fileHandle = open("output.txt", "w")
tagExcludes = ["style","span"]

class MyHTMLParser(HTMLParser):
	def handle_starttag(self, tag, attrs):
		global lastStartTag, tagExcludes, fileHandle
		if tag not in tagExcludes:
			#print("START_TAG:", tag, "ATTRS:", attrs)
			fileHandle.write(tag)
			fileHandle.write("\n")
			lastStartTag = tag
	def handle_endtag(self, tag):
		global fileHandle
		#print("END_TAG:", tag)
		fileHandle.write(tag)
		fileHandle.write("\n")
	def handle_data(self, data):
		global lastStartTag, fileHandle
		m = re.match(r"(.|-)+\s|(.|-)+", data, re.I|re.U)
		if m and len(data)>0:
			print("DATA:", m.group())
			if lastStartTag != "script":
				fileHandle.write(m.group(0))
				fileHandle.write("\n")

def extractURLData(url):
	opnr = urllib.request.FancyURLopener({})
	f = opnr.open(url)
	x = f.read()
	return x.decode("utf-8")
		

exampleHTML = "<html><head></head><body><div id='PARAGRAPH_ID'><p>PARAGRAPH</p></div></body></html>"		
prsr = MyHTMLParser()
urlData = extractURLData("https://www.baseball-reference.com/leagues/MLB/1997-standings.shtml")
#print(urlData)
prsr.feed(urlData)
fileHandle.close()
