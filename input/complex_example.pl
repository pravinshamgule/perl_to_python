#!/usr/bin/perl
use strict;
use warnings;
use Scalar::Util qw(looks_like_number);
use Data::Dumper;

# This is a complex Perl example that uses various Perl features
# to test the enhanced Perl to Python converter

# Define a hash with various data types
my %config = (
    'name' => 'Complex Example',
    'version' => 1.0,
    'enabled' => 1,
    'features' => ['loops', 'regex', 'hash', 'array', 'functions'],
    'settings' => {
        'debug' => 0,
        'verbose' => 1,
        'timeout' => 30
    }
);

# Define an array
my @numbers = (1..10);

# Define a subroutine to process data
sub process_data {
    my ($data, $options) = @_;
    
    # Check if data is defined
    unless (defined $data) {
        die "Error: No data provided.\n";
    }
    
    # Check if data is a reference
    unless (ref($data) eq 'HASH') {
        die "Error: Data must be a hash reference.\n";
    }
    
    # Set default options
    $options = {} unless defined $options;
    
    # Extract options with defaults
    my $debug = exists $options->{debug} ? $options->{debug} : 0;
    my $verbose = exists $options->{verbose} ? $options->{verbose} : 0;
    
    # Print debug information
    if ($debug) {
        print "Debug: Processing data with options:\n";
        print Dumper($options);
    }
    
    # Process each key in the data
    my $result = {};
    foreach my $key (keys %$data) {
        my $value = $data->{$key};
        
        # Skip undefined values
        next unless defined $value;
        
        # Process value based on type
        if (ref($value) eq 'ARRAY') {
            # Process array values
            my @processed = map { process_value($_, $debug) } @$value;
            $result->{$key} = \@processed;
        } elsif (ref($value) eq 'HASH') {
            # Recursively process nested hash
            $result->{$key} = process_data($value, $options);
        } else {
            # Process scalar value
            $result->{$key} = process_value($value, $debug);
        }
        
        # Print verbose information
        if ($verbose) {
            print "Processed key: $key\n";
        }
    }
    
    return $result;
}

# Helper function to process a single value
sub process_value {
    my ($value, $debug) = @_;
    
    # Print debug information
    if ($debug) {
        print "Debug: Processing value: $value\n";
    }
    
    # Check if value is a number
    if (looks_like_number($value)) {
        # Double numeric values
        return $value * 2;
    } elsif ($value =~ m/^[a-zA-Z]+$/) {
        # Uppercase alphabetic values
        return uc($value);
    } else {
        # Add prefix to other values
        return "processed_" . $value;
    }
}

# Function to demonstrate regex operations
sub regex_demo {
    my ($text) = @_;
    
    # Default text if not provided
    $text = "Hello, World! This is a test." unless defined $text;
    
    # Match operation
    if ($text =~ m/Hello/) {
        print "Text contains 'Hello'\n";
    }
    
    # Case-insensitive match
    if ($text =~ m/world/i) {
        print "Text contains 'world' (case-insensitive)\n";
    }
    
    # Substitution
    my $modified = $text;
    $modified =~ s/Hello/Hi/;
    print "After substitution: $modified\n";
    
    # Global substitution
    $modified =~ s/[aeiou]/*/g;
    print "After vowel replacement: $modified\n";
    
    # Translation
    my $uppercase = $text;
    $uppercase =~ tr/a-z/A-Z/;
    print "Uppercase: $uppercase\n";
    
    return $modified;
}

# Function to demonstrate loop constructs
sub loop_demo {
    my ($count) = @_;
    
    # Default count if not provided
    $count = 5 unless defined $count;
    
    # For loop with range
    print "For loop with range:\n";
    for my $i (1..$count) {
        print "  i = $i\n";
    }
    
    # Foreach loop with array
    print "Foreach loop with array:\n";
    my @items = ('apple', 'banana', 'orange', 'grape', 'kiwi');
    foreach my $item (@items) {
        print "  item = $item\n";
    }
    
    # While loop
    print "While loop:\n";
    my $i = 0;
    while ($i < $count) {
        print "  i = $i\n";
        $i++;
    }
    
    # Until loop
    print "Until loop:\n";
    my $j = $count;
    until ($j <= 0) {
        print "  j = $j\n";
        $j--;
    }
    
    return $count;
}

# Main script
print "Starting complex example...\n";

# Get command line arguments
my ($mode, $input_file) = @ARGV;

# Set default mode if not provided
$mode = "default" unless defined $mode;

# Process based on mode
if ($mode eq "regex") {
    print "Running regex demo...\n";
    my $result = regex_demo();
    print "Regex demo completed with result: $result\n";
} elsif ($mode eq "loop") {
    print "Running loop demo...\n";
    my $count = 3;
    my $result = loop_demo($count);
    print "Loop demo completed with count: $result\n";
} elsif ($mode eq "file" && defined $input_file) {
    print "Processing file: $input_file\n";
    
    # Check if file exists
    unless (-e $input_file) {
        die "Error: File not found: $input_file\n";
    }
    
    # Read file content
    open my $fh, '<', $input_file or die "Error opening file: $!\n";
    my $content = do { local $/; <$fh> };
    close $fh;
    
    # Process file content
    my %data = (
        'filename' => $input_file,
        'content' => $content,
        'size' => -s $input_file,
        'lines' => scalar(split /\n/, $content)
    );
    
    my $result = process_data(\%data, { 'debug' => 1, 'verbose' => 1 });
    print "File processing completed.\n";
    print "Result:\n";
    print Dumper($result);
} else {
    # Default mode: process config data
    print "Processing config data...\n";
    my $result = process_data(\%config, { 'debug' => $config{settings}{debug}, 'verbose' => $config{settings}{verbose} });
    print "Config processing completed.\n";
    print "Result:\n";
    print Dumper($result);
}

print "Complex example completed.\n";