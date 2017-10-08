#!/bin/bash

if grep BART ~/.bashrc
then
    echo found BART API key in .bashrc
else
    echo did not find BART API key in .bashrc
    echo adding...
    echo 'BART_API_KEY=MW9S-E7SL-26DU-VV8V' >> ~/.bashrc
fi 
