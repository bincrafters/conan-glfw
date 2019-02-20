#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import glob
from conans import ConanFile, CMake, tools


class GlfwConan(ConanFile):
    name = "glfw"
    version = "3.2.1.20180327"
    description = "The GLFW library - Builds on Windows, Linux and Macos/OSX"
    settings = "os", "arch", "build_type", "compiler"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {'shared': False, "fPIC": True}
    license = "Zlib"
    url = "https://github.com/bincrafters/conan-glfw"
    homepage = "https://github.com/glfw/glfw"
    author = "Bincrafters <bincrafters@gmail.com>"
    topics = ("conan", "gflw", "opengl", "vulcan", "opengl-es")
    exports = "LICENSE"
    exports_sources = "CMakeLists.txt"
    generators = "cmake"
    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def system_requirements(self):
        if tools.os_info.is_linux:
            if tools.os_info.with_apt:
                installer = tools.SystemPackageTool()
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
            elif tools.os_info.with_yum:
                installer = tools.SystemPackageTool()
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
            elif tools.os_info.with_pacman:
                if self.settings.arch == "x86" and tools.detected_architecture() == "x86_64":
                    # Note: The packages with the "lib32-" prefix will only be
                    # available if the user has activate Arch's multilib
                    # repository, See
                    # https://wiki.archlinux.org/index.php/official_repositories#multilib
                    arch_suffix = 'lib32-'
                else:
                    arch_suffix = ''
                installer = tools.SystemPackageTool()
                installer.install("%s%s" % (arch_suffix, "libx11"))
                installer.install("%s%s" % (arch_suffix, "libxrandr"))
                installer.install("%s%s" % (arch_suffix, "libxinerama"))
                installer.install("%s%s" % (arch_suffix, "libxcursor"))
                installer.install("%s%s" % (arch_suffix, "libxi"))
                installer.install("%s%s" % (arch_suffix, "libglvnd"))

            else:
                self.output.warn("Could not determine package manager, skipping Linux system requirements installation.")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "6a49afdeb0ae8f0d6b198f321422d2c75676f7efcff28ea9b8e45ac5c68c6d4a"
        revision = "0a3c4f5d80b041ee1a12c8da3503653d98bd1a15"
        tools.get("{}/archive/{}.zip".format(self.homepage, revision), sha256=sha256)
        extracted_folder = self.name + '-' + revision
        os.rename(extracted_folder, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["GLFW_BUILD_EXAMPLES"] = False
        cmake.definitions["GLFW_BUILD_TESTS"] = False
        cmake.definitions["GLFW_BUILD_DOCS"] = False
        cmake.configure(build_dir=self._build_subfolder)
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

        if self.settings.os == "Macos" and self.options.shared:
            with tools.chdir(os.path.join(self._source_subfolder, 'src')):
                for filename in glob.glob('*.dylib'):
                    self.run('install_name_tool -id {filename} {filename}'.format(filename=filename))

    def package(self):
        self.copy("COPYING.txt", dst="licenses", src=self._source_subfolder)
        self.copy(pattern="*.pdb", dst="bin", keep_path=False)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.extend(['Xrandr', 'Xrender', 'Xi', 'Xinerama', 'Xcursor', 'GL', 'm', 'dl', 'drm', 'Xdamage', 'X11-xcb', 'xcb-glx', 'xcb-dri2', 'xcb-dri3', 'xcb-present', 'xcb-sync', 'Xxf86vm', 'Xfixes', 'Xext', 'X11', 'pthread', 'xcb', 'Xau'])
            if self.options.shared:
                self.cpp_info.exelinkflags.append("-lrt -lm -ldl")
        elif self.settings.os == "Macos":
            self.cpp_info.exelinkflags.append("-framework OpenGL -framework Cocoa -framework IOKit -framework CoreVideo")
