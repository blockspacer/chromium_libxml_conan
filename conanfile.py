import glob
import os
from conans import ConanFile, CMake, tools
from conans.model.version import Version
from conans.errors import ConanInvalidConfiguration

from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment, RunEnvironment, python_requires
from conans.errors import ConanInvalidConfiguration, ConanException
from conans.tools import os_info
import os, re, stat, fnmatch, platform, glob, traceback, shutil
from functools import total_ordering

# if you using python less than 3 use from distutils import strtobool
from distutils.util import strtobool

conan_build_helper = python_requires("conan_build_helper/[~=0.0]@conan/stable")

# conan runs the methods in this order:
# config_options(),
# configure(),
# requirements(),
# package_id(),
# build_requirements(),
# build_id(),
# system_requirements(),
# source(),
# imports(),
# build(),
# package(),
# package_info()

class chromium_libxml_conan_project(conan_build_helper.CMakePackage):
    name = "chromium_libxml"

    # Indicates License type of the packaged library
    # TODO (!!!)
    # license = "MIT"

    version = "stable"
    commit = "b73d9be6d6d07a37371854a766eee67e683e3d59"

    # TODO (!!!)
    #url = "https://github.com/blockspacer/CXXCTP"

    description = "modified `libxml` library from chromium"
    topics = ('c++')

    options = {
      # "LIBXML2_WITH_AUTOMATA": [True, False],
      "LIBXML2_WITH_C14N": [True, False],
      "LIBXML2_WITH_CATALOG": [True, False],
      "LIBXML2_WITH_DEBUG": [True, False],
      "LIBXML2_WITH_DOCB": [True, False],
      # LIBXML2_WITH_EXPR
      "LIBXML2_WITH_FTP": [True, False],
      "LIBXML2_WITH_HTML": [True, False],
      "LIBXML2_WITH_HTTP": [True, False],
      "LIBXML2_WITH_ICONV": [True, False],
      "LIBXML2_WITH_ICU": [True, False],
      "LIBXML2_WITH_ISO8859X": [True, False],
      "LIBXML2_WITH_LEGACY": [True, False],
      "LIBXML2_WITH_LZMA": [True, False],
      "LIBXML2_WITH_MEM_DEBUG": [True, False],
      "LIBXML2_WITH_MODULES": [True, False],
      "LIBXML2_WITH_OUTPUT": [True, False],
      "LIBXML2_WITH_PATTERN": [True, False],
      "LIBXML2_WITH_PROGRAMS": [True, False],
      "LIBXML2_WITH_PUSH": [True, False],
      "LIBXML2_WITH_PYTHON": [True, False],
      "LIBXML2_WITH_READER": [True, False],
      "LIBXML2_WITH_REGEXPS": [True, False],
      "LIBXML2_WITH_RUN_DEBUG": [True, False],
      "LIBXML2_WITH_SAX1": [True, False],
      "LIBXML2_WITH_SCHEMAS": [True, False],
      "LIBXML2_WITH_SCHEMATRON": [True, False],
      "LIBXML2_WITH_TESTS": [True, False],
      "LIBXML2_WITH_THREADS": [True, False],
      "LIBXML2_WITH_THREAD_ALLOC": [True, False],
      "LIBXML2_WITH_TREE": [True, False],
      #"LIBXML2_WITH_TRIO": [True, False],
      #"LIBXML2_WITH_UNICODE": [True, False],
      "LIBXML2_WITH_VALID": [True, False],
      "LIBXML2_WITH_WRITER": [True, False],
      "LIBXML2_WITH_XINCLUDE": [True, False],
      "LIBXML2_WITH_XPATH": [True, False],
      "LIBXML2_WITH_XPTR": [True, False],
      "LIBXML2_WITH_ZLIB": [True, False],
      "enable_ubsan": [True, False],
      "enable_asan": [True, False],
      "enable_msan": [True, False],
      "enable_tsan": [True, False],
      "shared": [True, False],
      "debug": [True, False],
      "enable_sanitizers": [True, False],
      "enable_cobalt": [True, False],
      "use_system_zlib": [True, False]
    }

    default_options = (
      #"LIBXML2_WITH_AUTOMATA=False",
      "LIBXML2_WITH_C14N=False",
      "LIBXML2_WITH_CATALOG=False",
      "LIBXML2_WITH_DEBUG=False",
      "LIBXML2_WITH_DOCB=False",
      "LIBXML2_WITH_FTP=False",
      "LIBXML2_WITH_HTML=True",
      "LIBXML2_WITH_HTTP=False",
      "LIBXML2_WITH_ICONV=False",
      "LIBXML2_WITH_ICU=True",
      "LIBXML2_WITH_ISO8859X=False",
      "LIBXML2_WITH_LEGACY=False",
      "LIBXML2_WITH_LZMA=False",
      "LIBXML2_WITH_MEM_DEBUG=False",
      "LIBXML2_WITH_MODULES=False",
      "LIBXML2_WITH_OUTPUT=True",
      "LIBXML2_WITH_PATTERN=False",
      "LIBXML2_WITH_PROGRAMS=False",
      "LIBXML2_WITH_PUSH=True",
      "LIBXML2_WITH_PYTHON=False",
      "LIBXML2_WITH_READER=True",
      "LIBXML2_WITH_REGEXPS=False",
      "LIBXML2_WITH_RUN_DEBUG=False",
      "LIBXML2_WITH_SAX1=False",
      "LIBXML2_WITH_SCHEMAS=False",
      "LIBXML2_WITH_SCHEMATRON=False",
      "LIBXML2_WITH_TESTS=False",
      "LIBXML2_WITH_THREADS=True",
      "LIBXML2_WITH_THREAD_ALLOC=False",
      "LIBXML2_WITH_TREE=True",
      "LIBXML2_WITH_VALID=False",
      "LIBXML2_WITH_WRITER=True",
      "LIBXML2_WITH_XINCLUDE=False",
      "LIBXML2_WITH_XPATH=True",
      "LIBXML2_WITH_XPTR=False",
      "LIBXML2_WITH_ZLIB=True",
      "enable_ubsan=False",
      "enable_asan=False",
      "enable_msan=False",
      "enable_tsan=False",
      "shared=False",
      "debug=False",
      "enable_sanitizers=False",
      "enable_cobalt=False",
      "use_system_zlib=False"
      # build
      #"*:shared=False"
    )

    # Custom attributes for Bincrafters recipe conventions
    _source_subfolder = "."
    _build_subfolder = "."

    # NOTE: no cmake_find_package due to custom FindXXX.cmake
    generators = "cmake", "cmake_paths", "virtualenv"

    # Packages the license for the conanfile.py
    #exports = ["LICENSE.md"]

    # If the source code is going to be in the same repo as the Conan recipe,
    # there is no need to define a `source` method. The source folder can be
    # defined like this
    exports_sources = ("LICENSE", "*.md", "include/*", "src/*",
                       "cmake/*", "examples/*", "CMakeLists.txt", "tests/*", "benchmarks/*",
                       "scripts/*", "tools/*", "codegen/*", "assets/*",
                       "docs/*", "licenses/*", "patches/*", "resources/*",
                       "submodules/*", "thirdparty/*", "third-party/*",
                       "third_party/*", "base/*", "chromium/*")

    settings = "os", "compiler", "build_type", "arch"

    # sets cmake variables required to use clang 10 from conan
    def _is_compile_with_llvm_tools_enabled(self):
      return self._environ_option("COMPILE_WITH_LLVM_TOOLS", default = 'false')

    # installs clang 10 from conan
    def _is_llvm_tools_enabled(self):
      return self._environ_option("ENABLE_LLVM_TOOLS", default = 'false')

    #def source(self):
    #  url = "https://github.com/....."
    #  self.run("git clone %s ......." % url)

    def configure(self):
        lower_build_type = str(self.settings.build_type).lower()

        if lower_build_type != "release" and not self._is_llvm_tools_enabled():
            self.output.warn('enable llvm_tools for Debug builds')

        if self._is_compile_with_llvm_tools_enabled() and not self._is_llvm_tools_enabled():
            raise ConanInvalidConfiguration("llvm_tools must be enabled")

        if self.options.enable_ubsan \
           or self.options.enable_asan \
           or self.options.enable_msan \
           or self.options.enable_tsan:
            if not self._is_llvm_tools_enabled():
                raise ConanInvalidConfiguration("sanitizers require llvm_tools")

        if self.options.enable_ubsan:
            if self._is_tests_enabled():
              self.options["conan_gtest"].enable_ubsan = True
            self.options["chromium_icu"].enable_ubsan = True
            if not self.options.use_system_zlib:
              self.options["chromium_zlib"].enable_ubsan = True

        if self.options.enable_asan:
            if self._is_tests_enabled():
              self.options["conan_gtest"].enable_asan = True
            self.options["chromium_icu"].enable_asan = True
            if not self.options.use_system_zlib:
              self.options["chromium_zlib"].enable_asan = True

        if self.options.enable_msan:
            if self._is_tests_enabled():
              self.options["conan_gtest"].enable_msan = True
            self.options["chromium_icu"].enable_msan = True
            if not self.options.use_system_zlib:
              self.options["chromium_zlib"].enable_msan = True

        if self.options.enable_tsan:
            if self._is_tests_enabled():
              self.options["conan_gtest"].enable_tsan = True
            self.options["chromium_icu"].enable_tsan = True
            if not self.options.use_system_zlib:
              self.options["chromium_zlib"].enable_tsan = True

        if self.settings.os == "Emscripten":
           self.options.use_system_zlib = "True"

    def build_requirements(self):
        self.build_requires("cmake_platform_detection/master@conan/stable")
        self.build_requires("cmake_build_options/master@conan/stable")
        self.build_requires("cmake_helper_utils/master@conan/stable")

        if self._is_tests_enabled():
            self.build_requires("catch2/[>=2.1.0]@bincrafters/stable")
            self.build_requires("conan_gtest/stable@conan/stable")
            self.build_requires("FakeIt/[>=2.0.4]@gasuketsu/stable")

        if self.options.enable_tsan \
            or self.options.enable_msan \
            or self.options.enable_asan \
            or self.options.enable_ubsan:
          self.build_requires("cmake_sanitizers/master@conan/stable")

        # provides clang-tidy, clang-format, IWYU, scan-build, etc.
        if self._is_llvm_tools_enabled():
          self.build_requires("llvm_tools/master@conan/stable")

    def requirements(self):
        if self.options.enable_cobalt:
            self.requires("cobalt_starboard_headers_only/master@conan/stable")

        self.requires("chromium_build_util/master@conan/stable")
        self.requires("chromium_icu/master@conan/stable")

        if not self.options.use_system_zlib:
          self.requires("chromium_zlib/master@conan/stable")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.parallel = True
        cmake.verbose = True

        if self.options.shared:
            cmake.definitions["BUILD_SHARED_LIBS"] = "ON"

        def add_cmake_option(var_name, value):
            value_str = "{}".format(value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value

        for option, value in self.options.items():
             self.add_cmake_option(cmake, str(option).upper(), value)

        add_cmake_option("ENABLE_COBALT", self.options.enable_cobalt)

        add_cmake_option("ENABLE_SANITIZERS", self.options.enable_sanitizers)

        add_cmake_option("ENABLE_TESTS", self._is_tests_enabled())

        add_cmake_option("USE_SYSTEM_ZLIB", self.options.use_system_zlib)

        add_cmake_option("LIBXML2_WITH_THREADS", self.options.LIBXML2_WITH_THREADS)

        cmake.definitions["ENABLE_UBSAN"] = 'ON'
        if not self.options.enable_ubsan:
            cmake.definitions["ENABLE_UBSAN"] = 'OFF'

        cmake.definitions["ENABLE_ASAN"] = 'ON'
        if not self.options.enable_asan:
            cmake.definitions["ENABLE_ASAN"] = 'OFF'

        cmake.definitions["ENABLE_MSAN"] = 'ON'
        if not self.options.enable_msan:
            cmake.definitions["ENABLE_MSAN"] = 'OFF'

        cmake.definitions["ENABLE_TSAN"] = 'ON'
        if not self.options.enable_tsan:
            cmake.definitions["ENABLE_TSAN"] = 'OFF'

        self.add_cmake_option(cmake, "COMPILE_WITH_LLVM_TOOLS", self._is_compile_with_llvm_tools_enabled())

        cmake.configure(build_folder=self._build_subfolder)

        return cmake

    def package(self):
        with tools.vcvars(self.settings, only_diff=False): # https://github.com/conan-io/conan/issues/6577
          self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
          #self.copy("*", dst="third_party", src="{}/include/chromium/third_party/libxml/src/include/libxml".format(self._source_subfolder))
          cmake = self._configure_cmake()
          cmake.install()

    def build(self):
        with tools.vcvars(self.settings, only_diff=False): # https://github.com/conan-io/conan/issues/6577
          cmake = self._configure_cmake()
          if self.settings.compiler == 'gcc':
              cmake.definitions["CMAKE_C_COMPILER"] = "gcc-{}".format(
                  self.settings.compiler.version)
              cmake.definitions["CMAKE_CXX_COMPILER"] = "g++-{}".format(
                  self.settings.compiler.version)

          #cmake.definitions["CMAKE_TOOLCHAIN_FILE"] = 'conan_paths.cmake'

          # The CMakeLists.txt file must be in `source_folder`
          cmake.configure(source_folder=".")

          cpu_count = tools.cpu_count()
          self.output.info('Detected %s CPUs' % (cpu_count))

          # -j flag for parallel builds
          cmake.build(args=["--", "-j%s" % cpu_count])

          if self._is_tests_enabled():
            self.output.info('Running tests')
            self.run('ctest --parallel %s' % (cpu_count))
            # TODO: use cmake.test()

    # Importing files copies files from the local store to your project.
    def imports(self):
        dest = os.getenv("CONAN_IMPORT_PATH", "bin")
        self.output.info("CONAN_IMPORT_PATH is ${CONAN_IMPORT_PATH}")
        self.copy("license*", dst=dest, ignore_case=True)
        self.copy("*.dll", dst=dest, src="bin")
        self.copy("*.so*", dst=dest, src="bin")
        self.copy("*.pdb", dst=dest, src="lib")
        self.copy("*.dylib*", dst=dest, src="lib")
        self.copy("*.lib*", dst=dest, src="lib")
        self.copy("*.a*", dst=dest, src="lib")

    # package_info() method specifies the list of
    # the necessary libraries, defines and flags
    # for different build configurations for the consumers of the package.
    # This is necessary as there is no possible way to extract this information
    # from the CMake install automatically.
    # For instance, you need to specify the lib directories, etc.
    def package_info(self):
        #self.cpp_info.libs = ["chromium_libxml"]

        self.cpp_info.includedirs = ["include"]

        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.bindirs = ["bin"]
        self.env_info.LD_LIBRARY_PATH.append(
            os.path.join(self.package_folder, "lib"))
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))
        for libpath in self.deps_cpp_info.lib_paths:
            self.env_info.LD_LIBRARY_PATH.append(libpath)

        #self.cpp_info.includedirs.append(os.getcwd())
        #self.cpp_info.includedirs.append(
        #  os.path.join("base", "third_party", "libxml"))
        #self.cpp_info.includedirs.append(
        #  os.path.join("base", "third_party", "libxml", "compat"))

        #if self.settings.os == "Linux":
        #  self.cpp_info.defines.append('HAVE_CONFIG_H=1')

        # in linux we need to link also with these libs
        #if self.settings.os == "Linux":
        #    self.cpp_info.libs.extend(["pthread", "dl", "rt"])

        #self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.defines.append('PDFLIB_DLL')
