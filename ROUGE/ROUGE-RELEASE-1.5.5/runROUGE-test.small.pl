#!/usr/bin/perl
use Cwd;
$curdir=getcwd;
$ROUGE="../ROUGE-1.5.5.pl";
chdir("sample-test");
$cmd="$ROUGE -e ../data -c 95 -2 -1 -U -r 1000 -n 4 -w 1.2 -a ROUGE-test.xml > ../sample-output/ROUGE-test-c95-2-1-U-r1000-n4-w1.2-a.out";
print $cmd,"\n";
system($cmd);
$cmd="$ROUGE -e ../data -c 95 -2 -1 -U -r 1000 -n 4 -w 1.2 -a -m ROUGE-test.xml > ../sample-output/ROUGE-test-c95-2-1-U-r1000-n4-w1.2-a-m.out";
print $cmd,"\n";
system($cmd);
chdir($curdir);
