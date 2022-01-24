# Xsight xplt tools package for es9632x
# Currently we use the same deb for xx and xq boxes.
# TODO: bring and install the deb per box type.

# Add platform specific tools
XPLT_VERSION=2.1.1-0-g4f5e42c
XPLT_TOOLS = xplt_es9632xq_sonicnos-$(XPLT_VERSION)_amd64.deb
XPLT_TOOLS_URL = http://x-nexus:8081/repository/xplt-es9632x/deb/$(XPLT_TOOLS)

export XPLT_TOOLS_URL
