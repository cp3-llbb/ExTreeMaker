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
 cmsrel CMSSW_7_4_4
 cd CMSSW_7_4_4/src
 cmsenv
 git cms-init
 cd ${CMSSW_BASE}/src 
 git clone -o upstream https://github.com/cp3-llbb/ExTreeMaker.git cp3_llbb/ExTreeMaker
 cd cp3_llbb/ExTreeMaker
 git checkout dev_goingMiniAOD
 source setup.sh
 scram b -j 4
 ```
# Test run (command line)

 ```
 cd ${CMSSW_BASE}/src/cp3_llbb/ExTreeMaker/python
 ./../bin/python ./../scripts/runFramework.py -c TestConfiguration -i /home/fynu/obondu/storage/MINIAODSIM/RelValTTbar_13_PU25ns_MCRUN2_74_V9_gensim71X-v1.root --nEvents 100
 ```
 
# When willing to commit things
  * Remember to *branch before committing anything*: ```git checkout -b my-new-branch```
  * The ```setup.sh``` script took care of adding ```origin``` as your own repo, so to push just do the usual ```git push origin my-new-branch```


# PyCharm configuration

You need the professional edition of PyCharm. You can request a licence using your UCL mail address here: https://www.jetbrains.com/student

## Project setup

Launch PyCharm. On the welcome screen, choose 'Checkout from Version Control' and select Github. Follow the instructions, and checkout **your** fork of ``ExTreeMaker``.

## Deployment

This steps indicate to PyCharm how-to copy your local files to ingrid. Go to File > Settings > Build, Execution, Deployment
and then click on Deployment. Click on the green plus button to add a new deployment configuration. Name it ``ingrid`` and choose ``SFTP`` as type.

On the Connection tab, set:

* SFTP host: ingrid-ui1.cism.ucl.ac.be
* Port: 22
* Username: your ingrid username
* Auth type: if you have an SSH key, you can choose 'Key pair' here, or password otherwise
* If you chose 'Key pair', fill the 'Private key file' field with the absolute path of your private SSH key, and the 'passphrase' field. If you chose password, fill the password field.

On the Mappings tab, set the 'Deployment path' to the absolute path of the ``ExTreeMaker`` directory inside the CMSSW release. For example, it can be ``/home/fynu/sbrochet/scratch/Framework/CMSSW_7_4_4/src/cp3_llbb/ExTreeMaker``.

Now click on the 'Add another mapping'. For the local path, set the absolute path of the ``ExTreeMaker`` directory. For the deployment path, use the same path as above, but replace ``src`` by ``python`` (for example, ``/home/fynu/sbrochet/scratch/Framework/CMSSW_7_4_4/python/cp3_llbb/ExTreeMaker``). Set the web path to '/'.

Click on 'Apply' to save your changes.

Now, on the menu on the left, click on 'Options' under 'Deployment'. Set the option 'Upload changed files automatically to the default server' to 'Always'. Click on 'Apply' to save your changes, and 'OK' to close the dialog.

Now you need to do the first upload of the project remotely. On the 'Project' window, right-click on the 'ExTreeMaker' project (top left of the screen), and select 'Upload to ingrid'.

## Remote python interpreter

We need to configure PyCharm to use python from CMSSW instead of system-wide python. Go to File > Settings > Project: ExTreeMaker and click on 'Project Interpreter'. Click on the little wheel (top right of the screen), and choose 'Add remote'.

Select 'Deployment configuration', and choose 'ingrid' (or whatever name you used for your deployment configuration). For the 'Python interpreter path', select the ``python`` file located in the ``bin`` folder of the framework. It'll look like ``/home/fynu/sbrochet/scratch/Framework/CMSSW_7_4_4/src/cp3_llbb/ExTreeMaker/bin/python``. Click on OK to validate. Make sure that the new python interpreter is selected.

## Run configuration

Final step is to tell PyCharm how-to execute the framework on ingrid. Go to Run > Edit configurations... Click on the green plus button and choose 'Python'. Name your new run configuration as you want (ingrid for example...). In the configuration tab, set:

* Script: click on the '...' button to browse. Select the file 'scripts/runFramework.py'
* Script parameters: ``-c TestConfiguration -i /home/fynu/obondu/storage/MINIAODSIM/RelValTTbar_13_PU25ns_MCRUN2_74_V9_gensim71X-v1.root --nEvents 100`` will allow you to get started
* Python interpreter: choose here your remote interpreter (something like ``sftp://...``)
* Working directory: Browse and choose the 'python' folder

That's all. Click on Apply and then OK. You can now run remotely on ingrid. To test, click on the green arrow (top right of the screen). Be sure first to select the right run configuration on the drop-down list on the left of the run button. You should see the output inside the Run window.

## Git setup

Unfortunately there is currently no easy user-friendly way to have several git remotes in pycharm, so we have to setup and update with the upstream manually:
 * As long as your pycharm project is in a directory containing the string "Pycharm" (the installation default being "PycharmProjects"), just run `source setup.sh` in the pycharm 'Terminal' at the bottom of the screen (should already point you to the correct directory)
