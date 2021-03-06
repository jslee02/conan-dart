from conans import ConanFile, CMake
from conans.tools import download, unzip
import os

class ConsoleBridgeConan(ConanFile):
    name = "console_bridge"
    version = "0.2.7"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    exports = "console_bridge/*"
    url="https://github.com/jslee02/conan-dart/tree/master/console_bridge/0.2.7"

    def system_requirements(self):
        self.global_system_requirements=True
        if self.settings.os == "Linux":
            self.run("sudo apt-get install libboost-all-dev || true ")

    def requirements(self):
        if self.settings.os == "Windows":
             self.requires("Boost/1.59.0@lasote/stable")

    def source(self):
        zip_name = "console_bridge-0.2.7.zip"
        download("https://github.com/ros/console_bridge/archive/0.2.7.zip", zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        self.run("cd console_bridge-0.2.7 && cmake . %s %s" % (cmake.command_line, shared))
        self.run("cd console_bridge-0.2.7 && cmake --build . %s" % cmake.build_config)

    def package(self):
        # include
        self.copy("*.h", dst="include", src="console_bridge-0.2.7/include")

        # lib
        self.copy("*.dll", dst="bin", src="fconsole_bridge-0.2.7")
        self.copy("*.lib", dst="lib", src="console_bridge-0.2.7")
        self.copy("*.a", dst="lib", src="console_bridge-0.2.7")
        self.copy("*.so*", dst="lib", src="console_bridge-0.2.7")
        self.copy("*.dylib*", dst="lib", src="console_bridge-0.2.7")

    def package_info(self):
        self.cpp_info.libs = ["console_bridge"]

