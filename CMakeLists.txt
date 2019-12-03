﻿# see https://github.com/chromium/chromium/blob/9db0b5162b8648833c3a6b1af044cebd9d7d3855/base/BUILD.gn

cmake_minimum_required(VERSION 3.4)

# project() must be before checks, see https://stackoverflow.com/a/26437667/10904212
set(PROJECT_NAME "chromium_libxml")
set(PROJECT_VERSION 1.0.0.1)
project(${PROJECT_NAME}
  VERSION ${PROJECT_VERSION}
  LANGUAGES CXX C)

option(ENABLE_COBALT ON)

option(USE_SYSTEM_ZLIB FALSE)

set(STATIC_LIB_NAME ${PROJECT_NAME}-static)

set(libxml_DIR "${CMAKE_CURRENT_SOURCE_DIR}/chromium/third_party/libxml/")

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

find_package(cmake_platform_detection REQUIRED)
run_cmake_platform_detection()

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

# chromium_icu
find_package(chromium_icu REQUIRED) # TODO: WIN
if(NOT TARGET chromium_icu::chromium_icu-static)
  message(FATAL_ERROR "not supported: using system provided chromium_icu library")
endif()
set(CUSTOM_ICU_LIB chromium_icu::chromium_icu-static) # see icu.cmake

# chromium_zlib
if(NOT USE_SYSTEM_ZLIB)
  find_package(chromium_zlib REQUIRED)
  if(TARGET chromium_zlib::chromium_zlib-static)
    set(zlib_LIB chromium_zlib::chromium_zlib-static)
  else()
    message(FATAL_ERROR "not supported: using system provided chromium_zlib library")
  endif()
endif(NOT USE_SYSTEM_ZLIB)

# # uses Config.cmake or a -config.cmake file
# # see https://gitlab.kitware.com/cmake/community/wikis/doc/tutorials/How-to-create-a-ProjectConfig.cmake-file
# find_package(chromium_build_util REQUIRED)
# #
# if(TARGET chromium_build_util::chromium_build_util-static)
#   set(build_util_LIB chromium_build_util::chromium_build_util-static)
# else()
#   message(FATAL_ERROR "not supported: using system provided chromium_build_util library")
# endif()

list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/)

include(cmake/PlatformChecks)

include(cmake/CommonOptions)

include(cmake/ProjectFiles)

# $<INSTALL_INTERFACE:...> is exported using install(EXPORT)
# $<BUILD_INTERFACE:...> is exported using export(), or when the target is used by another target in the same buildsystem
macro(add_relative_include_dir TARGET VISIBILITY_BUILD VISIBILITY_INSTALL NEW_ELEM)
  target_include_directories(${TARGET}
    ${VISIBILITY_BUILD} "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/${NEW_ELEM}>"
    ${VISIBILITY_INSTALL} "$<INSTALL_INTERFACE:$<INSTALL_PREFIX>/${CMAKE_INSTALL_INCLUDEDIR}/${NEW_ELEM}>"
  )
endmacro(add_relative_include_dir)

add_library(${STATIC_LIB_NAME} STATIC
  ${libxml_SOURCES}
)

# path to third_party/libxml/libxml.h
add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium")

# add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/third_party")

add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml")

# requires "libxml/xmlreader.h"
add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/src/include")

# if (current_cpu == "x86" || current_cpu == "x64")
if(TARGET_EMSCRIPTEN)
  # requires libxml/xmlversion.h
  add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/web_ports/libxml_wrapper/emscripten/include")
  # requires config.h
  add_relative_include_dir(${STATIC_LIB_NAME} PRIVATE PRIVATE "chromium/web_ports/libxml_wrapper/emscripten")
elseif(TARGET_LINUX)
  # requires libxml/xmlversion.h
  add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/linux/include")
  # requires config.h
  add_relative_include_dir(${STATIC_LIB_NAME} PRIVATE PRIVATE "chromium/third_party/libxml/linux")
elseif(TARGET_WINDOWS)
  # requires libxml/xmlversion.h
  add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/win32/include")
  # requires config.h
  add_relative_include_dir(${STATIC_LIB_NAME} PRIVATE PRIVATE "chromium/third_party/libxml/win32")
