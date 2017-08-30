#! /usr/bin/env bash

echo "Downloading required libraries"

pip install praw
pip install Pillow
pip install numpy
pip install imgurpython

cp credentials-example.py credentials.py

echo ">> Update credentials.py with your credentials"
echo ">> Then run get_imgur_token.py to get imgur access and refresh token"
