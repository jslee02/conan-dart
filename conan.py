#!/usr/bin/env python
import sys
sys.path.append('C:\projects\conan-dart\conan') # Absolute path of the cloned repository folder

from conans.conan import main
main(sys.argv[1:])

