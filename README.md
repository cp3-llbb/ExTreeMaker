ExTreeMaker
===========

*Please note:*
* The instructions are for the UCLouvain ingrid SLC6 cluster (to access SAMADhi)
* You need the proper username and password to access SAMADhi :) If you don't know what this is about, ask around
* The `git cms-init` takes a while to run and is currently useless... But it is still needed if ever some day we need to checkout other CMSSW packages (which seems likely IMHO)
* The current state of the art mini-AOD documentation can be found [here](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookMiniAOD2015)
* We have setup a 'fake' python in the `bin` directory that runs `cmsenv` and set the correct `PYTHONPATH` before executing python itself, this is currently useful to setup the debugger

# First time setup

 ```
 source /nfs/soft/grid/ui_sl6/setup/grid-env.sh
 source /cvmfs/cms.cern.ch/cmsset_default.sh
 export SCRAM_ARCH=slc6_amd64_gcc491
 cmsrel CMSSW_7_4_1
 cd CMSSW_7_4_1/src
 cmsenv
 git cms-init
 cd ${CMSSW_BASE}/src 
 git clone -o upstream https://github.com/cp3-llbb/ExTreeMaker.git cp3-llbb/ExTreeMaker
 cd cp3-llbb/ExTreeMaker
 git checkout dev_goingMiniAOD
 source setup.sh
 scram b -j 4
 ```
# Test run (command line)

 ```
 cd ${CMSSW_BASE}/src/cp3-llbb/ExTreeMaker/python
 ./../bin/python PatAnalysis/ControlPlots.py -c incConfig --all -i /home/fynu/obondu/storage/MINIAODSIM/RelValTTbar_13_PU25ns_MCRUN2_74_V9_gensim71X-v1.root --nEvents 100
 ```
 
# When willing to commit things
  * Remember to *branch before committing anything*: ```git checkout -b my-new-branch```
  * The ```setup.sh``` script took care of adding ```origin``` as your own repo, so to push just do the usual ```git push origin my-new-branch```

