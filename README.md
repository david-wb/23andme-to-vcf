# 23andme to VCF

A simple command-line tool to convert 23andMe raw data files to VCF format.

# Install
```
pip install 23andme-to-vcf
```

# Usage

```
23andme-to-vcf --input in.txt --fasta GRCh37.fa --fai GRCh37.fa.fai --output out.vcf
```

Alternatively, run the public docker image `davidwb/23andme-to-vcf` which already contains the reference and fasta index:

```
docker run -v `pwd`:/app/data davidwb/23andme-to-vcf --input genome_David_Brown_v4_Full_20180518133503.txt --output david_23andme.vcf
```