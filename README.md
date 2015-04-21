cp3-llbb
========

*Please note:*
* The instructions are for the UCLouvain ingrid SLC6 cluster (to access SAMADhi)
* SCRAM_ARCH is slc6_amd64_gcc491
* You need the proper username and password to access SAMADhi :)

 ```
 cmsrel CMSSW_7_4_0_pre9
 cd CMSSW_7_4_0_pre9/src
 cmsenv
 git cms-init
 cd $CMSSW_BASE/src 
 git clone https://github.com/OlivierBondu/cp3-llbb.git UserCode/cp3-llbb
 ```

