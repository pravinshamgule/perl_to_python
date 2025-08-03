#!/usr/bin/perl
# A simple Perl script to demonstrate the conversion process

use strict;
use warnings;
use Data::Dumper;
use Getopt::Long;

# Define command-line options
my $verbose = 0;
my $name = "World";
my $count = 1;
my $help = 0;

GetOptions(
    "verbose!" => \$verbose,
    "name=s" => \$name,
    "count=i" => \$count,
    "help" => \$help
) or die("Error in command line arguments\n");

# Display help if requested
if ($help) {
    print_help();
    exit(0);
}

# Main function
sub main {
    print "Starting the program...\n" if $verbose;
    
    for (my $i = 0; $i < $count; $i++) {
        say_hello($name);
    }
    
    # Create a hash (dictionary in Python)
    my %person = (
        "name" => $name,
        "greeting_count" => $count,
        "timestamp" => time()
    );
    
    # Print the hash using Data::Dumper
    if ($verbose) {
        print "Person details:\n";
        print Dumper(\%person);
    }
    
    return 0;
}

# Function to say hello
sub say_hello {
    my ($name) = @_;
    print "Hello, $name!\n";
}

# Function to print help
sub print_help {
    print <<EOF;
Usage: $0 [options]

Options:
  --name=NAME     Name to greet (default: World)
  --count=N       Number of times to greet (default: 1)
  --verbose       Enable verbose output
  --help          Display this help message

Example:
  $0 --name="John Doe" --count=3 --verbose
EOF
}

# POD documentation
=pod

=head1 NAME

hello_world.pl - A simple Perl script to demonstrate Perl to Python conversion

=head1 SYNOPSIS

hello_world.pl [options]

=head1 DESCRIPTION

This is a simple Perl script that demonstrates various Perl features
that will be converted to Python by the Perl to Python conversion agent.

=head1 OPTIONS

=over 4

=item B<--name>=NAME

Name to greet (default: World)

=item B<--count>=N

Number of times to greet (default: 1)

=item B<--verbose>

Enable verbose output

=item B<--help>

Display help message

=back

=head1 AUTHOR

Perl to Python Conversion Agent

=cut

# Call the main function
exit main();