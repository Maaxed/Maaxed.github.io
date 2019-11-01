from os import walk, path, chdir
import re
from shutil import copy2

encoding = 'utf-8'

includeRegex = re.compile(r'<include\s+src\s*=\s*"([\w.\-\/ ]+)"\s*\/?>')
structureRegex = re.compile(r'(<structure\s+src\s*=\s*"([\w.\-\/ ]+)"\s*>|<\/structure\s*>)')
contentRegex = re.compile(r'<struct-content\s*\/?>')

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

def processContent(content, replacements):
	##Include instruction
	content = includeRegex.sub(lambda match: processContent(replacements[match.group(1)], replacements), content)
	
	structures = []
	##Structure instruction

	match = structureRegex.search(content)
	while match:
		if match.group(1).startswith("</"):
			start = structures.pop()
			repl = processContent(replacements[start.group(2)], replacements)
			struct_content = content[start.end() : match.start()]
			content = content[:start.start()] + contentRegex.sub(lambda ma: struct_content, repl) + content[match.end():]
			match = structureRegex.search(content, start.end())
		else:
			structures.append(match)
			match = structureRegex.search(content, match.end())

	return content


def buildAll(folder, output, replacements):
	for (dirPath, dirs, files) in walk(folder):
		for fileName in files:
			if (fileName.endswith(".html")):
				print("Processing main file as html :", path.join(dirPath, fileName))
				##Open file
				inputFile = open(path.join(dirPath, fileName), 'r', encoding = encoding)
				oldContent = inputFile.read()
				inputFile.close()

				content = processContent(oldContent, replacements)
				
				##Write file
				outputFile = open(path.join(dirPath.replace(folder, output), fileName), 'w', encoding = encoding)
				outputFile.write(content);
				outputFile.close()
			else:
				print("Processing main file as ressource :", path.join(dirPath, fileName))
				copy2(path.join(dirPath, fileName), dirPath.replace(folder, output))


buildAll("main", "build", readRefs("refs"));