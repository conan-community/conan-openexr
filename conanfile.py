from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class OpenEXRConan(ConanFile):
    name = "openexr"
    description = "OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & Magic for use in computer imaging applications."
    version = "2.3.0"
    license = "BSD"
    url = "https://github.com/jgsogo/conan-openexr.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "namespace_versioning": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "namespace_versioning=True", "fPIC=True"
    generators = "cmake"
    exports = "FindOpenEXR.cmake"

    requires = "ilmbase/{version}@jgsogo/stable".format(version=version),

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if "fPIC" in self.options.fields and self.options.shared:
            self.options.fPIC = True

    def source(self):
        url = "https://github.com/openexr/openexr/releases/download/v{version}/openexr-{version}.tar.gz"
        tools.get(url.format(version=self.version))
        tools.replace_in_file("openexr-%s/CMakeLists.txt" % self.version, "PROJECT (openexr)",
                              """PROJECT (openexr)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()""")

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["OPENEXR_ENABLE_TESTS"] = False
        cmake.definitions["OPENEXR_NAMESPACE_VERSIONING"] = self.options.namespace_versioning
        if "fPIC" in self.options.fields:
            cmake.definitions["CMAKE_POSITION_INDEPENDENT_CODE"] = self.options.fPIC

        cmake.definitions["OPENEXR_BUILD_PYTHON_LIBS"] = False
        cmake.definitions["OPENEXR_BUILD_VIEWERS"] = False
        cmake.definitions["OPENEXR_BUILD_ILMBASE"] = False
        cmake.definitions["OPENEXR_BUILD_SHARED"] = self.options.shared
        cmake.definitions["OPENEXR_BUILD_STATIC"] = not bool(self.options.shared)

        # Use dependencies from Conan
        cmake.definitions["ILMBASE_PACKAGE_PREFIX"] = self.deps_cpp_info["ilmbase"].rootpath

        src_dir = "openexr-%s" % self.version
        cmake.configure(source_dir=src_dir)
        return cmake

    def build(self):
        yes_no = {True: "enable", False: "disable"}
        args = ["--{}-shared".format(yes_no.get(bool(self.options.shared))),
                "--{}-static".format(yes_no.get(not bool(self.options.shared))),
                "--{}-namespaceversioning".format(yes_no.get(bool(self.options.namespace_versioning))),
                ]

        autotools = AutoToolsBuildEnvironment(self)
        autotools.configure(configure_dir='openexr-{}'.format(self.version), args=args)
        autotools.make()
        tools.replace_prefix_in_pc_file("OpenEXR.pc", "${package_root_path_openexr}")

    def package(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.install()
        self.copy("FindOpenEXR.cmake", src=".", dst=".")
        self.copy("license*", dst="licenses", src="ilmbase-%s" % self.version, ignore_case=True, keep_path=False)


    def package_info(self):
        self.cpp_info.includedirs = [os.path.join('include', 'OpenEXR'), ]
        self.cpp_info.libs = ['Half', 'Iex', 'IexMath', 'IlmThread', 'Imath']

        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")

        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]
