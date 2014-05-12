#!/bin/bash
cd ROUGE; ./duc2007.prepare.pl
cd ROUGE-EVAL; ./runROUGE.pl
cd ../../; python getResults.py "$1"
open results.txt