qt_add_library(core STATIC)
add_library(threatping::core ALIAS core)

target_sources(
  core
  PRIVATE src/ProvidersRegistry.cpp
  PUBLIC include/threatping/providers/core/ProvidersRegistry.h)

target_include_directories(core PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

target_link_libraries(core PUBLIC Qt6::Core threatping::api)
