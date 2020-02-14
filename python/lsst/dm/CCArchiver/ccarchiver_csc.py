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
from lsst.dm.CCArchiver.atdirector import CCDirector
from lsst.ts import salobj
from lsst.ts.salobj import State

LOGGER = logging.getLogger(__name__)


class CCArchiverCSC(ArchiverCSC):

    def __init__(self, schema_file, index, config_dir=None, initial_state=salobj.State.STANDBY,
                 initial_simulation_mode=0):
        schema_path = pathlib.Path(__file__).resolve().parents[4].joinpath("schema", schema_file)
        super().__init__("CCArchiver", index=index, schema_path=schema_path,
                         config_dir=config_dir, initial_state=initial_state,
                         initial_simulation_mode=initial_simulation_mode)

        domain = salobj.Domain()

        salinfo = salobj.SalInfo(domain=domain, name="CCArchiver", index=0)

        camera_events = {'endReadout', 'startIntegration'}
        self.camera_remote = salobj.Remote(domain, "CCCamera", index=0, readonly=True, include=camera_events,
                                           evt_max_history=0)
        self.camera_remote.evt_endReadout.callback = self.endReadoutCallback
        self.camera_remote.evt_startIntegration.callback = self.startIntegrationCallback

        efd_events = {'largeFileObjectAvailable'}
        self.efd_remote = salobj.Remote(domain, "EFD", index=0, readonly=True, include=efd_events,
                                        evt_max_history=0)
        self.efd_remote.evt_largeFileObjectAvailable.callback = self.largeFileObjectAvailableCallback

        self.director = CCDirector(self, "CCArchiver", "atarchiver_config.yaml", "CCArchiverCSC.log")
        self.director.configure()

        self.transitioning_to_fault_evt = asyncio.Event()
        self.transitioning_to_fault_evt.clear()

        self.current_state = None
        LOGGER.info("************************ Starting CCArchiver ************************")
