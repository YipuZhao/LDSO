cmake_minimum_required(VERSION 2.8)
project(ldso)

# Set default build type if not specified otherwise.
# See https://cmake.org/pipermail/cmake/2012-May/050243.html
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
  message(STATUS "Setting build type to '${CMAKE_BUILD_TYPE}' as none was specified.")
  # Set the possible values of build type for cmake-gui
  set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release"
    "MinSizeRel" "RelWithDebInfo")
endif()

# C++ standard
if(${CMAKE_VERSION} VERSION_LESS "3.2.0")
  set( CMAKE_CXX_FLAGS "-std=c++11 ${CMAKE_CXX_FLAGS}" )
else()
  set(CMAKE_CXX_STANDARD 11)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
  set(CMAKE_CXX_EXTENSIONS OFF)
endif()

# costum modules
LIST(APPEND CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)

# TODO: change this to not output outside build dir
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

# required libs

# customize eigen dir
# find_package(Eigen3 3.1.0 REQUIRED)
set( EIGEN3_INCLUDE_DIR /usr/include/eigen3 )
MESSAGE("EIGEN include dir: " ${EIGEN3_INCLUDE_DIR})

# customize opencv dir
# set(OpenCV_DIR /opt/opencv3/share/OpenCV)
# find_package(OpenCV 3.4.1 REQUIRED)
set(OpenCV_DIR /opt/opencv2/share/OpenCV)
find_package(OpenCV 2.4.13 REQUIRED core ocl)
MESSAGE("OpenCV include dir: " ${OpenCV_INCLUDE_DIRS})

# customize pangolin dir
# set(Pangolin_DIR /opt/Pangolin/lib/cmake/Pangolin/)
# find_package(Pangolin REQUIRED)
set(Pangolin_FOUND TRUE)
set(Pangolin_INCLUDE_DIRS /opt/Pangolin/include/)
set(Pangolin_LIBRARIES /opt/Pangolin/lib/libpangolin.so)
MESSAGE("Pangolin include dir: " ${Pangolin_INCLUDE_DIRS})

find_package(Glog REQUIRED)

# optional libs
find_package(LibZip QUIET)

set(CMAKE_CXX_FLAGS "-Wall -Wno-deprecated -march=native -Wno-duplicate-decl-specifier -Wno-ignored-qualifiers -Wno-reorder -pthread")

# decide if we have ziplib.
if (LIBZIP_LIBRARY)
  message("--- found ziplib (${LIBZIP_VERSION}), compiling with zip capability.")
  add_definitions(-DHAS_ZIPLIB=1)
  include_directories( ${LIBZIP_INCLUDE_DIR_ZIP} ${LIBZIP_INCLUDE_DIR_ZIPCONF} )
else()
  message("--- not found ziplib (${LIBZIP_LIBRARY}), compiling without zip capability.")
  set(LIBZIP_LIBRARY "")
endif()

include_directories(
        ${EIGEN3_INCLUDE_DIR}
        ${OpenCV_INCLUDE_DIR}
        ${Glog_INCLUDE_DIRS}
        ${Pangolin_INCLUDE_DIRS}

        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/thirdparty/
        ${PROJECT_SOURCE_DIR}/thirdparty/g2o/
        ${PROJECT_SOURCE_DIR}/thirdparty/DBoW3/
)

set( THIRD_PARTY_LIBS
        GLEW
        GL
        ${OpenCV_LIBS}
        ${GLOG_LIBRARY}
        ${Pangolin_LIBRARIES}
        ${PROJECT_SOURCE_DIR}/thirdparty/g2o/lib/libg2o${CMAKE_SHARED_LIBRARY_SUFFIX}
        ${PROJECT_SOURCE_DIR}/thirdparty/DBoW3/build/src/libDBoW3${CMAKE_SHARED_LIBRARY_SUFFIX}
        ${LIBZIP_LIBRARY}
)

add_subdirectory(src)
add_subdirectory(examples)
