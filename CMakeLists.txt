# see https://github.com/chromium/chromium/blob/9db0b5162b8648833c3a6b1af044cebd9d7d3855/base/BUILD.gn

cmake_minimum_required(VERSION 3.4)

# project() must be before checks, see https://stackoverflow.com/a/26437667/10904212
set(PROJECT_NAME "chromium_libxml")
set(PROJECT_VERSION 2.9.10)
project(${PROJECT_NAME}
  VERSION ${PROJECT_VERSION}
  LANGUAGES CXX C)

include(CheckCSourceCompiles)
include(CheckFunctionExists)
include(CheckIncludeFiles)
include(CheckLibraryExists)
include(CheckStructHasMember)
include(CheckSymbolExists)
include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

set(LIBXML_MAJOR_VERSION 2)
set(LIBXML_MINOR_VERSION 9)
set(LIBXML_MICRO_VERSION 10)

set(VERSION "${LIBXML_MAJOR_VERSION}.${LIBXML_MINOR_VERSION}.${LIBXML_MICRO_VERSION}")
set(LIBXML_VERSION ${LIBXML_MAJOR_VERSION}0${LIBXML_MINOR_VERSION}0${LIBXML_MICRO_VERSION})
set(LIBXML_VERSION_STRING "${LIBXML_VERSION}")
set(LIBXML_VERSION_EXTRA "")
set(LIBXML_VERSION_NUMBER ${LIBXML_VERSION})

option(BUILD_SHARED_LIBS "Build shared libraries" OFF)
set(LIBXML2_WITH_AUTOMATA OFF)
option(LIBXML2_WITH_C14N "Add the Canonicalization support" OFF)
option(LIBXML2_WITH_CATALOG "Add the Catalog support" OFF)
option(LIBXML2_WITH_DEBUG "Add the debugging module" OFF)
option(LIBXML2_WITH_DOCB "Add Docbook SGML support" OFF)
set(LIBXML2_WITH_EXPR ON)
option(LIBXML2_WITH_FTP "Add the FTP support" OFF)
option(LIBXML2_WITH_HTML "Add the HTML support" ON)
option(LIBXML2_WITH_HTTP "Add the HTTP support" OFF)
option(LIBXML2_WITH_ICONV "Add ICONV support" OFF)
option(LIBXML2_WITH_ICU "Add ICU support" ON)
option(LIBXML2_WITH_ISO8859X "Add ISO8859X support if no iconv" OFF)
option(LIBXML2_WITH_LEGACY "Add deprecated APIs for compatibility" OFF)
option(LIBXML2_WITH_LZMA "Use liblzma" OFF)
option(LIBXML2_WITH_MEM_DEBUG "Add the memory debugging module" OFF)
option(LIBXML2_WITH_MODULES "Add the dynamic modules support" OFF)
option(LIBXML2_WITH_OUTPUT "Add the serialization support" ON)
option(LIBXML2_WITH_PATTERN "Add the xmlPattern selection interface" OFF)
option(LIBXML2_WITH_PROGRAMS "Build programs" OFF)
option(LIBXML2_WITH_PUSH "Add the PUSH parser interfaces" ON)
option(LIBXML2_WITH_PYTHON "Build Python bindings" OFF)
option(LIBXML2_WITH_READER "Add the xmlReader parsing interface" ON)
option(LIBXML2_WITH_REGEXPS "Add Regular Expressions support" OFF)
option(LIBXML2_WITH_RUN_DEBUG "Add the runtime debugging module" OFF)
option(LIBXML2_WITH_SAX1 "Add the older SAX1 interface" OFF)
option(LIBXML2_WITH_SCHEMAS "Add Relax-NG and Schemas support" OFF)
option(LIBXML2_WITH_SCHEMATRON "Add Schematron support" OFF)
option(LIBXML2_WITH_TESTS "Build tests" OFF)
option(LIBXML2_WITH_THREADS "Add multithread support" ON)
option(LIBXML2_WITH_THREAD_ALLOC "Add per-thread memory" OFF)
option(LIBXML2_WITH_TREE "Add the DOM like tree manipulation APIs" ON)
set(LIBXML2_WITH_TRIO OFF)
set(LIBXML2_WITH_UNICODE ON)
option(LIBXML2_WITH_VALID "Add the DTD validation support" OFF)
option(LIBXML2_WITH_WRITER "Add the xmlWriter saving interface" ON)
option(LIBXML2_WITH_XINCLUDE "Add the XInclude support" OFF)
option(LIBXML2_WITH_XPATH "Add the XPATH support" ON)
option(LIBXML2_WITH_XPTR "Add the XPointer support" OFF)
option(LIBXML2_WITH_ZLIB "Use libz" ON)
set(LIBXML2_XMLCONF_WORKING_DIR ${CMAKE_CURRENT_BINARY_DIR} CACHE PATH "Working directory for XML Conformance Test Suite")

set(ENABLE_COBALT FALSE CACHE BOOL "ENABLE_COBALT")

option(USE_SYSTEM_ZLIB FALSE)

set(PROJ_LIB_NAME ${PROJECT_NAME})

set(libxml_DIR "${CMAKE_CURRENT_SOURCE_DIR}/chromium/third_party/libxml/")

option(COMPILE_WITH_LLVM_TOOLS
  "Enable clang from llvm_tools (conan package)" OFF)

