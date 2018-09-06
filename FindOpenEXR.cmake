
set(OPENEXR_ROOT ${CONAN_OPENEXR_ROOT} CACHE PATH "Path to OpenEXR root path")

# Find include dirs
find_path(OPENEXR_INCLUDE_DIRS
	NAMES OpenEXRConfig.h
	HINTS ${OPENEXR_ROOT}/include ${OPENEXR_ROOT}/include/OpenEXR
)

# Look for libraries
foreach(LIBNAME IlmImf IlmImfUtil)
	find_library(OPENEXR_${LIBNAME}_LIBRARY
		NAMES ${LIBNAME}
        HINTS ${OPENEXR_ROOT}/lib
        PATH_SUFFIXES lib
        )
endforeach()

# Check version
file(STRINGS ${OPENEXR_INCLUDE_DIRS}/OpenEXRConfig.h TMP REGEX "#define OPENEXR_VERSION_STRING.*$")
string(REGEX MATCHALL "[0-9.]+" OPENEXR_VERSION ${TMP})

# handle the QUIETLY and REQUIRED arguments and set xxx_FOUND to TRUE
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(OpenEXR
    REQUIRED_VARS
        OPENEXR_INCLUDE_DIRS
        OPENEXR_IlmImf_LIBRARY
        OPENEXR_IlmImfUtil_LIBRARY
    VERSION_VAR
        OPENEXR_VERSION
)


# Create imported targets
if(OPENEXR_FOUND)
    # TODO: Create imported targets (CMake version?)
    set(OPENEXR_LIBRARIES ${CONAN_LIBS_OPENEXR} ${CONAN_LIBS_ILMBASE})
endif()


mark_as_advanced(MYPACKAGE_LIBRARY
    OPENEXR_IlmImf_LIBRARY
    OPENEXR_IlmImfUtil_LIBRARY
    )

if(OPENEXR_FOUND)
	mark_as_advanced(OPENEXR_ROOT)
endif()
