include(FetchContent)

set(SMP_LOG_BUILD_EXAMPLES
    OFF
    CACHE BOOL "" FORCE)

FetchContent_Declare(
  smp-log
  GIT_REPOSITORY https://github.com/Mykhail024/smp-log.git
  GIT_TAG v0.1.0)
FetchContent_MakeAvailable(smp-log)

find_package(Qt6 REQUIRED COMPONENTS Core Gui QuickControls2 LinguistTools Svg)

qt_standard_project_setup(REQUIRES 6.11)

set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOMOC ON)
set(QT_QML_GENERATE_QMLLS_INI ON)
set(QT_QML_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/qml)

qt_add_executable(threat-ping main.cpp Application.cpp Application.h)

target_link_libraries(threat-ping PRIVATE smp::log Qt6::Core Qt6::Gui
                                          Qt6::QuickControls2 Qt6::Svg)

