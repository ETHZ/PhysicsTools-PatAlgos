#!/bin/env perl
#
# Replaces for fast simulation
#
# Usage: $0 <output file> <replaces file>

use strict;

die "Usage: $0 <output> <replaces>\n" if ( @ARGV != 2 );

my $cfgFile = $ARGV[0];
my $replaceFile = $ARGV[1];

my %replaces;

# Get list of replaces
open(IN,$replaceFile) or die "Couldn't open $replaceFile: $!";
while( <IN> ) {
  if ( /replace\s+(\S+)(\s*=.*)[#|\/\/]?/ ) {
    $replaces{$1} = $2;
  }
}
close(IN);

# Scan cfgfile and replace
my $temp = $cfgFile.".tmp";
open(TEMP,">$temp") or die "Couldn't open $temp: $!";
open(CFG,$cfgFile) or die "Couldn't open $cfgFile: $!";
while ( <CFG> ) {
  chomp();
  my $line = $_;
  my $matched = 0;
  foreach my $replace ( keys %replaces ) {
    next if ( !$replaces{$replace} );
    if ( $line =~ /$replace/ ) {
      print TEMP "replace ".$replace.$replaces{$replace}."\n";
      $replaces{$replace} = 0;
      ++$matched;
      last;
    }
  }
  if ( !$matched ) {
    print TEMP $line."\n";
  }
}
close(CFG);

# Add missing items at the end of file

foreach my $replace ( keys %replaces ) {
  next if ( !$replaces{$replace} );
  print TEMP "replace ".$replace.$replaces{$replace}."\n";
}
close(TEMP) or die "Couldn't close $temp: $!";
rename($temp,$cfgFile);
