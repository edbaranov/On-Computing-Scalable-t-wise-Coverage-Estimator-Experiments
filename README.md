# Readme

This supplementary materials contain information for the reproduction of experiments and experiment results.  

## Results

Results folder contain csv files with experiment results. The files are grouped by the section number in which the corresponding experiment is described. File names start with a tool or an algorithm name, followed by the value of t (size of combination). In sections 5 and 6, there are two files for each algorithm and t value: `<alg>_<t>.csv` contains results for the approximations, `<alg>_<t>_comb.csv` includes the results for exact computation (with BLMCov or BLMMaxCov). In sections 7 and 8 results there files or folder with ttest in their name - such files contain results used for Welch's t-test. `-1` in table cells represent cases when computation has not been terminated. 
 
## Benchmarks

Benchmarks for experiments are publicly available at Zenodo.  

Benchmarks for sections 5 and 6: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5883536.svg)](https://doi.org/10.5281/zenodo.5883536)  

Benchmarks for sections 7 and 8: [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10220246.svg)](https://doi.org/10.5281/zenodo.10220246)   

## Experiments setup

### System Requirements:

Linux OS (tested on Ubuntu 18.04 LTS, Ubuntu 20.04 LTS, and Debian 12.2)

### General Comments

In all experiments we used random seeds from 1 to 10 (to 50 for Welch's t-test).  

### Sections 5 and 6

ApproxCov and ApproxMaxCov implementations are available at: [https://github.com/meelgroup/approxcov/](https://github.com/meelgroup/approxcov/)  
Readme file contains installation instructions. In our experiments we used revisions 30c6787 of approxmc and 641f915 of cryptominisat. Our implementation works with the latest versions of approxmc and cryptominisat (revisions d9f7d05 and 8c8e698).  

`scripts` folder contains 4 python scripts to compute Cov and MaxCov for binary and general cases.  
  
To run exact computation of combinations of cnf formula (BLMMaxCov) the command is:  
`python3 approxmaxcov.py --twise <twise> <cnf_file>`  
where   
1) twise is the number of features in combination (size of the combination),  
2) cnf_file - path to file in Dimacs format. 
Note that it might take several hours even for t=2 especially on large benchmarks  

To run the computation with ApproxMaxCov of combinations of cnf formula the command is:  
`python3 approxmaxcov.py --approximate --twise <twise> --seed <seed> <cnf_file>`  
where  
1) twise is the number of features in combination (size of the combination),  
2) seed sets up a random seed,  
3) cnf_file - path to file in Dimacs format.  
Optional arguments: `--delta <delta>` `--epsilon <epsilon>` define the accuracy: probability at least (1 − delta) the output of Approxmc is an (1 ± epsilon) multiplication approximation of the correct value. Default values are delta=0.05, epsilon=0.05.  

To compute the exact number of combinations in the sample set (BLMCov):  
`python3 approxcov.py --twise <twise>  <sample_file>`  
where  
1) twise is the number of features in combination (size of the combination),  
2) sample_file - path to file with samples.   

To compute the approximate number of combinations in the sample set (ApproxCov):  
`python3 approxcov.py --twise <twise> --approximate --seed <seed> <sample_file>`  
where  
1) twise is the number of features in combination (size of the combination),   
2) seed sets up a random seed,  
3) sample_file - path to file with samples.  
Optional arguments: `--delta <delta>` `--epsilon <epsilon>` define the accuracy: probability at least (1 − delta) the output of Approxmc is an (1 ± epsilon) multiplication approximation of the correct value. Default values are delta=0.05, epsilon=0.05. 

Note that sample_file is expected to follow the format generated by waps and baital tools. Each line starts with the sample number (ignored), followed by comma, followed by space separated list of literals defining the sample. Each literal shall be either positive integer in case the corresponding variable of CNF formula is evaluated to True or negative integer if evaluated to False. The list must contain all variables from CNF formula and sorted by variable number.

The usage for generalised algorithms is the same. The corresponding scripts are `approxmaxcov_mv.py` and `approxcov_mv.py`.  

Note that we expect the following format:  
For MaxCovGeneral - an smt file with QF_BV logic. First line is a comment line staring with 2 semicolon symbols and followed by a list of space-separated integers defining number of values each variable can have.  
For CovGeneral - first line is a list of space-separated integers defining number of values each variable can have. The following lines start with an ignored integer (sample number as in binary case), followed by comma, followed by space separated list of values for each literal. It is assumed that each literal has values between 0 and nb_of_values-1.
In the scripts for non-binary features there are functions to convert CASA format [Brady J Garvin, Myra B Cohen, and Matthew B Dwyer. 2009. An improved meta-heuristic search for constrained interaction testing] into the format accepted by our scripts.

### Section 7

Baital tool is available at [https://github.com/meelgroup/baital/](https://github.com/meelgroup/baital/)  

Readme file contains installation instructions. The main script is `baital.py` located in `src` folder.    

To improve the control over the experiment, we split the computation into three steps. For the original strategy we used:  

1) `python baital.py <benchmark_name> --preprocess-only --twise 2`  
2) `python baital.py <benchmark_name> --outputfile <samples_file> --waps --twise 2 --samples 1000 --strategy 1 --preprocess-file <preprocess_file> --cov-approximate --no-maxcov --seed <seed>`  
3) `python baital.py <benchmark_name> --no-sampling --samples-file <samples_file> --maxcov-file <preprocess_file> --twise 2`     

