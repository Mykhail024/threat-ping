cmake_minimum_required(VERSION 3.30 FATAL_ERROR)

set(THREAT_PING_VERSION "0.1.0")

project(
  threat-ping
  VERSION ${THREAT_PING_VERSION}
  LANGUAGES CXX)

include(GNUInstallDirs)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -pedantic-errors -Werror")
set(CMAKE_CXX_FLAGS_DEBUG
    "${CMAKE_CXX_FLAGS_DEBUG} -O0 -g3 -fno-omit-frame-pointer")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE
      Debug
      CACHE STRING "Build type" FORCE)
endif()

set(TSAN
    OFF
    CACHE STRING "ThreadSanitizer support")

set(THREAT_PING_PLUGIN_INSTALL_DIR
    ""
    CACHE STRING "Installation directory for threat-ping plugins")

string(TOLOWER "${CMAKE_BUILD_TYPE}" build_type_lower)
if(build_type_lower STREQUAL "debug")
  message(STATUS "Building in debug mode")

  find_program(CCACHE_PROGRAM ccache)
  if(CCACHE_PROGRAM)
    set_property(GLOBAL PROPERTY RULE_LAUNCH_COMPILE "${CCACHE_PROGRAM}")
    message(STATUS "Found ccache: ${CCACHE_PROGRAM}")
  endif()

  include(CheckCXXSourceCompiles)
  set(CMAKE_REQUIRED_FLAGS "-fsanitize=thread")
  check_cxx_source_compiles("int main() { return 0; }" HAS_TSAN_WORKAROUND)
  unset(CMAKE_REQUIRED_FLAGS)

  if(HAS_TSAN_WORKAROUND AND TSAN)
    message(STATUS "Building with ThreadSanitizer support")
    set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fsanitize=thread")
    set(CMAKE_EXE_LINKER_FLAGS_DEBUG
        "${CMAKE_EXE_LINKER_FLAGS_DEBUG} -fsanitize=thread")
  endif()
else()
  message(STATUS "Building in release mode")
endif()

include_directories("${CMAKE_BINARY_DIR}")

add_subdirectory(${CMAKE_SOURCE_DIR}/src)

# Installs
if(THREAT_PING_PLUGIN_INSTALL_DIR)
  set(PLUGIN_INSTALL_DIR "${THREAT_PING_PLUGIN_INSTALL_DIR}")
else()
  if(APPLE)
    set(PLUGIN_INSTALL_DIR
        "${CMAKE_INSTALL_PREFIX}/ThreatPing.app/Contents/PlugIns")
  elseif(WIN32)
    set(PLUGIN_INSTALL_DIR "${CMAKE_INSTALL_BINDIR}/plugins")
  elseif(ANDROID)
    set(PLUGIN_INSTALL_DIR "/assets/plugins")
  else()
    # Unix (Linux)
    set(PLUGIN_INSTALL_DIR "${CMAKE_INSTALL_FULL_LIBDIR}/threat-ping/plugins")
  endif()
endif()

set(THREAT_PROVIDER_PLUGIN_INSTALL_DIR "${PLUGIN_INSTALL_DIR}/providers")

message(
  STATUS
    "ThreatPing plugins will be installed to the ${PLUGIN_INSTALL_DIR} directory"
)

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.in
               ${CMAKE_CURRENT_BINARY_DIR}/config.h @ONLY)
