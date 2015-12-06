from conans import ConanFile, CMake
from conans.tools import download, unzip
import os

class FclConan(ConanFile):
    name = "fcl"
    version = "0.3"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    requires = "libccd/2.0@jslee02/stable", "Boost/1.59.0@lasote/stable"
    exports = "fcl/*"
    url="https://github.com/jslee02/conan-dart/tree/master/fcl/0.3"

    def source(self):
        zip_name = "fcl-0.3.2.zip"
        download("https://github.com/flexible-collision-library/fcl/archive/0.3.2.zip", zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        self.run("cd fcl-0.3.2 && cmake . %s %s" % (cmake.command_line, shared))
        self.run("cd fcl-0.3.2 && cmake --build . %s" % cmake.build_config)

    def package(self):
        # include
        self.copy("*.h", dst="include", src="fcl-0.3.2/include")
        self.copy("*.hxx", dst="include", src="fcl-0.3.2/include")
        
        # lib
        self.copy("*.dll", dst="bin", src="fcl-0.3.2/lib")
        self.copy("*.lib", dst="lib", src="fcl-0.3.2/lib")
        self.copy("*.a", dst="lib", src="fcl-0.3.2/lib")
        self.copy("*.so*", dst="lib", src="fcl-0.3.2/lib")
        self.copy("*.dylib*", dst="lib", src="fcl-0.3.2/lib")

    def package_info(self):
        self.cpp_info.libs = ["fcl"]

