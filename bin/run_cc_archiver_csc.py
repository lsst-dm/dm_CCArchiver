#!/usr/bin/env python
import asyncio
from lsst.dm.CCArchiver.ccarchiver_csc import CCArchiverCSC


asyncio.run(CCArchiverCSC.amain(index=None))