# see https://github.com/Ericsson/codechecker/blob/master/tools/report-converter/README.md#undefined-behaviour-sanitizer
# NOTE: Compile with -g and -fno-omit-frame-pointer
# to get proper debug information in your binary.
# NOTE: Run your program with environment variable UBSAN_OPTIONS=print_stacktrace=1.
# see https://github.com/google/sanitizers/wiki/SanitizerCommonFlags
option(ENABLE_UBSAN
  "Enable Undefined Behaviour Sanitizer" OFF)

# see https://github.com/google/sanitizers/wiki/AddressSanitizerLeakSanitizer
# see https://github.com/Ericsson/codechecker/blob/master/tools/report-converter/README.md#address-sanitizer
# NOTE: Compile with -g and -fno-omit-frame-pointer
# to get proper debug information in your binary.
# NOTE: use ASAN_OPTIONS=detect_leaks=1 LSAN_OPTIONS=suppressions=suppr.txt
# NOTE: You need the ASAN_OPTIONS=symbolize=1
# to turn on resolving addresses in object code
# to source code line numbers and filenames.
# This option is implicit for Clang but it won't do any harm.
# see https://github.com/google/sanitizers/wiki/SanitizerCommonFlags
option(ENABLE_ASAN
  "Enable Address Sanitizer" OFF)

# see https://github.com/Ericsson/codechecker/blob/master/tools/report-converter/README.md#memory-sanitizer
# NOTE: Compile with -g and -fno-omit-frame-pointer
# to get proper debug information in your binary.
option(ENABLE_MSAN
  "Enable Memory Sanitizer" OFF)

# see https://github.com/Ericsson/codechecker/blob/master/tools/report-converter/README.md#thread-sanitizer
# NOTE: Compile with -g
# to get proper debug information in your binary.
option(ENABLE_TSAN
  "Enable Thread Sanitizer" OFF)

if(COMPILE_WITH_LLVM_TOOLS)
  message(STATUS
    "Using COMPILE_WITH_LLVM_TOOLS")
  # do not check compile in conanbuildinfo
  # cause we will switch to other compiler after conan install
  set(CONAN_DISABLE_CHECK_COMPILER ON)
else(COMPILE_WITH_LLVM_TOOLS)
  message(STATUS
    "Disabled COMPILE_WITH_LLVM_TOOLS")
endif(COMPILE_WITH_LLVM_TOOLS)

# --------------------------- conan configuration ------------------------------

# Conan package manager List of packages used by the project is container in
# conanfile.py
option(CONAN_AUTO_INSTALL "Let CMake call conan install automatically" OFF)
if (CONAN_AUTO_INSTALL)
  set(CONAN_PROFILE
      "default"
      CACHE STRING "Conan profile to use during installation")
  include(cmake/conan-auto-install.cmake)
  conan_auto_install(${CONAN_PROFILE})
endif()

if(EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
  list(APPEND CMAKE_MODULE_PATH ${CMAKE_BINARY_DIR}/)
  include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
  include(${CMAKE_BINARY_DIR}/conan_paths.cmake OPTIONAL)
  conan_basic_setup(
    # prevent conan_basic_setup from resetting cmake variables
    TARGETS
    KEEP_RPATHS
    # see https://github.com/conan-io/conan/issues/6012
    NO_OUTPUT_DIRS)
else()
  message (FATAL_ERROR "must use conan")
endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/)

if(ENABLE_MSAN OR ENABLE_TSAN OR ENABLE_ASAN OR ENABLE_UBSAN)
  find_package(cmake_sanitizers REQUIRED)
endif()

find_package(cmake_helper_utils REQUIRED)

# prefer ASCII for folder names
force_latin_paths() # from cmake_helper_utils (conan package)

# out dirs (CMAKE_*_OUTPUT_DIRECTORY) must be not empty
validate_out_dirs() # from cmake_helper_utils (conan package)

# In-source builds not allowed
validate_out_source_build(WARNING) # from cmake_helper_utils (conan package)

if(ENABLE_MSAN)
  add_msan_flags()
endif(ENABLE_MSAN)

if(ENABLE_TSAN)
  add_tsan_flags()
endif(ENABLE_TSAN)

if(ENABLE_ASAN)
  add_asan_flags()
endif(ENABLE_ASAN)

if(ENABLE_UBSAN)
  add_ubsan_flags()
endif(ENABLE_UBSAN)

if(COMPILE_WITH_LLVM_TOOLS)
  message(STATUS
    "Using COMPILE_WITH_LLVM_TOOLS")
  # force change CMAKE_*_COMPILER and CMAKE_LINKER to clang from conan
  compile_with_llvm_tools() # from cmake_helper_utils (conan package)
else(COMPILE_WITH_LLVM_TOOLS)
  message(STATUS
    "Disabled COMPILE_WITH_LLVM_TOOLS")
endif(COMPILE_WITH_LLVM_TOOLS)

find_package(cmake_platform_detection REQUIRED)
run_cmake_platform_detection()
# NOTE: perform platform checks before everything else
include(cmake/PlatformChecks)

find_package(cmake_build_options REQUIRED)
setup_default_build_type(RELEASE)
setup_cmake_build_options(RELEASE DEBUG)

if(ENABLE_COBALT)
  find_package(cobalt_starboard_headers_only REQUIRED)
  if(TARGET cobalt_starboard_headers_only::cobalt_starboard_headers_only-static)
    set(cobalt_starboard_headers_only_LIB cobalt_starboard_headers_only::cobalt_starboard_headers_only-static)
  else()
    message(FATAL_ERROR "not supported: using system provided cobalt_starboard_headers_only library")
  endif()
endif(ENABLE_COBALT)

if(LIBXML2_WITH_ICONV)
	#find_package(Iconv REQUIRED)
  message(FATAL_ERROR "TODO: Iconv")
