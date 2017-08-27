echo "Downloading required libraries"

pip install Pillow
pip install numpy scipy matplotlib ipython jupyter pandas sympy nose
pip install imgurpython

echo "Downloading daltonizer"

if [[ -ne "daltonize"]]; then
    git clone https://github.com/joergdietrich/daltonize.git
fi

echo "Setting up required folders"

if [[ -ne "img" ]]; then
    mkdir img
fi