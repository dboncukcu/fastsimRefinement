#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh
export PYTHONPATH=./site-packages:$PYTHONPATH

export outputDirName="test100_log10_recJetpt"

echo $outputDirName

mkdir /eos/user/d/dboncukc/fastsim/$outputDirName

cp train.py /eos/user/d/dboncukc/fastsim/$outputDirName/train.py
cp my_modules.py /eos/user/d/dboncukc/fastsim/$outputDirName/my_modules.py

python train.py
