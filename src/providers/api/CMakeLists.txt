qt_add_library(api INTERFACE)
add_library(threatping::api ALIAS api)

target_include_directories(api INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)

target_link_libraries(api INTERFACE Qt6::Core)
