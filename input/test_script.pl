#!/usr/bin/perl
use strict;
use warnings;
use FindBin;
use lib $FindBin::Bin;  # Add current directory to module search path
use StringUtils qw(to_uppercase);

# Test input
my $input = "hello world";

# Convert and print
my $output = to_uppercase($input);
print "Uppercase: $output\n";