endif()

if(LIBXML2_WITH_ICU)
  # chromium_icu
  find_package(chromium_icu REQUIRED) # TODO: WIN
  if(NOT TARGET chromium_icu::chromium_icu-static)
    message(FATAL_ERROR "not supported: using system provided chromium_icu library")
  endif()
  set(CUSTOM_ICU_LIB chromium_icu::chromium_icu-static) # see icu.cmake
else()
  message(FATAL_ERROR "TODO: TEST WITHOUT ICU")
endif()

if(LIBXML2_WITH_LZMA)
	#find_package(LibLZMA REQUIRED)
  message(FATAL_ERROR "TODO: LibLZMA")
endif()

if(LIBXML2_WITH_ZLIB)
  # chromium_zlib
  if(NOT USE_SYSTEM_ZLIB)
    find_package(chromium_zlib REQUIRED)
    if(TARGET chromium_zlib::chromium_zlib)
      set(zlib_LIB chromium_zlib::chromium_zlib)
    else()
      message(FATAL_ERROR "not supported: using system provided chromium_zlib library")
    endif()
  endif(NOT USE_SYSTEM_ZLIB)
else()
  message(FATAL_ERROR "TODO: TEST WITHOUT ZLIB")
endif()

if(LIBXML2_WITH_PYTHON)
	check_include_files(unistd.h HAVE_UNISTD_H)
	check_symbol_exists(F_GETFL fcntl.h HAVE_F_GETFL)
	if(HAVE_UNISTD_H AND HAVE_F_GETFL)
		find_package(Python COMPONENTS Interpreter Development REQUIRED)
	else()
		find_package(Python2 COMPONENTS Interpreter Development REQUIRED)
		add_library(Python::Python ALIAS Python2::Python)
		set(Python_EXECUTABLE ${Python2_EXECUTABLE})
		set(Python_SITEARCH ${Python2_SITEARCH})
	endif()
	set(LIBXML2_PYTHON_INSTALL_DIR ${Python_SITEARCH} CACHE PATH "Python bindings install directory")
endif()

if(LIBXML2_WITH_THREADS)
	find_package(Threads REQUIRED)
endif()

foreach(VARIABLE IN ITEMS WITH_AUTOMATA WITH_C14N WITH_CATALOG WITH_DEBUG WITH_DOCB WITH_EXPR WITH_FTP WITH_HTML WITH_HTTP WITH_ICONV WITH_ICU WITH_ISO8859X WITH_LEGACY WITH_LZMA WITH_MEM_DEBUG WITH_MODULES WITH_OUTPUT WITH_PATTERN WITH_PUSH WITH_READER WITH_REGEXPS WITH_RUN_DEBUG WITH_SAX1 WITH_SCHEMAS WITH_SCHEMATRON WITH_THREADS WITH_THREAD_ALLOC WITH_TREE WITH_TRIO WITH_UNICODE WITH_VALID WITH_WRITER WITH_XINCLUDE WITH_XPATH WITH_XPTR WITH_ZLIB)
	if(LIBXML2_${VARIABLE})
		set(${VARIABLE} 1)
	else()
		set(${VARIABLE} 0)
	endif()
endforeach()

set(MODULE_EXTENSION "${CMAKE_SHARED_LIBRARY_SUFFIX}")

set(PACKAGE "libxml2")
set(PACKAGE_BUGREPORT "xml@gnome.org")
set(PACKAGE_NAME "libxml2")
set(PACKAGE_STRING "libxml2 ${VERSION}")
set(PACKAGE_TARNAME "libxml2")
set(PACKAGE_URL "http://www.xmlsoft.org/")
set(PACKAGE_VERSION ${VERSION})

if(LIBLZMA_FOUND)
	list(APPEND CMAKE_REQUIRED_LIBRARIES LibLZMA::LibLZMA)
endif()

if(Threads_FOUND)
	list(APPEND CMAKE_REQUIRED_LIBRARIES Threads::Threads)
endif()

if(ZLIB_FOUND)
	list(APPEND CMAKE_REQUIRED_LIBRARIES ZLIB::ZLIB)
endif()

if(MSVC)
	#configure_file(include/win32config.h config.h COPYONLY)
  configure_file(chromium/third_party/libxml/src/include/win32config.h 
    chromium/third_party/libxml/src/config.h 
    COPYONLY)
