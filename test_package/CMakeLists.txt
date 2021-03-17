cmake_minimum_required(VERSION 2.8.11)
project(chromium_libxml_test_package)

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

find_package(chromium_libxml MODULE REQUIRED)
if(TARGET chromium_libxml::chromium_libxml-static)
  set(libxml_LIB chromium_libxml::chromium_libxml-static)
else()
  message(FATAL_ERROR "not supported: using system provided chromium_libxml library")
endif()

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PUBLIC
  ${libxml_LIB})
