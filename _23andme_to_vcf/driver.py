import argparse
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--input', help='A 23andme data file', required=True)
parser.add_argument('--output', help='Output VCF file', required=True)
parser.add_argument('--fasta', help='An uncompressed reference genome GRCh37 fasta file', required=True)
parser.add_argument('--fai', help='The fasta index for for the reference', required=True)

def load_fai(args):
    index = {}
    with open(args.fai) as f:
        for line in f:
            toks = line.split('\t')
            chrom = 'chr' + toks[0]
            if chrom == 'chrMT':
                chrom = 'chrM'
            length = int(toks[1])
            start = int(toks[2])
            linebases = int(toks[3])
            linewidth = int(toks[4])
            index[chrom] = (start, length, linebases, linewidth)
    return index

def get_vcf_records(pos_list, fai, args):
    with open(args.fasta) as f:
        def get_alts(ref, genotype):
            for x in genotype:
                assert x in 'ACGT'

            if len(genotype) == 1:
                if ref in genotype:
                    return []
                return [genotype]

            if ref == genotype[0] and ref == genotype[1]:
                return []
            if ref == genotype[0]:
                return [genotype[1]]
            if ref == genotype[1]:
                return [genotype[0]]
            return [genotype[0], genotype[1]]

        for (rsid, chrom, pos, genotype) in pos_list:
            start, _, linebases, linewidth = fai[chrom]
            n_lines = int(pos / linebases)
            n_bases = pos % linebases
            n_bytes = start + n_lines * linewidth + n_bases
            f.seek(n_bytes)
            ref = f.read(1)
            alts = get_alts(ref, genotype)
            pos = str(pos + 1)
            diploid = len(genotype) == 2
            assert ref not in alts
            assert len(alts) <= 2
            if diploid:
                if len(alts) == 2:
                    if alts[0] == alts[1]:
                        yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '1/1')
                    else:
                        yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '1/2')
                        yield (chrom, pos, rsid, ref, alts[1], '.', '.', '.', 'GT', '2/1')
                elif len(alts) == 1:
                    yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '0/1')
            elif len(alts) == 1: 
                yield (chrom, pos, rsid, ref, alts[0], '.', '.', '.', 'GT', '1')

def load_23andme_data(input):
    with open(input) as f:
        for line in f:
            if line.startswith('#'): continue
            if line.strip():
                rsid, chrom, pos, genotype = line.strip().split('\t')
                if chrom == 'MT':
                    chrom = 'M'
                chrom = 'chr' + chrom
                if genotype != '--':
                    skip = False
                    for x in genotype:
                        if x not in 'ACTG':
                            skip = True
                    if not skip:
                        yield rsid, chrom, int(pos) - 1, genotype # subtract one because positions are 1-based indices

def write_vcf_header(f):
    f.write(
"""##fileformat=VCFv4.2
##source=23andme_to_vcf
##reference=GRCh37
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM POS ID REF ALT QUAL FILTER INFO FORMAT SAMPLE
""")

def write_vcf(outfile, records):
    with open(outfile, 'w') as f:
        write_vcf_header(f)
        for record in records:
            f.write('\t'.join(record) + '\n')

def main():
    args = parser.parse_args()
    fai = load_fai(args)
    snps = load_23andme_data(args.input)
    records = get_vcf_records(snps, fai, args)
    write_vcf(args.output, records)