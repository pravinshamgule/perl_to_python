#!/usr/bin/perl
use strict;
use warnings;

my $prod = $ARGV[0] // 36;
my $msg  = 'a' x $prod;

for my $i (2 .. $prod / 2) {
    for my $j ($i .. $prod / $i) {
        if ($msg =~ /^(?:a{$i}){$j}\z/) {
            say "$j * $i == $prod";
        }
    }
}