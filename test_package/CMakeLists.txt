cmake_minimum_required(VERSION 2.8.11)
project(chromium_libxml_test_package)

option(LIBXML2_WITH_THREADS "Add multithread support" ON)

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
if(TARGET chromium_libxml::chromium_libxml)
  set(libxml_LIB chromium_libxml::chromium_libxml)
else()
  message(FATAL_ERROR "not supported: using system provided chromium_libxml library")
endif()

if(LIBXML2_WITH_THREADS)
	find_package(Threads REQUIRED)
endif()

add_executable(${PROJECT_NAME} test_package.c)
target_link_libraries(${PROJECT_NAME} PUBLIC
  ${libxml_LIB})

if(LIBXML2_WITH_THREADS)
  if(WIN32)
    target_compile_definitions(${PROJECT_NAME} PRIVATE HAVE_WIN32_THREADS)
  endif()
  target_link_libraries(${PROJECT_NAME} Threads::Threads)
endif()
