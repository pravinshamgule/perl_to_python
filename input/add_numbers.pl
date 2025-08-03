#!/usr/bin/perl
use strict;
use warnings;
use Scalar::Util qw(looks_like_number);

# Get inputs from command line or ask interactively
my ($num1, $num2) = @ARGV;

unless (defined $num1 && defined $num2) {
    print "Enter first number: ";
    chomp($num1 = <STDIN>);
    
    print "Enter second number: ";
    chomp($num2 = <STDIN>);
}

# Validate inputs
unless (looks_like_number($num1)) {
    die "Error: First input '$num1' is not a valid number.\n";
}

unless (looks_like_number($num2)) {
    die "Error: Second input '$num2' is not a valid number.\n";
}

# Perform addition
my $sum = $num1 + $num2;

# Output the result
print "The sum of $num1 and $num2 is: $sum\n";
