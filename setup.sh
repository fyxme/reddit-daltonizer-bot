#! /usr/bin/env bash

echo "Downloading required libraries"

pip install praw
pip install Pillow
pip install numpy
pip install imgurpython

echo ">> Update credentials-example.py with your credentials"
echo ">> Rename credentials-example.py to credentials.py"
echo ">> Then run get_imgur_token.py to get imgur access and refresh token"