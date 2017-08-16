#!/usr/bin/env perl

use warnings;
use strict;

my $atroposOutput;
{
    local $/ = undef;
    open IN, $ARGV[0] or die "Can't find file $ARGV[0]: $!\n";
    $atroposOutput = <IN>;
    close IN;
}

open OUT, ">data/runRecords1.csv" or die "Can't write to data/runRecords1.csv: $!\n";
print OUT "Accession,owner,database,is_public,5’ adapter,3’ adapter,platform\n";

while ( $atroposOutput =~ m{-------------------------------------------------------------------------------
([DES]RR\d+),"(.+)"


=======
Input 1
=======

File: \1
Detected \d+ adapters/contaminants:
 1. Longest kmer: [GATC]+
    Name\(s\): ([^\n,]+)
.*?
=======
Input 2
=======

Detected \d adapters/contaminants:
1. Longest kmer: [GATC]+
   Name\(s\): ([^\n,]+)}msg ) {

    my $db = substr($1,0,1) eq "E" ? "European Bioinformatics Institute (EMBL-EBI)" : substr($1,0,1) eq "S" ? "NCBI Sequence Read Archives" : "DNA DataBank of Japan";
    print OUT "$1,Chaim A Schramm,$db,yes,$3,$4,$2\n";

}
 
close OUT;

