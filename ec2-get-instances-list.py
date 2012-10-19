#!/usr/bin/python

# this script will generate a text file with using <tab> as field separator
# to import it to Google Docs, for example, open file, specified as out using MS Office Excel / Libreoffice Calc / etc
# open it as csv and set fields separator. You will get a pretty and usable table

import subprocess

#specify your ec2 tools credentials here
ec2_key='/work/ec2tools.pem'
ec2_cert='/work/ec2tools.cert'

try:
	with open (ec2_key) as f: pass
except:
	print "Error! ec2_key doesn't exist!"

try:
	with open (ec2_cert) as f: pass
except:
	print "Error! ec2_cert doesn't exist!"


file='/tmp/ec2-new'
out='/tmp/ec2-out.csv'

fout=open(out,'w')

def fileexists(file):
	try:
		with open(file) as f: pass
	except:
		f = open(file, 'w+')
	f.close()

fileexists(out)
fout=open(out,'w')

subprocess.call("ec2-describe-instances -K %s -C %s | grep -v 'BLOCKDEVICE' > %s" %(ec2_key, ec2_cert, file), shell=True,executable='/bin/bash')

f=open(file,'r')
rlines=f.readlines()

def getinstances(onlyrunning):
	for line in rlines:
		final={}
		if 'INSTANCE' in line:
			i = rlines.index(line)
			if 'stopped' not in line:
				llist=line.split()
				final['instance']=llist[1]
				final['DNS']=llist[3]
				final['Size']=llist[8]
				final['State']='running'
				#print final
			else:
				final['instance']=llist[1]
				final['DNS']='no'
				final['Size']=llist[8]
				final['State']='stopped'
				#print final
			j=1
			while (j < 10) and (i+j>0):
				if 'INSTANCE' in rlines[i-j]:
					break
				if 'RESERVATION' in rlines[i-j]:
					final['Groups']=rlines[i-j].split()[-1]
				j+=1
			j=1
			while (j < 10) and (i+j < len(rlines)):
				if 'INSTANCE' in rlines[i+j]:
					break
				if 'TAG' in rlines[i+j]:
					if 'Customer' in rlines[i+j]:
						final['Customer']=rlines[i+j].split()[-1]
					if 'Product' in rlines[i+j]:
						final['Product']=rlines[i+j].split()[-1]
					if 'Purpose' in rlines[i+j]:
						final['Purpose']=rlines[i+j].split()[-1]
					#final
				j+=1
			testlist = ['Customer', 'Product', 'Purpose']
			for i in testlist:
				if i not in final:
					final[i]='No_data'
			if 'Groups' not in final:
					final['Groups']='No_groups'
			if onlyrunning:
				if final['State']=='running':
					fout.write(final['instance']+';'+final['DNS']+';'+final['Size']+';'+final['Groups']+';'+final['State']+';'+final['Customer']+';'+final['Product']+';'+final['Purpose']+'\n')
			else:
				fout.write(final['instance']+';'+final['DNS']+';'+final['Size']+';'+final['Groups']+';'+final['State']+';'+final['Customer']+';'+final['Product']+';'+final['Purpose']+'\n')
	fout.close()

#getinstances(True) - for only running instances
#False - for all instances
getinstances(True)
