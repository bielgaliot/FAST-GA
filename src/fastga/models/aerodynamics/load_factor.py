"""
    FAST - Copyright (c) 2016 ONERA ISAE
"""

#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
from .external.openvsp.compute_vn import DOMAIN_PTS_NB

from openmdao.core.group import Group
from openmdao.core.explicitcomponent import ExplicitComponent

from .external.vlm.compute_vn import ComputeVNvlmNoVH
from .external.openvsp.compute_vn import ComputeVNopenvspNoVH

from fastoad.module_management.service_registry import RegisterOpenMDAOSystem
from fastoad.module_management.constants import ModelDomain


@RegisterOpenMDAOSystem("fastga.aerodynamics.load_factor", domain=ModelDomain.AERODYNAMICS)
class LoadFactor(Group):
    """
    Models for computing the loads and characteristic speed and load factor of the aircraft
    """

    def initialize(self):
        self.options.declare("propulsion_id", default="", types=str)
        self.options.declare("compute_cl_alpha", default=False, types=bool)
        self.options.declare("use_openvsp", default=False, types=bool)

    def setup(self):
        if not (self.options["use_openvsp"]):
            self.add_subsystem("vn_vlm",
                               ComputeVNvlmNoVH(
                                   propulsion_id=self.options["propulsion_id"],
                                   compute_cl_alpha=self.options["compute_cl_alpha"]
                               ),
                               promotes=["*"],
                               )
        else:
            self.add_subsystem("vn_openvsp",
                               ComputeVNopenvspNoVH(
                                   propulsion_id=self.options["propulsion_id"],
                                   compute_cl_alpha=self.options["compute_cl_alpha"]
                               ),
                               promotes=["*"],
                               )
        self.add_subsystem("sizing_load_factor",
                           _LoadFactorIdentification(),
                           promotes=["*"])


class _LoadFactorIdentification(ExplicitComponent):

    def setup(self):
        nan_array = np.full(DOMAIN_PTS_NB, np.nan)
        self.add_input("data:flight_domain:load_factor", val=nan_array, shape=DOMAIN_PTS_NB)

        self.add_output("data:mission:sizing:cs23:sizing_factor_ultimate")

        self.declare_partials("*", "*", method="fd")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        load_factor_array = inputs["data:flight_domain:load_factor"]
        outputs["data:mission:sizing:cs23:sizing_factor_ultimate"] = 1.5 * max(
            abs(max(load_factor_array)), abs(min(load_factor_array))
        )
