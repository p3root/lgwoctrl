#!/usr/bin/perl
 
##########################################################################
# Modules
##########################################################################

use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
use Config::Simple;
use File::HomeDir;
use Cwd 'abs_path';
use LWP::UserAgent;
use JSON qw( decode_json );
use utf8;
use Encode qw(encode_utf8);
#use warnings;
use strict;
no strict "refs"; # we need it for template system

##########################################################################
# Variables
##########################################################################

our $cfg;
our $pcfg;
our $pphrase;
our $lang;
our $template_title;
our $installdir;
our $planguagefile;
our $table;
our $version;
our $psubfolder;
my  $home = File::HomeDir->my_home;
our $startPair;
our $queryurl;
our $res;
our $ua;
our $json;
our $decoded_json;
our $urlstatus;
our $urlstatuscode;
our $i;
our $results;
our $decoded_json;
our $lat;
our $long;
our $numrestotal;


##########################################################################
# Read Settings
##########################################################################

# Version of this script
$version = "0.0.2";

# Figure out in which subfolder we are installed
$psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

$cfg             = new Config::Simple("$home/config/system/general.cfg");
$installdir      = $cfg->param("BASE.INSTALLFOLDER");
$lang            = $cfg->param("BASE.LANG");

##########################################################################
# Language Settings
##########################################################################

# Standard is german
if ($lang eq "") {
  $lang = "de";
}

# If there's no template, use german
if (!-e "$installdir/templates/plugins/$psubfolder/$lang/language.dat") {
  $lang = "de";
}

# Read translations
$planguagefile = "$installdir/templates/plugins/$psubfolder/$lang/language.dat";
$pphrase = new Config::Simple($planguagefile);

##########################################################################
# Program
##########################################################################


$startPair = param('startPair');
$startPair = quotemeta($startPair);


##########################################################################
# Program
##########################################################################

print CGI::header();
my $file_to_write = "pair.html";
my $form_vis = "visible";
my $pairState = "";
 
$pcfg = new Config::Simple("$installdir/config/plugins/$psubfolder/lgtv.cfg");
my $lgtvip = $pcfg->param("SETTINGS.IP");


if($startPair) {
	my $pair_path = "$installdir/webfrontend/cgi/plugins/$psubfolder/bin/pair.js";	
        my $pair_ret_code = system("/usr/bin/node $pair_path $lgtvip");
	$form_vis = "hidden";

	if($pair_ret_code == 0) {
		$file_to_write = "pair_s.html";
		
		my $filename = "$installdir/webfrontend/cgi/plugins/$psubfolder/clientKey$lgtvip";
		open(my $fh, '<:encoding(UTF-8)', $filename) or die "Could not open file '$filename' $!";
		my $key = <$fh>;		
		
	
		$pcfg->param("SETTINGS.ClientKey", "$key");
		$pcfg->save();
		
		$pairState = "Success";
	}
	else {
		$file_to_write = "pair_e.html";
		$pairState = "Failure";
	}
}


$template_title = $pphrase->param("TXT0000") . " - " . $pphrase->param("TXT0001");

open(F,"$installdir/templates/plugins/$psubfolder/$lang/$file_to_write") || die "Missing template /templates/plugins/$psubfolder/$lang/$file_to_write";
  while (<F>) {
    $_ =~ s/<!--\$(.*?)-->/${$1}/g;
    print $_;
  }
close(F);


exit;

