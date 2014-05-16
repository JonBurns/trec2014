#!/usr/bin/perl
$ROUGE="perl ../ROUGE-RELEASE-1.5.5/ROUGE-1.5.5.pl";

# DUC-2006 and DUC-2007
$cmd="$ROUGE -e ../ROUGE-RELEASE-1.5.5/data -n 2 -x -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -l 250 -a settings.xml > ROUGE.out";

# Gets LCS too, by removing -x
#$cmd="$ROUGE -e ../ROUGE-RELEASE-1.5.5/data -n 2 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -l 250 -a settings.xml > ROUGE.out";
# DUC2004
#$cmd="$ROUGE -e ../ROUGE-RELEASE-1.5.5/data -n 2 -m -2 4 -u -c 95 -r 1000 -f A -p 0.5 -t 0 -b 655 -a settings.xml > ROUGE.out";

# DUC-2004
#$cmd="$ROUGE -e ../ROUGE-RELEASE-1.5.5/data -n 4 -c 95 -m -b 655 -w 1.2 -a settings.xml > ROUGE.out";
print $cmd,"\n";
system($cmd);
