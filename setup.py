import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='23andme-to-vcf',
    version='0.0.3',
    author='David Brown',
    author_email='david.brown@lifeomic.com',
    description='A simple script to convert 23andMe raw data files to VCF format.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/david-wb/23andme_to_vcf',
    scripts=['bin/23andme-to-vcf'],
    packages=setuptools.find_packages(),
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    )
)
