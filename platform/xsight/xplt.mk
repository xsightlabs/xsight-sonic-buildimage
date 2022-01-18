# Xsight xplt tools package for es9632x
# Currently we use the same deb for xx and xq boxes.
# TODO: bring and install the deb per box type.

# Add platform specific tools
XPLT_TOOLS = xplt_es9632xq_sonicnos-2.1.1-0-g4f5e42c_amd64.deb
$(XPLT_TOOLS)_URL = http://x-nexus:8081/repository/xplt-es9632x/deb/$(XPLT_TOOLS)
SONIC_ONLINE_DEBS += $(XPLT_TOOLS)
