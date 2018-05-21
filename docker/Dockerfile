FROM python:3.6-slim

ARG AWS_ACCESS_KEY_ID
ARG AWS_SECRET_ACCESS_KEY
ARG AWS_SESSION_TOKEN

ENV AWS_REGION us-east-1
ENV AWS_ACCESS_KEY_ID $AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY $AWS_SECRET_ACCESS_KEY
ENV AWS_SESSION_TOKEN $AWS_SESSION_TOKEN

RUN pip install --upgrade pip \
    && pip install awscli \
    && pip install 23andme-to-vcf

RUN aws s3 cp s3://lifeomic-dev-gnosis/genome/genome-GRCh37/1/GRCh37.fa.gz /data/ \
    && aws s3 cp s3://lifeomic-dev-gnosis/genome/genome-GRCh37/1/GRCh37.fa.gz.fai /data/ \
    && cd /data && gunzip GRCh37.fa.gz

RUN echo $AWS_ACCESS_KEY_ID

ENTRYPOINT ["23andme-to-vcf", "--fasta", "/data/GRCh37.fa", "--fai", "/data/GRCh37.fa.gz.fai"]