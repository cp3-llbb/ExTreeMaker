#!/bin/bash

if [ ! -f ${CMSSW_BASE}/src/.git/HEAD ];
then
  echo "CMSSW area appears not to be set up correctly. Check README carefully."
  echo
  return 1
fi

cd ${CMSSW_BASE}/src/cp3-llbb/ExTreeMaker

git remote add delaere https://github.com/delaere/zbb_louvaini.git
git remote add BrieucF https://github.com/BrieucF/zbb_louvain.git
git remote add OlivierBondu https://github.com/OlivierBondu/ExTreeMaker.git
git remote add swertz https://github.com/swertz/ExTreeMaker.git
git remote add vidalm https://github.com/vidalm/zbb_louvain.git
git remote add camillebeluffi https://github.com/camillebeluffi/zbb_louvain.git
# have not yet forked, but are expected to:
git remote add acaudron https://github.com/acaudron/ExTreeMaker.git
git remote add AlexandreMertens https://github.com/AlexandreMertens/ExTreeMaker.git
git remote add blinkseb https://github.com/blinkseb/ExTreeMaker.git

GITHUBUSERNAME=`git config user.github`
GITHUBUSERREMOTE=`git remote -v | grep ${GITHUBUSERNAME} | awk '{print $2}' | head -n 1 | cut -d : -f 2`
git remote add origin git@github.com:${GITHUBUSERREMOTE}

#cd ${CMSSW_BASE}/src
