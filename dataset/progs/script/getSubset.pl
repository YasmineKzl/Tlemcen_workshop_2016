#!/usr/bin/perl
use warnings;

$PERCENT_NOISE = "$ARGV[1]";

open(READLIST,"<$ARGV[0]") or die("File not found");


while(<READLIST>){
    chomp;
    $reads{$_}++;
}

$size = keys %reads;
$max_nb_read_noise = $PERCENT_NOISE * $size;
$nb_read_noise = 0;
$i=1;

while(<STDIN>){

     if($i==1){
        $id1=$_;
	$id1=~/^@([^\s]+)/;
	$read_id=$1;
     }elsif($i==2){
        $qual=$_;
     }elsif($i==3){
        $id2=$_;
     }elsif($i==4){
	$i=0;
        if($reads{$read_id}){
	    print $id1,$qual,$id2,$_;
	}elsif($nb_read_noise < $max_nb_read_noise){
	    print $id1,$qual,$id2,$_;
	    $nb_read_noise++;
	}
     }

$i++;
}
