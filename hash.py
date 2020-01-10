'''
Created on Jan 7, 2020

@author: Jonathon Schnell

@date: 1/7/2019

@version: 1.0.1

'''
import argparse
import hashlib
import sys
import os.path

if __name__ == "__main__":
	#argument parser
	parser = argparse.ArgumentParser()
	parser.add_argument("string", help="[string] OR [filename.txt] to be hashed")
	parser.add_argument("algorithm", help="algorithm to be used [sha1], [sha224], [sha384], [sha256], [sha512], [md5]")
	parser.add_argument("-f", "--file", nargs='?', default='false', help="save hashes to an output file [filename.txt] main argument [string] must also be [filename.txt]")
	parser.add_argument("-d", "--dictionary", action="store", nargs='?', default='false', help="generate a dictionary file [filename.txt]")


	args = parser.parse_args()
	
	string = args.string
	algorithm = args.algorithm
	
	
	#check to see if fn can be opened
	def fileCheck(fn):
		try:
			open(fn, "r")
			return 1
		except IOError:
			sys.exit("Error: File does not appear to exist.")
	
	#check to see if output file exists
	def fileExist(fn):
		if os.path.isfile(fn):
			sys.exit("Error: File exist please choose a different name")

	#passed a string and algorithm an returns hash
	def hashString(string, algorithm):
		if algorithm == "sha1":
			return(hashlib.sha1(string).hexdigest())
		elif algorithm == "sha224":
			return(hashlib.sha224(string).hexdigest())
		elif algorithm == "sha384":
			return(hashlib.sha384(string).hexdigest())
		elif algorithm == "sha256":
			return(hashlib.sha256(string).hexdigest())
		elif algorithm == "sha512":
			return(hashlib.sha512(string).hexdigest())
		elif algorithm == "md5":
			return(hashlib.md5(string).hexdigest())
		else:
			return(args.algorithm + " is not valid a valid algorithm")
		
	def getString(string):
		rd = open(string, "r")
		outString = []
		while 1:
			line = rd.readline()
			if not line :
				break;
			outString.append(line)
		return outString
		rd.close()
		
	#opens file reads strings line by line and returns array of hashes then closes file
	def hashFile(string, algorithm):
		rd = open(string, "r")
		out = []
		while 1:
			line = rd.readline()
			if not line :
				break;
			out.append(hashString(line, algorithm))
		return out
		rd.close()
	
	#saves hashed string to outfile.txt
	def hashFileOut(string, algorithm, outfile):
		out = hashFile(string, algorithm)
		wr = open(outfile, "w")
		wr.write("\n".join(out))
		wr.write("\n")
		wr.close()
		print(outfile + " created")
		
	def hashDictionary(string, algorithm, outDictionary):
		out = hashFile(string, algorithm)
		outString = getString(string)
		wr = open(outDictionary, "w")
		i=1
		while i <= out.__len__() - 1:
			o = out[i]
			os = outString[i]
			wr.write(o + " : " + os)
			i += 1
		wr.close()
		print(outDictionary + " created")
	
	#if -d is set to an output dictionary
	if args.dictionary != "false":
		outDictionary = args.dictionary
		fileCheck(string)
		fileExist(outDictionary)
		hashDictionary(string, algorithm, outDictionary)
	
	#if -f is set to an outputfile
	elif args.file != "false":
		outfile = args.file
		fileCheck(string)
		fileExist(outfile)
		hashFileOut(string, algorithm, outfile)
		
	#if string contains ".txt"
	elif ".txt" in string:
		fileCheck(string)
		out = hashFile(string, algorithm)
		print "\n".join(out)
		
	#base case
	#if string is just a single string to be hashed and printed
	#cannot output to a file
	else:
		print(hashString(string, algorithm))
		