#elseif(TARGET_MAC) # TODO
#  # requires libxml/xmlversion.h
#  add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium/third_party/libxml/mac/include")
#  # requires config.h
#  add_relative_include_dir(${STATIC_LIB_NAME} PRIVATE PRIVATE "chromium/third_party/libxml/mac")
else()
  message(FATAL_ERROR "platform not supported")
endif()

#if (NOT EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/chromium/build/build_config.h")
#  message(FATAL_ERROR "Could not find build/build_config.h")
#endif()

# must include build/build_config.h
#add_relative_include_dir(${STATIC_LIB_NAME} PUBLIC PUBLIC "chromium")

#target_include_directories(${STATIC_LIB_NAME} PRIVATE
#  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/chromium>"
#)

#if(NOT DEFINED build_util_LIB)
#  message(FATAL_ERROR "NOT DEFINED: build_util_LIB")
#endif(NOT DEFINED build_util_LIB)
#
#target_link_libraries(${STATIC_LIB_NAME} PUBLIC
#  ${build_util_LIB}
#)

if(NOT DEFINED CUSTOM_ICU_LIB)
  message(FATAL_ERROR "CUSTOM_ICU_LIB must be defined")
endif(NOT DEFINED CUSTOM_ICU_LIB)

if(EMSCRIPTEN)
  target_link_libraries(${STATIC_LIB_NAME} PUBLIC
    ${CUSTOM_ICU_LIB} # icuuc
  )
else()
  if(NOT USE_SYSTEM_ZLIB)
    if(NOT DEFINED zlib_LIB)
      message(FATAL_ERROR "zlib_LIB must be defined")
    endif(NOT DEFINED zlib_LIB)
  endif(NOT USE_SYSTEM_ZLIB)

  target_link_libraries(${STATIC_LIB_NAME} PUBLIC
    ${zlib_LIB}
    ${CUSTOM_ICU_LIB} # icuuc
  )
endif()

if(NOT DEFINED ENABLE_COBALT)
  message(FATAL_ERROR "NOT DEFINED: ENABLE_COBALT")
endif(NOT DEFINED ENABLE_COBALT)
if(ENABLE_COBALT)
  if(NOT DEFINED cobalt_starboard_headers_only_LIB)
    message(FATAL_ERROR "NOT DEFINED: cobalt_starboard_headers_only_LIB")
  endif(NOT DEFINED cobalt_starboard_headers_only_LIB)

  # see defined(COBALT) in htmlEmitImpliedRootLevelParagraph
  target_link_libraries(${STATIC_LIB_NAME} PUBLIC
    ${cobalt_starboard_headers_only_LIB}
  )
endif(ENABLE_COBALT)

set_property(TARGET ${STATIC_LIB_NAME} PROPERTY CXX_STANDARD 17)

target_compile_definitions(${STATIC_LIB_NAME} PRIVATE
  # Define GLIBXML_STATIC as nothing to match how GLIBXML.h (an internal header)
  # defines GLIBXML_STATIC, otherwise we get the macro redefined warning from
  # GCC. ("defines" does "-DFOO" which defines the macro FOO as 1.)
  GLIBXML_STATIC=""
)

if(TARGET_EMSCRIPTEN)
  # use PROPERTY CXX_STANDARD 17
else()
  target_compile_features(${STATIC_LIB_NAME}
    PUBLIC cxx_auto_type
    PRIVATE cxx_variadic_templates)
endif()

target_compile_options(${STATIC_LIB_NAME} PRIVATE
  $<$<CXX_COMPILER_ID:GNU>:-Wall>)

set(DEBUG_LIBRARY_SUFFIX "-d")
set_target_properties(${STATIC_LIB_NAME}
  PROPERTIES
    ARCHIVE_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}" # TODO: /lib
    LIBRARY_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}" # TODO: /lib
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}" # TODO: /bin
    OUTPUT_NAME "${STATIC_LIB_NAME}$<$<CONFIG:Debug>:${DEBUG_LIBRARY_SUFFIX}>"
)

# install and export steps
include(cmake/Exports)