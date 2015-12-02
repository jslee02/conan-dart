from conans import ConanFile, CMake
from conans.tools import download, unzip
import os
import shutil

class LibccdConan(ConanFile):
    name = "libccd"
    version = "2.0"
    settings = "os", "compiler", "build_type", "arch"
    exports = "libccd/*"
    url="https://github.com/jslee02/conan-dart/tree/master/libccd/2.0"

    def source(self):
        zip_name = "libccd-2.0.zip"
        download("https://github.com/danfis/libccd/archive/v2.0.zip", zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        self.run('cd libccd-2.0 && cmake . %s' % cmake.command_line)
        self.run("cd libccd-2.0 && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include/ccd", src="libccd-2.0/src/ccd")
        self.copy("*.lib", dst="lib", src="libccd-2.0")
        self.copy("*.a", dst="lib", src="libccd-2.0")

    def package_info(self):
        self.cpp_info.libs = ["libccd"]
