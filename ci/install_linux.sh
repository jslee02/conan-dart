# Install gcc-multilib (fixed some errors)
sudo apt-get -qq update
sudo apt-get -qq --yes install gcc-multilib

# Install CMake 3
wget https://s3.amazonaws.com/biibinaries/thirdparty/cmake-3.0.2-Linux-64.tar.gz
tar -xzf cmake-3.0.2-Linux-64.tar.gz
sudo cp -fR cmake-3.0.2-Linux-64/* /usr
rm -rf cmake-3.0.2-Linux-64
rm cmake-3.0.2-Linux-64.tar.gz

# Download conan
wget https://s3-eu-west-1.amazonaws.com/conanio-production/downloads/conan-ubuntu-64_0_4_0.deb -O conan.deb
sudo dpkg -i conan.deb
rm conan.deb

# Adjust config and settings
conan user jslee02
echo -e "\ncompiler=gcc" >> ~/.conan/conan.conf
echo -e "\ncompiler.version=$(gcc -dumpversion)" >> ~/.conan/conan.conf

