from conans.model.conan_file import ConanFile
from conans import CMake
import os

class DefaultNameConan(ConanFile):
    name = "DefaultName"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "Boost/1.59.0@jslee02/stable"

    def build(self):
        cmake = CMake(self.settings)
        self.run("cmake . %s" % cmake.command_line)
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")
        
    def test(self):
        self.run("cd bin && .%smytest" % os.sep)

