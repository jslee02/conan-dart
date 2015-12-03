# brew update > /dev/null

# PACKAGES='
# cmake
# '

# brew install $PACKAGES | grep -v '%$'

# Download conan
wget https://s3-eu-west-1.amazonaws.com/conanio-production/downloads/conan-macos-64_0_4_0.pkg -O conan.pkg
sudo installer -pkg conan.pkg -target /
rm conan.pkg

# Adjust config and settings
conan user jslee02
echo -e "\ncompiler=gcc" >> ~/.conan/conan.conf
echo -e "\ncompiler.version=$(gcc -dumpversion)" >> ~/.conan/conan.conf

