#!/bin/bash

# Check where you are: local pycharm installation, or ingrid
isIngrid=0
isPycharm=0
if [ -n "${CMSSW_BASE+x}" ]
then
    isIngrid=1
fi

if [[ ${PWD} == *"Pycharm"* ]]
then
    isPycharm=1
fi

# Dedicated ingrid setup
if [ ${isIngrid} -eq 1 ]
then
    # Look out for conflicts between git and cmssw
    if [ ! -f ${CMSSW_BASE}/src/.git/HEAD ];
    then
        echo "You seem to be on Ingrid and CMSSW area appears not to be set up correctly. Check README carefully."
        echo
        return 1
    fi
    cd ${CMSSW_BASE}/src/cp3_llbb/ExTreeMaker
    # configure the origin repository
    GITHUBUSERNAME=`git config user.github`
    GITHUBUSERREMOTE=`git remote -v | grep ${GITHUBUSERNAME} | awk '{print $2}' | head -n 1 | cut -d / -f 5`
    git remote add origin git@github.com:${GITHUBUSERNAME}/${GITHUBUSERREMOTE}
fi

# Dedicated local setup
if [ ${isPycharm} -eq 1 ]
then
    # upstream is not configured by default on pycharm
    git remote add upstream https://github.com/cp3-llbb/ExTreeMaker.git
fi

# Setup common to both ingrid and local: add the remaining forks
git remote add delaere https://github.com/delaere/zbb_louvaini.git
git remote add BrieucF https://github.com/BrieucF/zbb_louvain.git
git remote add OlivierBondu https://github.com/OlivierBondu/ExTreeMaker.git
git remote add swertz https://github.com/swertz/ExTreeMaker.git
git remote add vidalm https://github.com/vidalm/zbb_louvain.git
git remote add camillebeluffi https://github.com/camillebeluffi/zbb_louvain.git
git remote add blinkseb https://github.com/blinkseb/ExTreeMaker.git
# have not yet forked, but are expected to:
git remote add acaudron https://github.com/acaudron/ExTreeMaker.git
git remote add AlexandreMertens https://github.com/AlexandreMertens/ExTreeMaker.git
