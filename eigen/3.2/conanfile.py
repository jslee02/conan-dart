from conans import ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil
import urllib

class EigenConan(ConanFile):
    name = "eigen"
    version = "3.2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = "eigen/*"
    url="https://github.com/jslee02/conan-dart/tree/master/eigen/3.2"

    def source(self):
        self.run('hg clone https://bitbucket.org/eigen/eigen -u 3.2.7')
        self.run('cd eigen')

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        self.run('mkdir eigen/build')
        self.run('cd eigen/build && cmake .. %s %s' % (cmake.command_line, shared))

    def package(self):
        self.copy("*.h", dst="include/eigen", src="eigen-3.2/src/ccd")

    def package_info(self):
        self.cpp_info.libs = ["eigen"]

