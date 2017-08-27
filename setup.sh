#! /usr/bin/env bash

echo "Downloading required libraries"

pip install Pillow
pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install imgurpython

echo "Setting up required folders"

if [[ ! -d "img" ]]; then
    mkdir img
fi

echo ">> Please update credentials.py with your credentials"
echo ">> Then run get_imgur_token.py to get imgur access and refresh token"