
cmake_minimum_required(VERSION 2.8)
project(AWALE)

include(CheckIncludeFiles)
include(CheckLibraryExists)
include(CTest)
include(ExternalProject)

set(BUILD_SHARED_LIBS ON)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${AWALE_SOURCE_DIR}/modules/")
set(CMAKE_CXX_FLAGS  "-Wall -pedantic -Wfatal-errors -std=c++11")
set(EXECUTABLE_OUTPUT_PATH ${PROJECT_BINARY_DIR}/bin)

find_package(Boost 1.50 COMPONENTS test_exec_monitor program_options REQUIRED)
#find_package(Doxygen)
include_directories("${CMAKE_CURRENT_SOURCE_DIR}/include"
			    "${PROJECT_BINARY_DIR}/include"
				"${PROJECT_BINARY_DIR}/deps/Celero/src/Celero/include")
link_directories("${PROJECT_BINARY_DIR}/bin")
add_subdirectory(src)
add_subdirectory(benchmark)
add_subdirectory(test)



# ------------------------------------ Installation details -------------------

set(LIB_INST_DIR "${CMAKE_INSTALL_PREFIX}/lib64")
set(HEADER_INST_DIR "${CMAKE_INSTALL_PREFIX}/include")

install(DIRECTORY "${AWALE_SOURCE_DIR}/include/"
    DESTINATION "${HEADER_INST_DIR}"
    FILES_MATCHING PATTERN "*.hpp"
)
