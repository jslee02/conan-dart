from conans import ConanFile
import os

class EigenConan(ConanFile):
    name = "eigen"
    version = "3.2"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = "eigen/*"
    url="https://github.com/jslee02/conan-dart/tree/master/eigen/3.2"

    def source(self):
        self.run('hg clone --insecure https://bitbucket.org/eigen/eigen -u 3.2.7')
        self.run('cd eigen')

    def package(self):
        self.copy("*", dst="include/Eigen", src="eigen/Eigen")
        self.copy("*", dst="include/unsupported", src="eigen/unsupported")

