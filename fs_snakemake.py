#!snakemake

## Run with:
## conda activate snakemake
## snakemake -c1 -s fs_snakemake.py
#
# Very helpful tutorial:
# https://carpentries-incubator.github.io/workflows-snakemake/

###########
###########
###########
###########
## Libraries
import os
import urllib.request
from requests import get  # to make GET request

###########
###########
###########
###########
## Functions
def download(url, file_name,verbose=True):
    """Downloads file_name from url, creating directories as needed for storage"""
    os.makedirs(os.path.dirname(file_name), exist_ok=True)
    if(verbose):
        print("Downloading "+url+" as "+file_name)
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = get(url)
        # write to file
        file.write(response.content)

def fscp(cpfile,dataroot,threads=1,verbose=True):
    """Runs fs as far as chromocombine completion"""
    fscmd="fs " + cpfile \
        + " -numthreads " + str(threads) \
  	    + " -idfile " + dataroot + ".ids" \
  	    + " -phasefiles " + dataroot + ".phase" \
  	    + " -recombfiles " + dataroot + ".recombfile" \
	    + " -combines2"
    if(verbose):
        print(fscmd)
    shell(fscmd)

def fsfs(cpfile,dataroot,threads=1,verbose=True):
    """Runs fs to finestructure completion"""
    fscmd="fs " + cpfile \
        + " -numthreads " + str(threads) \
  	    + " -go"
    if(verbose):
        print(fscmd)
    shell(fscmd)

###########
###########
###########
###########
# PARAMETERS
repo="https://raw.githubusercontent.com/danjlawson/finestructure4/main/examples/example1/"
DATAEXTS=["ids","phase","recombfile"]
examples="example_cp"
threads=4
verbose=True

###########
###########
###########
###########
## Rules

## Dummy rule to enforce the command getting run
rule all:
    input:
        "example_cp_linked_tree.xml"

## Download our data
rule download:
    output: expand("data/example_cp.{ext}",ext=DATAEXTS)
    run:
         for f in DATAEXTS:
             download(repo + "example_cp." + f,"data/example_cp."+f,verbose=verbose)

## Run chromopainter
rule cp:
    input: expand("data/example_cp.{ext}",ext=DATAEXTS)
    output: "example_cp_linked.chunkcounts.out"
    threads: threads
    run:
      fscp("example_cp.cp","data/example_cp",threads,verbose=verbose)

## Run finestructure
rule fs:
    input: "example_cp_linked.chunkcounts.out"
    output: "example_cp_linked_tree.xml"
    threads: threads
    run:
      fsfs("example_cp.cp","data/example_cp",threads,verbose=verbose)

## Cleaning up after ourselves
rule clean:
    shell:"""
rm -rf example_cp* data
"""
