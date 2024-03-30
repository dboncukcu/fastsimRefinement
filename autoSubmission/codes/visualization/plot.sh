#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_101cuda/x86_64-centos7-gcc8-opt/setup.sh

in_path="/eos/user/d/dboncukc/fastsim/epoch100_loge/"
training_id="loge"

export visulazationDir="${in_path},${training_id}"

echo "plotLearningCurves"
python plotLearningCurves.py

echo "plotWeights"
python plotWeights.py


echo "plotPareto"
python plotPareto.py

echo "plotRegression1D"
python plotRegression1D.py

echo "plotRegressionCorrelationFactors"
python plotRegressionCorrelationFactors.py

echo "All Done"
