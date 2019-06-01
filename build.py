from os import walk, path, chdir
import re
from shutil import copy2

encoding = 'utf-8'

def readRefs(folder):

	result = {}

	for (dirPath, dirs, files) in walk(folder):
		for fileName in files:
			print("Processing ref file :", path.join(dirPath, fileName))
			file = open(path.join(dirPath, fileName), 'r', encoding = encoding)
			key = (dirPath + "\\" + fileName).replace("\\", "/")[len(folder)+1:];
			result[key] = file.read()
			file.close()

	return result


def function(folder, output, replacements):
	for (dirPath, dirs, files) in walk(folder):
		for fileName in files:
			if (fileName.endswith(".html")):
				print("Processing main file as html :", path.join(dirPath, fileName))
				inputFile = open(path.join(dirPath, fileName), 'r', encoding = encoding)
				oldContent = inputFile.read()
				inputFile.close()
				content = re.sub("<include\\s+src=\"([\\w.\\-\\/ ]+)\"\\/?>", lambda match: replacements[match.group(1)], oldContent)
				outputFile = open(path.join(dirPath.replace(folder, output), fileName), 'w', encoding = encoding)
				outputFile.write(content);
				outputFile.close()
			else:
				print("Processing main file as ressource :", path.join(dirPath, fileName))
				copy2(path.join(dirPath, fileName), dirPath.replace(folder, output))


function("main", "build", readRefs("refs"));