else()
	check_c_source_compiles("
		void __attribute__((destructor))
		f(void) {}
		int main(void) { return 0; }
	" ATTRIBUTE_DESTRUCTOR)
	check_c_source_compiles("
		#include <netdb.h>
		int main() { (void) gethostbyname((const char*) \"\"); return 0; }
	" GETHOSTBYNAME_ARG_CAST_CONST)
	if(NOT GETHOSTBYNAME_ARG_CAST_CONST)
		set(GETHOSTBYNAME_ARG_CAST "(char *)")
	else()
		set(GETHOSTBYNAME_ARG_CAST "/**/")
	endif()
	check_include_files(arpa/inet.h HAVE_ARPA_INET_H)
	check_include_files(arpa/nameser.h HAVE_ARPA_NAMESER_H)
	check_struct_has_member("struct sockaddr_storage" ss_family "sys/socket.h;sys/types.h" HAVE_SS_FAMILY)
	check_struct_has_member("struct sockaddr_storage" __ss_family "sys/socket.h;sys/types.h" HAVE_BROKEN_SS_FAMILY)
	if(HAVE_BROKEN_SS_FAMILY)
		set(ss_family __ss_family)
	endif()
	check_function_exists(class HAVE_CLASS)
	check_include_files(ctype.h HAVE_CTYPE_H)
	check_include_files(dirent.h HAVE_DIRENT_H)
	check_include_files(dlfcn.h HAVE_DLFCN_H)
	check_library_exists(dl dlopen "" HAVE_DLOPEN)
	check_include_files(dl.h HAVE_DL_H)
	check_include_files(errno.h HAVE_ERRNO_H)
	check_include_files(fcntl.h HAVE_FCNTL_H)
	check_function_exists(finite HAVE_FINITE)
	check_include_files(float.h HAVE_FLOAT_H)
	check_function_exists(fpclass HAVE_FPCLASS)
	check_function_exists(fprintf HAVE_FPRINTF)
	check_function_exists(fp_class HAVE_FP_CLASS)
	check_function_exists(ftime HAVE_FTIME)
	check_function_exists(getaddrinfo HAVE_GETADDRINFO)
	check_function_exists(gettimeofday HAVE_GETTIMEOFDAY)
	check_include_files(inttypes.h HAVE_INTTYPES_H)
	check_function_exists(isascii HAVE_ISASCII)
	check_function_exists(isinf HAVE_ISINF)
	check_function_exists(isnan HAVE_ISNAN)
	check_function_exists(isnand HAVE_ISNAND)
	check_library_exists(history append_history "" HAVE_LIBHISTORY)
	check_library_exists(lzma lzma_code "" HAVE_LIBLZMA)
	check_library_exists(pthread pthread_join "" HAVE_LIBPTHREAD)
	check_library_exists(readline readline "" HAVE_LIBREADLINE)
	check_library_exists(z gzread "" HAVE_LIBZ)
	check_include_files(limits.h HAVE_LIMITS_H)
	check_function_exists(localtime HAVE_LOCALTIME)
	check_include_files(lzma.h HAVE_LZMA_H)
	check_include_files(malloc.h HAVE_MALLOC_H)
	check_include_files(math.h HAVE_MATH_H)
	check_include_files(memory.h HAVE_MEMORY_H)
	check_function_exists(mmap HAVE_MMAP)
	check_function_exists(munmap HAVE_MUNMAP)
	check_symbol_exists(DIR ndir.h HAVE_NDIR_H)
	check_include_files(netdb.h HAVE_NETDB_H)
	check_include_files(netinet/in.h HAVE_NETINET_IN_H)
	check_include_files(poll.h HAVE_POLL_H)
	check_function_exists(printf HAVE_PRINTF)
	check_include_files(pthread.h HAVE_PTHREAD_H)
	check_function_exists(putenv HAVE_PUTENV)
	check_function_exists(rand HAVE_RAND)
	check_function_exists(rand_r HAVE_RAND_R)
	check_include_files(resolv.h HAVE_RESOLV_H)
	check_library_exists(dld shl_load "" HAVE_SHLLOAD)
	check_function_exists(signal HAVE_SIGNAL)
	check_include_files(signal.h HAVE_SIGNAL_H)
	check_function_exists(snprintf HAVE_SNPRINTF)
	check_function_exists(sprintf HAVE_SPRINTF)
	check_function_exists(srand HAVE_SRAND)
	check_function_exists(sscanf HAVE_SSCANF)
	check_function_exists(stat HAVE_STAT)
	check_include_files(stdarg.h HAVE_STDARG_H)
	check_include_files(stdint.h HAVE_STDINT_H)
	check_include_files(stdlib.h HAVE_STDLIB_H)
	check_function_exists(strftime HAVE_STRFTIME)
	check_include_files(strings.h HAVE_STRINGS_H)
	check_include_files(string.h HAVE_STRING_H)
	check_symbol_exists(DIR sys/dir.h HAVE_SYS_DIR_H)
	check_include_files(sys/mman.h HAVE_SYS_MMAN_H)
	check_symbol_exists(DIR sys/ndir.h HAVE_SYS_NDIR_H)
	check_include_files(sys/select.h HAVE_SYS_SELECT_H)
	check_include_files(sys/socket.h HAVE_SYS_SOCKET_H)
	check_include_files(sys/stat.h HAVE_SYS_STAT_H)
	check_include_files(sys/timeb.h HAVE_SYS_TIMEB_H)
	check_include_files(sys/time.h HAVE_SYS_TIME_H)
	check_include_files(sys/types.h HAVE_SYS_TYPES_H)
	check_function_exists(time HAVE_TIME)
	check_include_files(time.h HAVE_TIME_H)
	check_include_files(unistd.h HAVE_UNISTD_H)
	check_function_exists(va_copy HAVE_VA_COPY)
	check_function_exists(vfprintf HAVE_VFPRINTF)
	check_function_exists(vsnprintf HAVE_VSNPRINTF)
	check_function_exists(vsprintf HAVE_VSPRINTF)
	check_function_exists(__va_copy HAVE___VA_COPY)
	check_c_source_compiles("
		#include <stdlib.h>
		#include <iconv.h>
		extern
		#ifdef __cplusplus
		\"C\"
		#endif
		#if defined(__STDC__) || defined(__cplusplus)
		size_t iconv(iconv_t cd, char** inbuf, size_t* inbytesleft, char** outbuf, size_t* outbytesleft);
		#else
		size_t iconv();
		#endif
		int main() { return 0; }
	" ICONV_CONST_TEST)
	if(NOT ICONV_CONST_TEST)
		set(ICONV_CONST "const")
	endif()
	set(LT_OBJDIR ".libs/")
	check_c_source_compiles("
		#include <sys/socket.h>
		#include <sys/types.h>
		int main() { (void) send(1, (const char*) \"\", 1, 1); return 0; }
	" SEND_ARG2_CAST_CONST)
	if(NOT SEND_ARG2_CAST_CONST)
		set(SEND_ARG2_CAST "(char *)")
	else()
		set(SEND_ARG2_CAST "/**/")
	endif()
	check_include_files("float.h;stdarg.h;stdlib.h;string.h" STDC_HEADERS)
	check_c_source_compiles("
		#include <stdarg.h>
		void a(va_list* ap) {};
		int main() { va_list ap1, ap2; a(&ap1); ap2 = (va_list) ap1; return 0; }
	" VA_LIST_IS_ARRAY_TEST)
	if(VA_LIST_IS_ARRAY_TEST)
		set(VA_LIST_IS_ARRAY FALSE)
	else()
		set(VA_LIST_IS_ARRAY TRUE)
	endif()
	check_c_source_compiles("
		#include <stddef.h>
		#include <sys/socket.h>
		#include <sys/types.h>
		int main() { (void) getsockopt(1, 1, 1, NULL, (socklen_t*) NULL); return 0; }
	" XML_SOCKLEN_T_SOCKLEN_T)
	if(XML_SOCKLEN_T_SOCKLEN_T)
		set(XML_SOCKLEN_T socklen_t)
	else()
		check_c_source_compiles("
			#include <stddef.h>
			#include <sys/socket.h>
			#include <sys/types.h>
			int main() { (void) getsockopt(1, 1, 1, NULL, (size_t*) NULL); return 0; }
		" XML_SOCKLEN_T_SIZE_T)
		if(XML_SOCKLEN_T_SIZE_T)
			set(XML_SOCKLEN_T size_t)
		else()
			check_c_source_compiles("
				#include <stddef.h>
				#include <sys/socket.h>
				#include <sys/types.h>
				int main() { (void) getsockopt (1, 1, 1, NULL, (int*) NULL); return 0; }
			" XML_SOCKLEN_T_INT)
			set(XML_SOCKLEN_T int)
		endif()
	endif()
	#configure_file(config.h.cmake.in config.h)
  configure_file(chromium/third_party/libxml/src/config.h.cmake.in
    chromium/third_party/libxml/src/config.h 
    COPYONLY)
endif()

# # uses Config.cmake or a -config.cmake file
# # see https://gitlab.kitware.com/cmake/community/wikis/doc/tutorials/How-to-create-a-ProjectConfig.cmake-file
# find_package(chromium_build_util REQUIRED)
# #
# if(TARGET chromium_build_util::chromium_build_util-static)
#   set(build_util_LIB chromium_build_util::chromium_build_util-static)
# else()
#   message(FATAL_ERROR "not supported: using system provided chromium_build_util library")
# endif()

include(cmake/CommonOptions)

include(cmake/ProjectFiles)

add_library(${PROJ_LIB_NAME}-test-includes INTERFACE)

# $<INSTALL_INTERFACE:...> is exported using install(EXPORT)
# $<BUILD_INTERFACE:...> is exported using export(), or when the target is used by another target in the same buildsystem
macro(add_relative_include_dir TARGET VISIBILITY_BUILD VISIBILITY_INSTALL NEW_ELEM)
  target_include_directories(${TARGET}
    ${VISIBILITY_BUILD} "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${NEW_ELEM}>"
    ${VISIBILITY_INSTALL} "$<INSTALL_INTERFACE:$<INSTALL_PREFIX>/${CMAKE_INSTALL_INCLUDEDIR}/${NEW_ELEM}>"
  )
  target_include_directories( ${TARGET}-test-includes SYSTEM INTERFACE
    ${CMAKE_CURRENT_SOURCE_DIR}/${NEW_ELEM} )
endmacro(add_relative_include_dir)

add_library(${PROJ_LIB_NAME} STATIC
  ${libxml_SOURCES}
)

# path to third_party/libxml/libxml.h
add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium")

# add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/third_party")

add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml")

# requires "libxml/xmlreader.h"
add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/src/include")

# if (current_cpu == "x86" || current_cpu == "x64")
if(TARGET_EMSCRIPTEN)
  # requires libxml/xmlversion.h
  configure_file(chromium/third_party/libxml/src/include/libxml/xmlversion.h.in 
    chromium/web_ports/libxml_wrapper/emscripten/include/libxml/xmlversion.h)
  add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/web_ports/libxml_wrapper/emscripten/include")
  # requires config.h
  add_relative_include_dir(${PROJ_LIB_NAME} PRIVATE PRIVATE "chromium/web_ports/libxml_wrapper/emscripten")
  add_relative_include_dir(${PROJ_LIB_NAME} PRIVATE PRIVATE "include/chromium/web_ports/libxml_wrapper/emscripten")
elseif(TARGET_LINUX)
  # requires libxml/xmlversion.h
  configure_file(chromium/third_party/libxml/src/include/libxml/xmlversion.h.in 
    chromium/third_party/libxml/linux/include/libxml/xmlversion.h)
  add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/linux/include")
  # requires config.h
  add_relative_include_dir(${PROJ_LIB_NAME} PRIVATE PRIVATE "chromium/third_party/libxml/linux")
elseif(TARGET_WINDOWS)
  # requires libxml/xmlversion.h
  configure_file(chromium/third_party/libxml/src/include/libxml/xmlversion.h.in 
    chromium/third_party/libxml/win32/include/libxml/xmlversion.h)
  add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/win32/include")
  # requires config.h
  add_relative_include_dir(${PROJ_LIB_NAME} PRIVATE PRIVATE "chromium/third_party/libxml/win32")
#elseif(TARGET_MAC) # TODO
#  # requires libxml/xmlversion.h
#  configure_file(chromium/third_party/libxml/src/include/libxml/xmlversion.h.in 
#    chromium/third_party/libxml/mac/include/libxml/xmlversion.h)
#  add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/mac/include")
#  # requires config.h
#  add_relative_include_dir(${PROJ_LIB_NAME} PRIVATE PRIVATE "chromium/third_party/libxml/mac")
else()
  message(FATAL_ERROR "platform not supported")
endif()

#if (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/chromium/build/build_config.h")
#  message(FATAL_ERROR "Could not find build/build_config.h")
#endif()

# must include build/build_config.h
#add_relative_include_dir(${PROJ_LIB_NAME} PUBLIC PUBLIC "chromium")

#target_include_directories(${PROJ_LIB_NAME} PRIVATE
#  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/chromium>"
#)

#if(NOT DEFINED build_util_LIB)
#  message(FATAL_ERROR "NOT DEFINED: build_util_LIB")
#endif(NOT DEFINED build_util_LIB)
#
#target_link_libraries(${PROJ_LIB_NAME} PUBLIC
#  ${build_util_LIB}
#)

if(NOT DEFINED CUSTOM_ICU_LIB)
  message(FATAL_ERROR "CUSTOM_ICU_LIB must be defined")
endif(NOT DEFINED CUSTOM_ICU_LIB)

if(EMSCRIPTEN)
  target_link_libraries(${PROJ_LIB_NAME} PUBLIC
    ${CUSTOM_ICU_LIB} # icuuc
  )
else()
  if(NOT USE_SYSTEM_ZLIB)
    if(NOT DEFINED zlib_LIB)
      message(FATAL_ERROR "zlib_LIB must be defined")
    endif(NOT DEFINED zlib_LIB)
  endif(NOT USE_SYSTEM_ZLIB)
endif()

if(ENABLE_COBALT)
  if(NOT DEFINED cobalt_starboard_headers_only_LIB)
    message(FATAL_ERROR "NOT DEFINED: cobalt_starboard_headers_only_LIB")
  endif(NOT DEFINED cobalt_starboard_headers_only_LIB)

  # see defined(COBALT) in htmlEmitImpliedRootLevelParagraph
  target_link_libraries(${PROJ_LIB_NAME} PUBLIC
    ${cobalt_starboard_headers_only_LIB}
  )
endif(ENABLE_COBALT)

set_property(TARGET ${PROJ_LIB_NAME} PROPERTY C_EXTENSIONS ON)
set_property(TARGET ${PROJ_LIB_NAME} PROPERTY C_STANDARD 11)
set_property(TARGET ${PROJ_LIB_NAME} PROPERTY CXX_STANDARD 17)

# POSITION_INDEPENDENT_CODE for -fPIC
set_property(TARGET ${PROJ_LIB_NAME} PROPERTY POSITION_INDEPENDENT_CODE ON)

if(ENABLE_MSAN OR ENABLE_TSAN OR ENABLE_ASAN OR ENABLE_UBSAN)
  message(STATUS
    "Using sanitizers")

  if(cmake_build_type_tolower MATCHES "release" )
    message(WARNING
      "Disable sanitizers in Release builds")
  endif()

  # use llvm_tools from conan
  find_program_helper(llvm-symbolizer
    PATHS
      #${CONAN_BIN_DIRS}
      ${CONAN_BIN_DIRS_LLVM_TOOLS}
    NO_SYSTEM_ENVIRONMENT_PATH
    NO_CMAKE_SYSTEM_PATH
    ${ARGUMENTS_UNPARSED_ARGUMENTS}
    REQUIRED
    OUT_VAR LLVM_SYMBOLIZER_PROGRAM
    VERBOSE TRUE
  )
  check_sanitizer_options(
    ENABLE_TSAN ${ENABLE_TSAN}
    ENABLE_ASAN ${ENABLE_ASAN}
    ENABLE_MSAN ${ENABLE_MSAN}
    ENABLE_UBSAN ${ENABLE_UBSAN}
    LLVM_SYMBOLIZER_PROGRAM ${LLVM_SYMBOLIZER_PROGRAM}
  )
else()
  message(STATUS
    "Disabled sanitizers")
endif()

if(ENABLE_MSAN)
  message(STATUS "enabling MSAN on ${PROJ_LIB_NAME}")
  add_msan_static_link(${PROJ_LIB_NAME})
  add_msan_definitions(${PROJ_LIB_NAME})
  add_msan_flags()
else(ENABLE_MSAN)
  message(STATUS
    "Disabled ENABLE_MSAN")
endif(ENABLE_MSAN)

if(ENABLE_TSAN)
  message(STATUS "enabling TSAN on ${PROJ_LIB_NAME}")
  add_tsan_static_link(${PROJ_LIB_NAME})
  add_tsan_flags(${PROJ_LIB_NAME})
  add_tsan_definitions(${PROJ_LIB_NAME})
  add_tsan_flags()
else(ENABLE_TSAN)
  message(STATUS
    "Disabled ENABLE_TSAN")
endif(ENABLE_TSAN)

if(ENABLE_ASAN)
  message(STATUS "enabling ASAN on ${PROJ_LIB_NAME}")
  add_asan_static_link(${PROJ_LIB_NAME})
  add_asan_definitions(${PROJ_LIB_NAME})
  add_asan_flags()
else(ENABLE_ASAN)
  message(STATUS
    "Disabled ENABLE_ASAN")
endif(ENABLE_ASAN)

if(ENABLE_UBSAN)
  message(STATUS "enabling UBSAN on ${PROJ_LIB_NAME}")
  add_ubsan_static_link(${PROJ_LIB_NAME})
  add_ubsan_definitions(${PROJ_LIB_NAME})
  add_ubsan_flags()
else(ENABLE_UBSAN)
  message(STATUS
    "Disabled ENABLE_UBSAN")
endif(ENABLE_UBSAN)

if(NOT BUILD_SHARED_LIBS)
  target_compile_definitions(${PROJ_LIB_NAME} PRIVATE
    # Define GLIBXML_STATIC as nothing to match how GLIBXML.h (an internal header)
    # defines GLIBXML_STATIC, otherwise we get the macro redefined warning from
    # GCC. ("defines" does "-DFOO" which defines the macro FOO as 1.)
    GLIBXML_STATIC=""
  )

	target_compile_definitions(${PROJ_LIB_NAME} INTERFACE 
    LIBXML_STATIC
  )
endif()

if(LIBXML2_WITH_THREADS)
	target_compile_definitions(${PROJ_LIB_NAME} PRIVATE _REENTRANT)
	if(WIN32)
		target_compile_definitions(${PROJ_LIB_NAME} PRIVATE HAVE_WIN32_THREADS)
	endif()
endif()

if(TARGET_EMSCRIPTEN)
  # use PROPERTY CXX_STANDARD 17
else()
  target_compile_features(${PROJ_LIB_NAME}
    PUBLIC cxx_auto_type
    PRIVATE cxx_variadic_templates)
endif()

target_compile_options(${PROJ_LIB_NAME} PRIVATE
  $<$<CXX_COMPILER_ID:GNU>:-Wall>)

if(HAVE_DLOPEN)
	target_link_libraries(${PROJ_LIB_NAME} PRIVATE dl)
	set(MODULE_PLATFORM_LIBS "-ldl")
endif()

if(HAVE_SHLLOAD)
	target_link_libraries(${PROJ_LIB_NAME} PRIVATE dld)
	set(MODULE_PLATFORM_LIBS "-ldld")
endif()

if(UNIX)
	target_link_libraries(${PROJ_LIB_NAME} PRIVATE m)
	set(M_LIBS "-lm")
endif()

if(WIN32)
	target_link_libraries(${PROJ_LIB_NAME} PRIVATE ws2_32)
	set(WIN32_EXTRA_LIBADD "-lws2_32")
endif()

if(LIBXML2_WITH_ICONV)
	#target_link_libraries(${PROJ_LIB_NAME} PUBLIC Iconv::Iconv)
	#if(NOT Iconv_IS_BUILT_IN)
	#	set(ICONV_LIBS "-liconv")
	#endif()
  message(FATAL_ERROR "TODO: Iconv")
endif()

if(LIBXML2_WITH_ICU)
  target_link_libraries(${PROJ_LIB_NAME} PUBLIC
    ${CUSTOM_ICU_LIB} # icuuc
  )
	#target_link_libraries(${PROJ_LIB_NAME} PRIVATE ICU::data ICU::i18n ICU::uc)
	#if(WIN32)
	#	set(ICU_LIBS "-licudt -licuin -licuuc")
	#else()
	#	set(ICU_LIBS "-licudata -licui18n -licuuc")
	#endif()
endif()

if(LIBXML2_WITH_LZMA)
	#target_link_libraries(${PROJ_LIB_NAME} PRIVATE LibLZMA::LibLZMA)
	#set(LZMA_LIBS "-llzma")
  message(FATAL_ERROR "TODO: LZMA")
endif()

if(LIBXML2_WITH_THREADS)
	target_link_libraries(${PROJ_LIB_NAME} PRIVATE Threads::Threads)
	set(THREAD_LIBS ${CMAKE_THREAD_LIBS_INIT})
endif()

if(LIBXML2_WITH_ZLIB)
  target_link_libraries(${PROJ_LIB_NAME} PUBLIC
    ${zlib_LIB}
  )
	#target_link_libraries(${PROJ_LIB_NAME} PRIVATE ZLIB::ZLIB)
	#set(Z_LIBS "-lz")
endif()

if(WIN32)
	if(BUILD_SHARED_LIBS)
		set_target_properties(
			${PROJ_LIB_NAME}
			PROPERTIES
			DEBUG_POSTFIX d
		)
	else()
		set_target_properties(
			${PROJ_LIB_NAME}
			PROPERTIES
			DEBUG_POSTFIX sd
			MINSIZEREL_POSTFIX s
			RELEASE_POSTFIX s
			RELWITHDEBINFO_POSTFIX s
		)
	endif()
endif()

#set(DEBUG_LIBRARY_SUFFIX "-d")
set_target_properties(${PROJ_LIB_NAME}
  PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}" # TODO: /lib
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}" # TODO: /lib
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}" # TODO: /bin
    #OUTPUT_NAME "${PROJ_LIB_NAME}$<$<CONFIG:Debug>:${DEBUG_LIBRARY_SUFFIX}>"
)

# install and export steps
include(cmake/Exports)

# if(LIBXML2_WITH_PROGRAMS)
#   set(
#     PROGRAMS
#     xmlcatalog
#     xmllint
#   )
#   foreach(PROGRAM ${PROGRAMS})
#     add_executable(${PROGRAM} ${PROGRAM}.c)
#     target_link_libraries(${PROGRAM} LibXml2)
#     if(HAVE_LIBHISTORY)
#       target_link_libraries(${PROGRAM} history)
#     endif()
#     if(HAVE_LIBREADLINE)
#       target_link_libraries(${PROGRAM} readline)
#     endif()
    # install(TARGETS	${PROGRAM} EXPORT LibXml2 RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR} COMPONENT programs)
#   endforeach()
# endif()
# 
# if(LIBXML2_WITH_TESTS)
#   enable_testing()
#   set(
#     TESTS
#     runxmlconf
#     runsuite
#     testapi
#     testAutomata
#     testC14N
#     testchar
#     testdict
#     testHTML
#     testModule
#     testlimits
#     testReader
#     testrecurse
#     testRegexp
#     testRelax
#     testSAX
#     testSchemas
#     testURI
#     testXPath
#   )
#   foreach(TEST ${TESTS})
#     add_executable(${TEST} ${TEST}.c)
#     target_link_libraries(${TEST} LibXml2)
#   endforeach()
#   if(EXISTS ${LIBXML2_XMLCONF_WORKING_DIR}/xmlconf/xmlconf.xml)
    # add_test(NAME runxmlconf COMMAND runxmlconf WORKING_DIRECTORY ${LIBXML2_XMLCONF_WORKING_DIR})
#   endif()
#   if(NOT WIN32)
#     add_test(NAME testapi COMMAND testapi)
#   endif()
#   add_test(NAME testchar COMMAND testchar)
#   add_test(NAME testdict COMMAND testdict)
#   add_test(NAME testrecurse COMMAND testrecurse WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
#   if(Threads_FOUND)
#     set(
#       TESTS_THREADS
#       runtest
#       testThreads
#     )
#     foreach(TEST ${TESTS_THREADS})
#       add_executable(${TEST} ${TEST}.c)
#       if(WIN32)
#         target_compile_definitions(${TEST} PRIVATE HAVE_WIN32_THREADS)
#       endif()
#       target_link_libraries(${TEST} LibXml2 Threads::Threads)
#     endforeach()
    # add_test(NAME runtest COMMAND runtest --out ${CMAKE_CURRENT_BINARY_DIR} WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
#     add_test(NAME testThreads COMMAND testThreads WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
#   endif()
# endif()
# 
# if(LIBXML2_WITH_PYTHON)
#   execute_process(
#     COMMAND
#     ${Python_EXECUTABLE}
#     ${CMAKE_CURRENT_SOURCE_DIR}/python/generator.py
#     ${CMAKE_CURRENT_SOURCE_DIR}/doc/libxml2-api.xml
#     ${CMAKE_CURRENT_SOURCE_DIR}/python/libxml2-python-api.xml
#     WORKING_DIRECTORY
#     ${CMAKE_CURRENT_BINARY_DIR}
#   )
#   file(READ python/libxml.py LIBXML_PY)
#   file(WRITE ${CMAKE_CURRENT_BINARY_DIR}/libxml2.py.in "${LIBXML_PY}")
#   file(READ ${CMAKE_CURRENT_BINARY_DIR}/libxml2class.py LIBXML2CLASS_PY)
#   file(APPEND ${CMAKE_CURRENT_BINARY_DIR}/libxml2.py.in "${LIBXML2CLASS_PY}")
#   configure_file(${CMAKE_CURRENT_BINARY_DIR}/libxml2.py.in libxml2.py COPYONLY)
#   add_library(
#     LibXml2Mod
#     libxml2-py.c
#     libxml2-py.h
#     python/libxml.c
#     python/libxml_wrap.h
#     python/types.c
#   )
#   target_include_directories(
#     LibXml2Mod
#     PUBLIC
#     $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/python>
#   )
#   target_link_libraries(LibXml2Mod LibXml2 Python::Python)
#   set_target_properties(
#     LibXml2Mod
#     PROPERTIES
#     IMPORT_PREFIX lib
#     OUTPUT_NAME xml2mod
#     PREFIX lib
#     VERSION ${VERSION}
#   )
#   install(
#     TARGETS	LibXml2Mod
#     ARCHIVE DESTINATION ${LIBXML2_PYTHON_INSTALL_DIR} COMPONENT development
    # LIBRARY DESTINATION ${LIBXML2_PYTHON_INSTALL_DIR} COMPONENT runtime NAMELINK_COMPONENT development
#     RUNTIME DESTINATION ${LIBXML2_PYTHON_INSTALL_DIR} COMPONENT runtime
#   )
#   if(MSVC AND BUILD_SHARED_LIBS)
    # install(FILES $<TARGET_PDB_FILE:LibXml2Mod> DESTINATION ${LIBXML2_PYTHON_INSTALL_DIR} CONFIGURATIONS Debug RelWithDebInfo COMPONENT debug)
#   endif()
  # install(FILES python/drv_libxml2.py DESTINATION ${LIBXML2_PYTHON_INSTALL_DIR} COMPONENT runtime)
  # install(FILES ${CMAKE_CURRENT_BINARY_DIR}/libxml2.py DESTINATION ${LIBXML2_PYTHON_INSTALL_DIR} COMPONENT runtime)
# endif()
# 
# install(FILES libxml.3 DESTINATION ${CMAKE_INSTALL_MANDIR}/man3 COMPONENT documentation)
# install(FILES doc/xmlcatalog.1 DESTINATION ${CMAKE_INSTALL_MANDIR}/man1 COMPONENT documentation)
# install(FILES doc/xmllint.1 DESTINATION ${CMAKE_INSTALL_MANDIR}/man1 COMPONENT documentation)
# install(DIRECTORY doc/ DESTINATION ${CMAKE_INSTALL_DATADIR}/doc/libxml2 COMPONENT documentation PATTERN Makefile.* EXCLUDE)

