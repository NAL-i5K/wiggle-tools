# Wiggle-Tools

Collection of scripts for generating [BigWig](http://genome.ucsc.edu/goldenPath/help/bigWig.html) files.

* [GCcontent2bigwig.py](GCcontent2bigwig.py): calculate GC content from a FASTA file and convert it to BigWig file format.

* [gap2bigwig.py](gap2bigwig.py): find out gap regions (i.e., N base) from a FASTA file and convert to a BigWig file format.

## Usage

* [GCcontent2bigwig.py](GCcontent2bigwig.py):
  ``` shell
    GCcontent2bigwig.py <FASTA file>
    [-o, --bigwig_filename=<output file name>
    -t, --tempfile
    -k, --keep_tempfile
    -g, --gzip]
  ```

* [gap2bigwig.py](gap2bigwig.py):
  ``` shell
    gap2bigwig.py <FASTA file>
    [-o, --bigwig_filename=<output file name>
     -t, --tempfile
     -k, --keep_tempfile
     -g, --gzip]
  ```

## Prerequsites

* Linux - tested on CentOS 6 x86_64 (should work on Mac, may work on windows if you can compile **wigToBigWig** by yourself)
* Python 2.7

## Installation

* wigToBigWig
  * Download binary:
    - linux: [http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/wigToBigWig](http://hgdownload.cse.ucsc.edu/admin/exe/linux.x86_64/wigToBigWig)
    - mac: [http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/wigToBigWig](http://hgdownload.cse.ucsc.edu/admin/exe/macOSX.x86_64/wigToBigWig)
  * Make wigToBigwig executable: `chmod +x wigToBigWig` 
  * Put in your `$PATH`, for example, most user have `/usr/local/bin` in `$PATH`, so just copy the binary into it: `cp wigToBigWig /usr/local/bin`
  
