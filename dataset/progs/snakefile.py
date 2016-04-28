import os

WORKDIR = "/gpfs/tagc/home/puthier/016_TLEMCEN/Tlemcen_workshop_2016/dataset"

workdir: WORKDIR

FQDIR = "/gpfs/tagc/home/puthier/013_LAN_RNA_SEQ_extended/input/fastq"
BAMDIR  = "/gpfs/tagc/home/puthier/013_LAN_RNA_SEQ_extended/output/bam/"

SMP = ["PI1", "PI2", "PI3","DM1","DM2","DM3"]

CHR = ["chr17", "chr18"]

SENS = ["R1", "R2"]

rule all:
    input: expand("output/fastq/{smp}_{chr}_{sens}.fq.gz", smp=SMP, chr=CHR, sens=SENS)
    threads: 1

rule get_read_ids:
    input: bam = os.path.join(BAMDIR, "{smp}.bam")
    threads: 1
    output: ids= "output/bam/{smp}_{chr}_ids.txt"
    shell: """
     	    samtools view {input.bam} | awk 'BEGIN{{ FS=OFS="\t" }}{{ if($3=="{wildcards.chr}"){{ print $0 }} }}' | cut -f1 > {output.ids}
	    """


rule get_reads:
    input: ids= "output/bam/{smp}_{chr}_ids.txt", fq = os.path.join(FQDIR, "{smp}_{sens}.fq.gz")
    threads: 1
    output: "output/fastq/{smp}_{chr}_{sens}.fq.gz"
    shell: """ 
    gunzip -c {input.fq}  | progs/script/getSubset.pl {input.ids} 0.1 | gzip >  {output}     
	    """





