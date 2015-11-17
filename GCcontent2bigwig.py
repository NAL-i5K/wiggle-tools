#!/usr/bin/env python
import os
import sys
import subprocess
import tempfile
import re
from optparse import OptionParser
from contextlib import contextmanager

'''
Calculate GC content from a FASTA file and convert it to BigWig file format.

Usage:
	GCcontent2bigwig.py <FASTA file>
	[-o, --bigwig_filename=<output file name>
	 -t, --tempfile
	 -k, --keep_tempfile
	 -g, --gzip]

Prerequisites:
  ucsc_bigwig: wigToBigWig can be downloaded from UCSC Genome Browser (http://hgdownload.cse.ucsc.edu/admin/exe/)

(c) Chien-Yueh Lee 2014-2015 / MIT Licence
kinomoto[AT]sakura[DOT]idv[DOT]tw
'''

def main(fasta_filename, bigwig_filename=None, use_tempfile=False, keep_tempfile=False, use_gzip=False):
	input_file_prefix = os.path.splitext(fasta_filename)[0]
	if bigwig_filename is None:
		bigwig_filename = '%s.bigwig' % input_file_prefix
		
	output_file_prefix = os.path.splitext(bigwig_filename)[0]
	
	if os.path.abspath(fasta_filename) == os.path.abspath(bigwig_filename):
		sys.stderr.write('Bad arguments, input and output files are the same.\n')
		sys.exit(1)

	# generate wig file
	wig_filename = '%s.wig' % output_file_prefix
	if use_tempfile:
		wig_filename = tempfile.NamedTemporaryFile(delete=False).name
	wig_file = open(wig_filename, "w")

	# generate chromosome sizes file
	chr_sizes_filename = '%s.sizes' % output_file_prefix
	if use_tempfile:
		chr_sizes_filename = tempfile.NamedTemporaryFile(delete=False).name
	chr_sizes = open(chr_sizes_filename, "w")

	MaxScore = 100
	minScore = -100
	base_start_pos = 0
	continuous_base_len = 0
	previous_base = ""
	chromosome = "My_sequence"
	counter = 0
	sizes = dict()
	base_score = {"C":1, "G":1, "A":-1, "T":-1, "N":0}
	base_substitution = {"C":"CG", "G":"CG", "A":"AT", "T":"AT", "N":"N"}
	
	if use_gzip:
		import gzip
		fp = gzip.open(fasta_filename, "rb")
	else:
		fp = open(fasta_filename, "r")
		
	for line in fp:
		line = line.strip()
		if len(line) > 0:
			if line[0] == ">":  # in header
				if "nucl" in dir():
					if nucl != "N": # Processing the last base
						wig_file.write("fixedStep chrom=%s start=%i step=1 span=%i\n%i\n" % (chromosome, base_start_pos, continuous_base_len, base_score[previous_base]))
						base_start_pos = 0
						continuous_base_len = 0
						previous_base = ""

				m = re.findall("(?<=>)[\w\-\|.]+", line)
				if m is not None:
					chromosome = m[0]
					counter = 0
					print "Processing %s" % m[0]
				else:
					print "No chromosome match!"
					sys.exit(1)
			else:   # in seq.
				for nucl in line:
					counter+=1
					sizes[chromosome] = counter # count chromosome size
					nucl = nucl.upper()

					if previous_base == "":	# in the first base
						wig_file.write("fixedStep chrom=%s start=1 step=1 span=1\n" % (chromosome))
						previous_base = nucl
						continuous_base_len = 1
						base_start_pos = 1
						continue

					# if nucl == "N":
						# if previous_base != "N":
							# wig_file.write("fixedStep chrom=%s start=%i step=1 span=%i\n%i\n" % (chromosome, base_start_pos, continuous_base_len, base_score[previous_base]))
						
						# previous_base = "N"
						# continuous_base_len = 1
						# base_start_pos = counter+1
						# continue

					elif base_substitution[nucl] == base_substitution[previous_base]: # hit bases continuously
						continuous_base_len+=1

					else:
						#wig_file.write("fixedStep chrom=%s start=%i step=1 span=%i\n%i\n" % (chromosome, base_start_pos, continuous_base_len, base_score[previous_base]))
						for ii in range(0,continuous_base_len):
							if base_score[previous_base]*continuous_base_len > MaxScore:
								wig_file.write("%i\n" % (MaxScore))
							elif base_score[previous_base]*continuous_base_len < minScore:
								wig_file.write("%i\n" % (minScore))
							else:
								wig_file.write("%i\n" % (base_score[previous_base]*continuous_base_len))
						
						continuous_base_len = 1
						base_start_pos = counter
					
					previous_base = nucl

			# if continuous_base_len > 1:
				# for ii in range(0,continuous_base_len):
					# if base_score[previous_base]*continuous_base_len > MaxScore:
						# wig_file.write("%i\n" % (MaxScore))
					# elif base_score[previous_base]*continuous_base_len < minScore:
						# wig_file.write("%i\n" % (minScore))
					# else:
						# wig_file.write("%i\n" % (base_score[previous_base]*continuous_base_len))
			# else:
				 # wig_file.write("%i\n" % (base_score[previous_base]*continuous_base_len))

	for key, value in sizes.items():
		chr_sizes.write("%s\t%i\n"%(key, value))
	
	fp.close()
	wig_file.close()
	chr_sizes.close()

	print "Converting wig to bigwig"
	cl = ["wigToBigWig", wig_filename, chr_sizes_filename, bigwig_filename]
	subprocess.check_call(cl)

	# remove temp files
	if not keep_tempfile:
		os.remove(chr_sizes_filename)
		os.remove(wig_filename)

	print "Done."

if __name__ == '__main__':
	parser = OptionParser()
	parser.add_option('-o', '--bigwig_filename', dest='bigwig_filename')
	parser.add_option('-t', '--tempfile', dest='use_tempfile',
					  action='store_true', default=False)
	parser.add_option('-k', '--keeptemp', dest='keep_tempfile',
					  action='store_true', default=False)
	parser.add_option('-g', '--gzip', dest='use_gzip',
					  action='store_true', default=False)
	(options, args) = parser.parse_args()
	if len(args) == 0:
		print __doc__
		sys.exit()
	kwargs = dict(
		bigwig_filename=options.bigwig_filename,
		use_tempfile=options.use_tempfile,
		keep_tempfile=options.keep_tempfile,
		use_gzip=options.use_gzip)
	for fasta_filename in args:
		main(fasta_filename, **kwargs)
