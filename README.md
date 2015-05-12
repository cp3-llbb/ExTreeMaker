ExTreeMaker
===========

*Please note:*
* The instructions are for the UCLouvain ingrid SLC6 cluster (to access SAMADhi)
* You need the proper username and password to access SAMADhi :)
* The `git cms-init` takes a while to run and is currently useless... But it is still needed if ever some day we need to checkout other CMSSW packages (which seems likely IMHO)

# First time setup

 ```
 source /nfs/soft/grid/ui_sl6/setup/grid-env.sh
 source /cvmfs/cms.cern.ch/cmsset_default.sh
 export SCRAM_ARCH=slc6_amd64_gcc491
 cmsrel CMSSW_7_4_0_pre9
 cd CMSSW_7_4_0_pre9/src
 cmsenv
 git cms-init
 cd $CMSSW_BASE/src 
 git clone https://github.com/cp3-llbb/ExTreeMaker.git UserCode/cp3-llbb
 cd UserCode/cp3-llbb
 git checkout dev_goingMiniAOD
 scram b -j 4
 ```