The first command runs a BLMMaxCov and stores the output in a file `results/<benchmark_name>_2.comb`. The second command performs the sampling: `<preprocess_file>` is a BLMMaxCov output file, `<samples_file> `is the file to store generated samples. The final command runs BLMCov to compute the coverage.  

For the new strategy the commands are the following:  

1) `python baital.py <benchmark_name> --preprocess-only --twise 2  --preprocess-approximate`   
2) `python baital.py <benchmark_name> --outputfile <samples_file> --waps --twise 2 --samples 1000 --strategy 3 --preprocess-file <preprocess_file> --cov-approximate --no-maxcov --seed <seed>`  
3) `python baital.py <benchmark_name> --no-sampling --samples-file <samples_file> --maxcov-file <BLMCov_preprocess_file> --twise 2`     

The first command runs a ApproxMaxCov and stores the output in a file `results/<benchmark_name>_2.acomb`. The second command performs the sampling: `<preprocess_file>` is an ApproxMaxCov output file, `<samples_file>` is the file to store generated samples. The final command runs BLMCov to compute the coverage. Note that for the last command we provide a preprocess_file computed for the original strategy (extension .comb).    

For the final part of the experiment where the new strategy is tested for higher values of t, we use the following commands (the final command runs ApproxCov and ApproxMaxCov):  

1) `python baital.py <benchmark_name> --preprocess-only --twise <twise>  --preprocess-approximate`   
2) `python baital.py <benchmark_name> --outputfile <samples_file> --waps --twise <twise> --samples 1000 --strategy 3 --preprocess-file <preprocess_file> --cov-approximate --no-maxcov --seed <seed>`  
3) `python baital.py <benchmark_name> --no-sampling --samples-file <samples_file> --cov-approximate --twise <twise>`  

Time reported in the csv tables are for steps 1 and 2.  


### Section 8

For this experiment we used Baital (installation instructions are in section 7), CMSGen (installed during Baital installation), LS-Sampling, and SamplingCA.

LS-Sampling is available at [https://github.com/chuanluocs/LS-Sampling](https://github.com/chuanluocs/LS-Sampling)  

Readme file contains installation instructions.

SamplingCA is available at [https://github.com/chuanluocs/SamplingCA](https://github.com/chuanluocs/SamplingCA)  

The modification described in the paper can be found in changes.patch file in the supplementary materials. The installation is the following:  
1) `cd SamplingCA`  
2) `git apply /path/to/changes.patch`  
3) `make`  

Sample sets have been generated with the following commands (run from the corresponding tool folder):

1) Uniform:  
`python baital.py <benchmark_name> --outputfile <samples_file> --rounds 1 --waps --twise 2 --samples 1000 --strategy 5 --cov-approximate --no-maxcov --seed <seed>`  
2) Baital3W:  
`python baital.py <benchmark_name> --outputfile <samples_file> --rounds 10 --waps --twise <twise> --samples 1000 --strategy 3 --cov-approximate --no-maxcov --seed <seed>`  
3) Baital5W:  
`python baital.py <benchmark_name> --outputfile <samples_file> --rounds 10 --waps --twise 2 --samples 1000 --strategy 5 --cov-approximate --no-maxcov --seed <seed>`  
4) Baital3C:  
`python baital.py <benchmark_name> --outputfile <samples_file> --rounds 10 --twise <twise> --samples 1000 --strategy 3 --extra-samples --no-maxcov --cov-approximate --seed <seed>`  
5) Baital5C:  
`python baital.py <benchmark_name> --outputfile <samples_file> --rounds 10 --twise 2 --samples 1000 --strategy 5 --extra-samples --cov-approximate --no-maxcov --seed <seed>`  
6) CMSGen:  
`./cmsgen <benchmark_name> --samplefile <output_file> --samples 1000 --seed 1`  
7) LS-Sampling:  
`./LS-Sampling -input_cnf_path <benchmark_name> -seed 1 -k 1000 -output_testcase_path <output_file> -no_coverage -t_wise 2 -lambda 100 -use_formula_simplification 1 -use_dynamic_updating_sampling_prob 1 -use_diversity_aware_heuristic_search 1`  
8) SamplingCA:  
`./SamplingCA -input_cnf_path <benchmark_name> -seed 1 -k 100 -output_testcase_path <output_file>`  

For the latter 3 tools `<output_file>` format has to be converted. We provide a python script `convert.py` in the supplementary materials. The usage is:  
`python3 convert.py --tool <tool_name> --outputfile <samples_file> <output_file>`  
`<tool_name>` is one of the samplingca, ls-sampling, cmsgen; `<output_file>` is the tool output; `<samples_file>` is the file created by the script with a format supported by ApproxCov

To compute the number of feature combimbinations either of the two scripts can be used:  
`python baital.py <benchmark_name> --no-sampling --samples-file <samples_file> --cov-approximate --twise <twise>  --cov-delta <delta> --cov-epsilon <epsilon>`   
`python3 approxcov.py --twise <twise>  <sample_file>  --cov-delta <delta> --cov-epsilon <epsilon>`  

For Uniform, Baital3W, and Baital5W we used `<delta>`=`<epsilon>`= 0.05, for the remaining tools `<delta>`=`<epsilon>`= 0.01
