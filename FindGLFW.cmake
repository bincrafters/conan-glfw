find_path(
  GLFW_INCLUDE_DIR
  NAMES
  GLFW
  PATHS
  include)

find_library(
  GLFW_LIBRARY
  NAMES
  glfw glfw3 glfw3dll
  PATHS
  lib)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(GLFW REQUIRED_VARS GLFW_LIBRARY GLFW_INCLUDE_DIR)


