package StringUtils;

use strict;
use warnings;
use Exporter 'import';

# Export function by default
our @EXPORT_OK = qw(to_uppercase);

# Function to convert lowercase string to uppercase
sub to_uppercase {
    my ($input) = @_;
    
    # Check if input is defined
    die "Error: No input string provided.\n" unless defined $input;

    # Check if it's a string (scalar)
    unless (!ref($input)) {
        die "Error: Input must be a scalar string.\n";
    }

    # Convert to uppercase
    my $upper = uc($input);
    return $upper;
}

1;  # Return true to indicate successful loading of the module
