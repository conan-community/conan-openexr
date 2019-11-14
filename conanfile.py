from conans import ConanFile, CMake, tools
import os


class OpenEXRConan(ConanFile):
    name = "openexr"
    description = "OpenEXR is a high dynamic-range (HDR) image file format developed by Industrial Light & " \
                  "Magic for use in computer imaging applications."
    version = "2.3.0"
    license = "BSD"
    url = "https://github.com/jgsogo/conan-openexr.git"

    alias = "openexr/2.3.0"

    def configure(self):
        self.output.warn("[DEPRECATED] Package openexr/bincrafters is being deprecated. Change yours to require openexr/2.3.0@ instead")

