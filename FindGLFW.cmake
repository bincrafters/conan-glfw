find_path(GLFW_INCLUDE_DIR NAMES GLFW/glfw3.h PATHS {CONAN_INCLUDE_DIRS_GLFW} NO_CMAKE_FIND_ROOT_PATH)
find_library(GLFW_LIBRARY NAMES ${CONAN_LIBS_GLFW} PATHS ${CONAN_LIB_DIRS_GLFW} NO_CMAKE_FIND_ROOT_PATH)

message(STATUS "** GLFW ALREADY FOUND BY CONAN!")
message(STATUS "** FOUND GLFW: ${GLFW_LIBRARY}")
message(STATUS "** FOUND GLFW INCLUDE: ${GLFW_INCLUDE_DIR}")

if(MSVC)
  set(GLFW_LIBRARY ${GLFW_LIBRARY} glu32)
endif()
if(APPLE)
  set(GLFW_LIBRARY ${GLFW_LIBRARY} -framework OpenGL -framework Cocoa -framework IOKit -framework CoreFoundation -framework CoreVideo)
endif()
if(UNIX AND NOT APPLE)
  set(GLFW_LIBRARY ${GLFW_LIBRARY} rt m dl Xrandr Xrender Xi Xinerama Xcursor GL GLU drm Xdamage X11-xcb xcb-glx xcb-dri2 xcb-dri3 xcb-present xcb-sync Xxf86vm Xfixes Xext X11 pthread xcb Xau)
endif()

set(GLFW_FOUND TRUE)
set(GLFW_INCLUDE_DIRS ${GLFW_INCLUDE_DIR})
set(GLFW_LIBRARIES ${GLFW_LIBRARY})

mark_as_advanced(GLFW_LIBRARY GLFW_INCLUDE_DIR)
