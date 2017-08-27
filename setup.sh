#! /usr/bin/env bash

echo "Downloading required libraries"

pip install Pillow
pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install imgurpython

echo "Setting up required folders"

if [[ ! -d "img" ]]; then
    mkdir img
fi

echo ">> Update credentials-example.py with your credentials"
echo ">> Rename credentials-example.py to credentials.py"
echo ">> Then run get_imgur_token.py to get imgur access and refresh token"