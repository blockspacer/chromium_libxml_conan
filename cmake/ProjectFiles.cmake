include_guard( DIRECTORY )

# if (current_cpu == "x86" || current_cpu == "x64")
if(TARGET_EMSCRIPTEN)
  # skip
elseif(TARGET_LINUX)
  if(CMAKE_CL_64)
    #
  else(CMAKE_CL_64)
    # TODO:
    #list(APPEND libxml_SOURCES
    #  ${libxml_DIR}intel/filter_sse2_intrinsics.c
    #  ${libxml_DIR}intel/intel_init.c
    #)
  endif(CMAKE_CL_64)
elseif(TARGET_WINDOWS) # TODO
  if(CMAKE_CL_64)
    #
  else(CMAKE_CL_64)
    # TODO:
    #list(APPEND libxml_SOURCES
    #  ${libxml_DIR}intel/filter_sse2_intrinsics.c
    #  ${libxml_DIR}intel/intel_init.c
    #)
  endif(CMAKE_CL_64)
else()
  message(FATAL_ERROR "platform not supported")
endif()

if(LIBXML2_WITH_SAX1)
  message(FATAL_ERROR "TODO: LIBXML2_WITH_SAX1 not supported")
	#list(APPEND libxml_SOURCES 
  #  "src/DOCBparser.c")
endif()

if(LIBXML2_WITH_TRIO)
  #"src/triodef.h"
  #"src/trionan.h"
  #"src/trio.c"
  #"src/trio.h"
  #"src/triodef.h"
  # Note: xpath.c #includes trionan.c
  #"src/trionan.c"
  #"src/triop.h"
  #"src/triostr.c"
  #"src/triostr.h"
	list(APPEND libxml_SOURCES 
    "src/trio.c" 
    "src/triostr.c")
endif()

list(APPEND libxml_SOURCES
  "src/HTMLparser.c"
  "src/HTMLtree.c"

  #"src/SAX.c"
  "src/SAX2.c"
  "src/buf.c"
  "src/buf.h"

  #"src/c14n.c"
  #"src/catalog.c"
  "src/chvalid.c"

  #"src/debugXML.c"
  "src/dict.c"
  "src/elfgcchack.h"
  "src/enc.h"
  "src/encoding.c"
  "src/entities.c"
  "src/error.c"
  "src/globals.c"
  "src/hash.c"
  "src/include/libxml/DOCBparser.h"
  "src/include/libxml/HTMLparser.h"
  "src/include/libxml/HTMLtree.h"
  "src/include/libxml/SAX.h"
  "src/include/libxml/SAX2.h"
  "src/include/libxml/c14n.h"
  "src/include/libxml/catalog.h"
  "src/include/libxml/chvalid.h"
  "src/include/libxml/debugXML.h"
  "src/include/libxml/dict.h"
  "src/include/libxml/encoding.h"
  "src/include/libxml/entities.h"
  "src/include/libxml/globals.h"
  "src/include/libxml/hash.h"
  "src/include/libxml/list.h"
  "src/include/libxml/nanoftp.h"
  "src/include/libxml/nanohttp.h"
  "src/include/libxml/parser.h"
  "src/include/libxml/parserInternals.h"
  "src/include/libxml/pattern.h"
  "src/include/libxml/relaxng.h"
  "src/include/libxml/schemasInternals.h"
  "src/include/libxml/schematron.h"
  "src/include/libxml/threads.h"
  "src/include/libxml/tree.h"
  "src/include/libxml/uri.h"
  "src/include/libxml/valid.h"
  "src/include/libxml/xinclude.h"
  "src/include/libxml/xlink.h"
  "src/include/libxml/xmlIO.h"
  "src/include/libxml/xmlautomata.h"
  "src/include/libxml/xmlerror.h"
  "src/include/libxml/xmlexports.h"
  "src/include/libxml/xmlmemory.h"
  "src/include/libxml/xmlmodule.h"
  "src/include/libxml/xmlreader.h"
  "src/include/libxml/xmlregexp.h"
  "src/include/libxml/xmlsave.h"
  "src/include/libxml/xmlschemas.h"
  "src/include/libxml/xmlschemastypes.h"
  "src/include/libxml/xmlstring.h"
  "src/include/libxml/xmlunicode.h"
  "src/include/libxml/xmlwriter.h"
  "src/include/libxml/xpath.h"
  "src/include/libxml/xpathInternals.h"
  "src/include/libxml/xpointer.h"

  #"src/legacy.c"
  "src/libxml.h"
  "src/list.c"
  "src/parser.c"
  "src/parserInternals.c"
  "src/pattern.c"

  #"src/relaxng.c"
  "src/save.h"

  #"src/schematron.c"
  "src/threads.c"
  "src/timsort.h"
  "src/tree.c"
  "src/uri.c"
  "src/valid.c"

  #"src/xinclude.c"
  #"src/xlink.c"
  "src/xmlIO.c"
  "src/xmlmemory.c"

  #"src/xmlmodule.c"
  "src/xmlreader.c"

  #"src/xmlregexp.c"
  "src/xmlsave.c"

  #"src/xmlschemas.c"
  #"src/xmlschemastypes.c"
  "src/xmlstring.c"
  "src/xmlunicode.c"
  "src/xmlwriter.c"
  "src/xpath.c"

  #"src/xpointer.c"
  #"src/xzlib.c"
  "src/xzlib.h"
)

# static_library("xml_reader")
list(APPEND libxml_SOURCES
  "chromium/xml_reader.cc"
  "chromium/xml_reader.h"
)

# static_library("xml_writer")
list(APPEND libxml_SOURCES
  "chromium/xml_writer.cc"
  "chromium/xml_writer.h"
)

# static_library("libxml_utils")
list(APPEND libxml_SOURCES
  "chromium/libxml_utils.cc"
  "chromium/libxml_utils.h"
)

# TODO
#if(WIN32)
#	list(APPEND libxml_SOURCES "win32/libxml2.rc")
#	file(
#		WRITE
#		${CMAKE_CURRENT_BINARY_DIR}/rcVersion.h
#		"#define LIBXML_MAJOR_VERSION ${LIBXML_MAJOR_VERSION}\n"
#		"#define LIBXML_MINOR_VERSION ${LIBXML_MINOR_VERSION}\n"
#		"#define LIBXML_MICRO_VERSION ${LIBXML_MICRO_VERSION}\n"
#		"#define LIBXML_DOTTED_VERSION \"${VERSION}\"\n"
#	)
#endif()

list(TRANSFORM libxml_SOURCES PREPEND "${libxml_DIR}")
