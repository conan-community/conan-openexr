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

    requires = "ilmbase/{version}@jgsogo/stable".format(version=version)

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.remove("fPIC")

    def configure(self):
        if "fPIC" in self.options.fields and self.options.shared:
            self.options.fPIC = True

    def source(self):
        url = "https://github.com/openexr/openexr/releases/download/v{version}/openexr-{version}.tar.gz"
        tools.get(url.format(version=self.version))

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
        self.cpp_info.libs = ['IlmImf', 'IlmImfUtil']

        if self.options.shared and self.settings.os == "Windows":
            self.cpp_info.defines.append("OPENEXR_DLL")

        if not self.settings.os == "Windows":
            self.cpp_info.cppflags = ["-pthread"]
