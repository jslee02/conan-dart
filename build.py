import os
import platform
import sys

default_client_conf_osx_10_11 = '''
[storage]
# This is the default path, but you can write your own
path: ~/.conan/data

[remotes]
conan.io: https://server.conan.io
local: http://localhost:9300

[settings_defaults]
arch=x86_64
build_type=Release
compiler=apple-clang
compiler.version=7.0
os=Macos
'''

ID = 'jslee02'
CHANNEL = 'stable'

class BuildPackage(object):
    def __init__(self, name, version, id = ID, channel = CHANNEL):
        self._name = name
        self._version = version
        self._id = id
        self._channel = channel

    def overwrite_default_config_file(self):
        conan_config_file = os.path.expanduser("~/.conan/conan.conf")
        config_file = open(conan_config_file, 'w')
        config_file.write(default_client_conf_osx_10_11)
        config_file.close()

    def get_package_dir(self, name, version):
        base_path = os.path.dirname(os.path.abspath(__file__))
        package_version_path = '%s/%s' % (self._name, self._version)
        path = os.path.join(base_path, package_version_path)
        result = os.path.isdir(path)
        result = result & os.path.exists(path)
        if not result:
            exit("Failed to find package at: %s" % path)
        return path

    def conan_export(self):
        # check if the path exists
        path = self.get_package_dir(self._name, self._version)
        os.system('cd %s && conan export %s/%s' % (path, self._id, self._channel))

    def test(self, settings):
        path = self.get_package_dir(self._name, self._version)
        argv =  " ".join(sys.argv[1:])
        command = "cd %s && conan test %s %s --build=missing" % (path, settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t %s" % command)

    def test_windows(self, compiler_version):
        # Check Visual Studio version
        compiler = '-s compiler="Visual Studio" -s compiler.version=%d ' % compiler_version

        # Static x86
        self.test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o libccd:shared=False')
        self.test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o libccd:shared=False')
        self.test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o libccd:shared=False')
        self.test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o libccd:shared=False')

        # Static x86_64
        self.test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o libccd:shared=False')
        self.test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o libccd:shared=False')
        self.test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o libccd:shared=False')
        self.test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o libccd:shared=False')

        # Shared x86
        self.test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o libccd:shared=True')
        self.test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o libccd:shared=True')
        self.test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o libccd:shared=True')
        self.test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o libccd:shared=True')

        # Shared x86_64
        self.test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o libccd:shared=True')
        self.test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o libccd:shared=True')
        self.test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o libccd:shared=True')
        self.test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o libccd:shared=True')

    def run(self):
        self.conan_export()

        # Workaround: CONAN doesn't allow to run any command when invalid compiler is detected and saved to 'conan.conf' file.
        # Travis-CI's osx 10.11 image contains gcc 4.2.1, which is invalid compiler to CONAN. So we overwrite 'conan.conf' to
        # the version of that gcc is removed. This might not a smart way but at least it works for now...
        if platform.system() == "Darwin":
            self.overwrite_default_config_file()

        if platform.system() == "Windows":
            self.test_windows(12)
            self.test_windows(14)

        elif platform.system() == "Darwin":  # This is OS X. Darwin forms the core set of components upon which Mac OS X and iOS are based.
            compiler = '-s compiler=apple-clang -s compiler.version=7.0 '

            # Static x86_64
            self.test(compiler + '-s arch=x86_64 -s build_type=Debug -o libccd:shared=False')
            self.test(compiler + '-s arch=x86_64 -s build_type=Release -o libccd:shared=False')

            # Shared x86_64
            self.test(compiler + '-s arch=x86_64 -s build_type=Debug -o libccd:shared=True')
            self.test(compiler + '-s arch=x86_64 -s build_type=Release -o libccd:shared=True')

        else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)
            if os.getenv("CXX") == "clang++":
                compiler = '-s compiler=clang -s compiler.version=3.4 '
            else:
                compiler = '-s compiler=gcc '

            # Static x86_64
            self.test(compiler + '-s arch=x86_64 -s build_type=Debug -o libccd:shared=False')
            self.test(compiler + '-s arch=x86_64 -s build_type=Release -o libccd:shared=False')

            # Shared x86_64
            self.test(compiler + '-s arch=x86_64 -s build_type=Debug -o libccd:shared=True')
            self.test(compiler + '-s arch=x86_64 -s build_type=Release -o libccd:shared=True')

if __name__ == "__main__":
    BuildPackage('eigen', 3.2).run()
    BuildPackage('fcl', 0.3).run()  # Disabled until Boost build issue is fixed
    BuildPackage('libccd', 2.0).run()

