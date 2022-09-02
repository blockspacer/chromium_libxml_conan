from conans import ConanFile, CMake, tools
import os

from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment, RunEnvironment, python_requires
from conans.errors import ConanInvalidConfiguration, ConanException
from conans.tools import os_info
import os, re, stat, fnmatch, platform, glob, traceback, shutil
from functools import total_ordering

# if you using python less than 3 use from distutils import strtobool
from distutils.util import strtobool

conan_build_helper = python_requires("conan_build_helper/[~=0.0]@conan/stable")

class TestPackageConan(conan_build_helper.CMakePackage):
    name = "chromium_libxml_test_package"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    # sets cmake variables required to use clang 10 from conan
    #def _is_compile_with_llvm_tools_enabled(self):
    #  return self._environ_option("COMPILE_WITH_LLVM_TOOLS", default = 'false')

    # installs clang 10 from conan
    def _is_llvm_tools_enabled(self):
      return self._environ_option("ENABLE_LLVM_TOOLS", default = 'false')

    def build_requirements(self):
        self.build_requires("cmake_platform_detection/master@conan/stable")
        self.build_requires("cmake_build_options/master@conan/stable")
        self.build_requires("cmake_helper_utils/master@conan/stable")

        # TODO: separate is_lsan
        if self.options['chromium_libxml'].enable_tsan \
            or self.options['chromium_libxml'].enable_msan \
            or self.options['chromium_libxml'].enable_asan \
            or self.options['chromium_libxml'].enable_ubsan:
          self.build_requires("cmake_sanitizers/master@conan/stable")

        # provides clang-tidy, clang-format, IWYU, scan-build, etc.
        if self._is_llvm_tools_enabled():
          self.build_requires("llvm_tools/master@conan/stable")

    def build(self):
        cmake = CMake(self)

        for option, value in self.options['chromium_libxml'].items():
            self.add_cmake_option(cmake, str(option).upper(), value)

        #cmake.definitions['LIBXML2_WITH_THREADS'] = self.options['chromium_libxml'].LIBXML2_WITH_THREADS

        #cmake.definitions['ENABLE_UBSAN'] = self.options['chromium_libxml'].enable_ubsan
        #cmake.definitions['ENABLE_ASAN'] = self.options['chromium_libxml'].enable_asan
        #cmake.definitions['ENABLE_MSAN'] = self.options['chromium_libxml'].enable_msan
        #cmake.definitions['ENABLE_TSAN'] = self.options['chromium_libxml'].enable_tsan

        #self.add_cmake_option(cmake, "COMPILE_WITH_LLVM_TOOLS", self._is_compile_with_llvm_tools_enabled())

        cmake.configure()
        cmake.build()

    def test(self):
      with tools.environment_append(RunEnvironment(self).vars):
          bin_path = os.path.join(self.build_folder, "chromium_libxml_test_package")
          arg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "books.xml"))
          bin_arg_path = "%s %s" % (bin_path, arg_path)
          if self.settings.os == "Windows":
              self.run(bin_arg_path)
          elif self.settings.os == "Macos":
              self.run("DYLD_LIBRARY_PATH=%s %s" % (os.environ.get('DYLD_LIBRARY_PATH', ''), bin_arg_path))
          else:
              self.run("LD_LIBRARY_PATH=%s %s" % (os.environ.get('LD_LIBRARY_PATH', ''), bin_arg_path))
