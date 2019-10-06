# -*- coding: utf-8 -*-
import re

referencesName = []

#------------------------------
# sort
def takeFirst(elem):
	return elem[0]

#------------------------------
def ReferencedIndex(word_):
	#
	if len(word_)>20:
		return

	#
	spetialChars = ['201','200',',']

	counter = 0
	for schar in spetialChars:
		if schar in word_:
			counter = counter + 1

	isANewReference = False
	if counter==2:
		countCurrentReference = referencesName.count(word_)
		if countCurrentReference==0:
			isANewReference = True
	else:
		return
	
	#
	counter_NOT = 0
	spetialChars_NOT = ['[J]','[M]']
	for schar_NOT in spetialChars_NOT:
		if schar_NOT in word_:
			counter_NOT = counter_NOT + 1
	
	if counter_NOT==0:
		isANewReference = True
	else:
		return

	#
	counter_ref = referencesName.count(word_)
	if isANewReference and counter_ref==0:
		referencesName.append(word_)

	return 

#------------------------------
print("hello")

#
# step 1 : read file
#
paper_read = open("originalPaper.md",'r')
content = paper_read.readlines()
paper_read.close()

for line_ori in content:
	line = line_ori.strip()
	#print(line)

	words = re.split('[\[\]]',line)
	#print(words)

	for word in words:
		#print(word)
		ReferencedIndex(word)

print('References')

counter = 0
for ref in referencesName:
	counter += 1
	print("[{}] : {}".format(counter,ref))

#
# step 2  : wirte
#
line_num = 0
line_num_Reference = -1

content_write = []
content_references = []

for line_ori in content:
	line_num = line_num + 1
	#print(line_ori)

	line_changed = line_ori
	for reference in referencesName:
		refID = referencesName.index(reference) + 1
		#line_ori.replace(reference,refID)
		line_changed = str(line_changed).replace(reference,str(refID))

	if line_ori=='# 参考文献\n':
		print('!!!!!!!!!!!!!!!!!!!!!!!# 参考文献')
		line_num_Reference = line_num
		content_write.append(line_ori)

	if line_num_Reference==-1:
		content_write.append(line_changed)

	if line_num_Reference!=-1 and line_ori!='\n' and line_ori!='# 参考文献\n':
		# get into contents of referecens
		refID = -1
		for reference in referencesName:
			refID_current = referencesName.index(reference) + 1
			if reference in line_ori:
				refID = refID_current
		line_changed += "\n"
		ref = (refID,line_changed)
		content_references.append(ref)

content_references.sort(key=takeFirst)
#print(content_references)

paper_write = open("paper_output.md",'w')
for line_ori in content_write:
	paper_write.write(line_ori)
for reference in content_references:
	paper_write.write(reference[1])
paper_write.close()
