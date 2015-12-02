from conans import ConanFile, CMake

class LibccdConan(ConanFile):
    name = "libccd"
    version = "2.0"
    settings = "os", "compiler", "build_type", "arch"
    exports = "libccd/*"

    def build(self):
        cmake = CMake(self.settings)
        self.run('cd libccd && cmake . %s' % cmake.command_line)
        self.run("cd libccd && cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="libccd")
        self.copy("*.lib", dst="lib", src="libccd")
        self.copy("*.a", dst="lib", src="libccd")

    def package_info(self):
        self.cpp_info.libs = ["libccd"]
