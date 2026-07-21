import os
import sys

# Suppress harmless QtWebEngine/Chromium console noise (D3D11/HDR composition
# warnings, DNS config watch errors). --log-level=3 limits Chromium logging to
# FATAL only; the GUI and Plotly rendering are unaffected.
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-features=DnsOverHttps --log-level=3"

from Distributed_Design_Optimizer.postprocess.App import main

if __name__ == "__main__":
    sys.exit(main())
