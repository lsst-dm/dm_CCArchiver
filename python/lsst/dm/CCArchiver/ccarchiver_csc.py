# This file is part of dm_CCArchiver
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import logging
import pathlib
from lsst.dm.csc.base.archiver_csc import ArchiverCSC
from lsst.dm.CCArchiver.ccdirector import CCDirector
from lsst.ts import salobj

LOGGER = logging.getLogger(__name__)


class CCArchiverCSC(ArchiverCSC):
    """ CCArchiverCSC is a specialization of an Archiver CSC

    Parameters
    ----------
    index : `str`
    """

    def __init__(self):
        super().__init__("CCArchiver", initial_state=salobj.State.STANDBY)

        domain = salobj.Domain()

        # set up receiving SAL messages
        salobj.SalInfo(domain=domain, name="CCArchiver")

        # receive events from CCCamera
        camera_events = {'endReadout', 'startIntegration'}
        self.camera_remote = salobj.Remote(domain, "CCCamera", readonly=True, include=camera_events,
                                           evt_max_history=0)
        self.camera_remote.evt_endReadout.callback = self.endReadoutCallback
        self.camera_remote.evt_startIntegration.callback = self.startIntegrationCallback

        # receive events from CCHeaderService
        cchs_events = {'largeFileObjectAvailable'}
        self.cchs_remote = salobj.Remote(domain, "CCHeaderService",
                                         readonly=True, include=cchs_events,
                                         evt_max_history=0)
        self.cchs_remote.evt_largeFileObjectAvailable.callback = self.largeFileObjectAvailableCallback

        # set up message director for ComCam
        self.director = CCDirector(self, "CCArchiver", "ccarchiver_config.yaml", "CCArchiverCSC.log")
        self.director.configure()

        # used to indicate that the CSC is in the process of transitioning to the FAULT state so
        # that it happens once, and not multiple times.
        self.transitioning_to_fault_evt = asyncio.Event()
        self.transitioning_to_fault_evt.clear()

        self.current_state = None
        LOGGER.info("************************ Starting CCArchiver ************************")
