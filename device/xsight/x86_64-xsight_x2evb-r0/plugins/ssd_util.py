#
# ssd_util.py
#
# Platfrom specific implementation of the SSD health API
#

try:
    from sonic_platform_base.sonic_ssd.ssd_generic import SsdUtil
except ImportError as e:
    raise ImportError (str(e) + "- required module not found")

class SsdUtil(SsdUtil):
    """
    Platfrom specific implementation of the SSD health API
    """
    def _parse_vendor(self):
        model_short = self.model.split()[0]
        if self.model.startswith('M.2'):
            return 'Generic'
        elif model_short in self.vendor_ssd_utility:
            return model_short
        else:
            return None
