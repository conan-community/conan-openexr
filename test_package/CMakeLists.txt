project(PackageTest)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(OpenEXR ${OPENEXR_VERSION} EXACT REQUIRED)

message(STATUS "OpenEXR libraries: ${OPENEXR_LIBRARIES}")
message(STATUS "OpenEXR include dirs: ${OPENEXR_INCLUDE_DIRS}")

add_executable(testPackage main.cpp)
target_link_libraries(testPackage ${OPENEXR_LIBRARIES})

