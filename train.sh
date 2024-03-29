#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
#source /afs/cern.ch/user/d/dboncukc/.bash_profile
export PYTHONPATH=./site-packages:$PYTHONPATH

export outputDirName="epoch1000_tanh800_logit"

export trainingId="tanh800_logit"

export isTest="False"

echo $outputDirName
mkdir /eos/user/d/dboncukc/fastsim/$outputDirName
mkdir /eos/user/d/dboncukc/fastsim/$outputDirName/codes
cp *.py /eos/user/d/dboncukc/fastsim/$outputDirName/codes/

python trainRegression_Jet.py
