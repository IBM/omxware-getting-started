### Description:  
A Docker container with the contents necessary to identify the comprehensive set of the molecular targets in SARS-CoV-2 genomes with high set membership and sequence identity accuracy

### Usage:  
1. Download required bioinfomatics tools at the links provided `docker-build.sh`  
2. Execute `docker-build.sh` to build the image  
3. Run `docker-run.sh` on your SARS-CoV-2 genome of interest. As an example in this repository, we've included retrieval and application of this method to the the SARS-CoV-2 reference sequence NC_045512.2
4. The resulting files will include the gene and protein sequences identified

If you have any questions, please feel free to create a GitHub issue.

### Citation:  
This repository provides the code to accompany the method described in ["Semi-supervised identification of SARS-CoV-2 molecular targets"](https://www.biorxiv.org/content/10.1101/2021.05.03.440524v1) if you use this code, please cite us with the following:  

Semi-supervised identification of SARS-CoV-2 molecular targets  
Kristen L. Beck, Edward Seabolt, Akshay Agarwal, Gowri Nayar, Simone Bianco, Harsha Krishnareddy, Vandana Mukherjee, James H. Kaufman  
bioRxiv 2021.05.03.440524; doi: https://doi.org/10.1101/2021.05.03.440524  
