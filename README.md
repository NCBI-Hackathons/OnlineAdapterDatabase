# AdapterBase

## Background

Adapters are short sequences that are attached to cDNA templates during preparation of next generation sequencing (NGS) libraries. Depending on the preparation of the NGS library and how it is sequenced, the raw NGS data may be contaminated with the adapter sequences. See [Didion et al. 2017](https://peerj.com/preprints/2452/) for more details.

Adapter trimming is a critical component of NGS data preprocessing. To trim adapters appropriately, it is necessary to know the sequences of the adapters that were used. However, adapter sequences are poorly documented and often are not included in the metadata of public database submissions (e.g. [SRA](https://www.ncbi.nlm.nih.gov/sra), [ENA](http://www.ebi.ac.uk/ena)).

## Goals

The goals of the AdapterBase are as follows, in decreasing order of importance:

1. Create a database schema to store adapter sequences and related metadata, and to link adapters to sequencing datasets. Adapters come in two flavors: 1) standard, widely used adapters (e.g. those found in Illumina NGS library preparation kits), and 2) custom adapters.
2. Create an API to access the data in the database. Ideally, this will be a GraphQL API, but REST is also fine for a prototype.
3. Create a simple web interface to browse and manage the data in the database.
4. Create language-specific bindings for the API. Preferably, Python will be the first language supported, but the responsible team can choose whichever language in which they're most comfortable.
5. Integrate the AdpaterBase API into [Atropos](https://github.com/jdidion/atropos), an NGS read trimming tool written in Python.

## Database

## API

## Web Interface

## Language Bindings

## Atropos Integration

## Project Team

