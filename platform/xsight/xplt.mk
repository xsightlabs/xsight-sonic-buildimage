# Xsight xplt tools package for es9632x
# Currently we use the same deb for xx and xq boxes.
# TODO: bring and install the deb per box type.

# Add platform specific tools
XPLT_VERSION=3.0.0-1-g31a6f59

XPLT_TOOLS = xplt_es9632xq_sonicnos-$(XPLT_VERSION)_amd64.deb
$(XPLT_TOOLS)_URL = "http://172.20.4.62:8081/repository/xplt-es9632x/deb/"$(XPLT_TOOLS)
SONIC_ONLINE_DEBS += $(XPLT_TOOLS)
