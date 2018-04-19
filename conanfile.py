from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, os_info, SystemPackageTool
import os
import glob


class GlfwConan(ConanFile):
    name = "glfw"
    version = "3.2.1.20180327"
    revision = "0a3c4f5d80b041ee1a12c8da3503653d98bd1a15"
    description = "The GLFW library - Builds on Windows, Linux and Macos/OSX"
    sources_folder = "sources"
    generators = "cmake"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    url = "https://github.com/bincrafters/conan-glfw"
    license = "https://github.com/glfw/glfw/blob/master/LICENSE.md"
    exports = "FindGLFW.cmake"
    exports_sources = "CMakeLists.txt"

    def system_requirements(self):
        if os_info.is_linux:
            if os_info.with_apt:
                installer = SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    arch_suffix = ':i386'
                    installer.install("g++-multilib")
                else:
                    arch_suffix = ''
                installer.install("%s%s" % ("mesa-common-dev", arch_suffix))
                installer.install("%s%s" % ("libglu1-mesa-dev", arch_suffix))
                installer.install("xorg-dev")
                installer.install("%s%s" % ("libx11-dev", arch_suffix))
                installer.install("%s%s" % ("libxrandr-dev", arch_suffix))
                installer.install("%s%s" % ("libxinerama-dev", arch_suffix))
                installer.install("%s%s" % ("libxcursor-dev", arch_suffix))
                installer.install("%s%s" % ("libxi-dev", arch_suffix))
            elif os_info.with_yum:
                installer = SystemPackageTool()
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    arch_suffix = '.i686'
                    installer.install("glibmm24.i686")
                    installer.install("glibc-devel.i686")
                    installer.install("libXrender-devel.i686")
                    installer.install("libdrm-devel.i686")
                    installer.install("libXdamage-devel.i686")
                    installer.install("libxcb-devel.i686")
                    installer.install("libX11-devel.i686")
                    installer.install("libXxf86vm-devel.i686")
                    installer.install("libXfixes-devel.i686")
                    installer.install("libXext-devel.i686")
                    installer.install("mesa-libGL-devel.i686")
                    installer.install("libXau-devel.i686")
                else:
                    arch_suffix = ''
                installer.install("%s%s" % ("mesa-libGLU-devel", arch_suffix))
                installer.install("%s%s" % ("xorg-x11-server-devel", arch_suffix))
                installer.install("%s%s" % ("libXrandr-devel", arch_suffix))
                installer.install("%s%s" % ("libXinerama-devel", arch_suffix))
                installer.install("%s%s" % ("libXcursor-devel", arch_suffix))
                installer.install("%s%s" % ("libXi-devel", arch_suffix))
            else:
                self.output.warn("Could not determine package manager, skipping Linux system requirements installation.")
   
    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        download("https://github.com/glfw/glfw/archive/%s.zip" % self.revision, "%s.zip" % self.sources_folder)
        unzip("%s.zip" % self.sources_folder)
        os.unlink("%s.zip" % self.sources_folder)
        os.rename("glfw-%s" % self.revision, self.sources_folder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["GLFW_BUILD_EXAMPLES"] = False
        cmake.definitions["GLFW_BUILD_TESTS"] = False
        cmake.definitions["GLFW_BUILD_DOCS"] = False
        cmake.configure()
        cmake.build()

        if self.settings.os == "Macos" and self.options.shared:
            with tools.chdir(os.path.join('sources', 'src')):
                for filename in glob.glob('*.dylib'):
                    self.run('install_name_tool -id {filename} {filename}'.format(filename=filename))

    def package(self):
        self.copy("FindGLFW.cmake", ".", ".")
        self.copy("%s/copying*" % self.sources_folder, dst="licenses",  ignore_case=True, keep_path=False)
        
        self.copy(pattern="*.h", dst="include", src="%s/include" % self.sources_folder, keep_path=True)

        if self.settings.compiler == "Visual Studio":
            self.copy(pattern="*.lib", dst="lib", keep_path=False)
            self.copy(pattern="*.pdb", dst="bin", keep_path=False)
            if self.options.shared:
                self.copy(pattern="*.dll", dst="bin", keep_path=False)
        else:
            if self.options.shared:
                if self.settings.os == "Linux":
                    self.copy(pattern="*.so*", dst="lib", keep_path=False)
                elif self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                elif self.settings.os == "Windows":
                    self.copy(pattern="*dll.a", dst="lib", keep_path=False)
                    self.copy(pattern="*.dll", dst="bin", keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", keep_path=False)

    def package_info(self):
        if self.settings.os == "Windows":
            if self.options.shared:
                self.cpp_info.libs = ['glfw3dll']
            else:
                self.cpp_info.libs = ['glfw3']
        else:
            if self.options.shared:
                self.cpp_info.libs = ['glfw']
                if self.settings.os == "Linux":
                    self.cpp_info.exelinkflags.append("-lrt -lm -ldl")
            else:
                self.cpp_info.libs = ['glfw3']
                if self.settings.os == "Macos":
                    self.cpp_info.exelinkflags.append("-framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo")
                if self.settings.os == "Linux":
                    self.cpp_info.libs.append("Xrandr Xrender Xi Xinerama Xcursor GL m dl drm Xdamage X11-xcb xcb-glx xcb-dri2 xcb-dri3 xcb-present xcb-sync Xxf86vm Xfixes Xext X11 pthread xcb Xau")
