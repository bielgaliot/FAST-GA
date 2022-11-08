#  This file is part of FAST-OAD_CS23 : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2022  ONERA & ISAE-SUPAERO
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

import openmdao.api as om
import fastoad.api as oad

from fastga.models.aerodynamics.constants import SUBMODEL_CL_Q_WING


@oad.RegisterSubmodel(
    SUBMODEL_CL_Q_WING, "fastga.submodel.aerodynamics.wing.cl_pitch_velocity.legacy"
)
class ComputeCLPitchVelocityWing(om.ExplicitComponent):
    """
    Computation of the contribution of the wing to the increase in lift due to a pitch velocity.
    The convention from :cite:`roskampart6:1985` are used, meaning that, for the derivative with
    respect to a pitch rate, this rate is made dimensionless by multiplying it by the MAC and
    dividing it by 2 times the airspeed.

    Based on :cite:`roskampart6:1985` section 10.2.7
    """

    def initialize(self):

        self.options.declare("low_speed_aero", default=False, types=bool)

    def setup(self):

        self.add_input("data:geometry:wing:aspect_ratio", val=np.nan)
        self.add_input("data:geometry:wing:sweep_25", val=np.nan, units="rad")
        self.add_input("data:geometry:wing:MAC:length", val=np.nan, units="m")
        self.add_input("data:geometry:wing:MAC:at25percent:x", val=np.nan, units="m")

        self.add_input("data:weight:aircraft:CG:aft:x", val=np.nan, units="m")
        self.add_input("data:weight:aircraft:CG:fwd:x", val=np.nan, units="m")

        if self.options["low_speed_aero"]:
            self.add_input("data:aerodynamics:wing:low_speed:CL_alpha", val=np.nan, units="rad**-1")
            self.add_input("data:aerodynamics:low_speed:mach", val=np.nan)

            self.add_output("data:aerodynamics:wing:low_speed:CL_q", units="rad**-1")

        else:
            self.add_input("data:aerodynamics:wing:cruise:CL_alpha", val=np.nan, units="rad**-1")
            self.add_input("data:aerodynamics:cruise:mach", val=np.nan)

            self.add_output("data:aerodynamics:wing:cruise:CL_q", units="rad**-1")

        self.declare_partials(of="*", wrt="*", method="exact")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        wing_ar = inputs["data:geometry:wing:aspect_ratio"]
        wing_sweep_25 = inputs["data:geometry:wing:sweep_25"]
        l0_wing = inputs["data:geometry:wing:MAC:length"]
        fa_length = inputs["data:geometry:wing:MAC:at25percent:x"]

        x_cg_fwd = inputs["data:weight:aircraft:CG:fwd:x"]
        x_cg_aft = inputs["data:weight:aircraft:CG:aft:x"]

        if self.options["low_speed_aero"]:
            cl_alpha_w = inputs["data:aerodynamics:wing:low_speed:CL_alpha"]
            mach = inputs["data:aerodynamics:low_speed:mach"]
        else:
            cl_alpha_w = inputs["data:aerodynamics:wing:cruise:CL_alpha"]
            mach = inputs["data:aerodynamics:cruise:mach"]

        # A CG position is necessary for the computation of this coefficient, we will thus assume
        # a CG between the two extremas
        x_cg_mid = (x_cg_fwd + x_cg_aft) / 2.0
        x_w = fa_length - x_cg_mid

        # At Mach number = 0.0
        cl_q_wing_0 = (0.5 + 2.0 * x_w / l0_wing) * cl_alpha_w

        b_coeff = np.sqrt(1.0 - mach ** 2.0 * np.cos(wing_sweep_25) ** 2.0)

        cl_q_wing = (
            (wing_ar + 2.0 * np.cos(wing_sweep_25))
            / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
            * cl_q_wing_0
        )

        if self.options["low_speed_aero"]:
            outputs["data:aerodynamics:wing:low_speed:CL_q"] = cl_q_wing
        else:
            outputs["data:aerodynamics:wing:cruise:CL_q"] = cl_q_wing

    def compute_partials(self, inputs, partials, discrete_inputs=None):

        wing_ar = inputs["data:geometry:wing:aspect_ratio"]
        wing_sweep_25 = inputs["data:geometry:wing:sweep_25"]
        l0_wing = inputs["data:geometry:wing:MAC:length"]
        fa_length = inputs["data:geometry:wing:MAC:at25percent:x"]

        x_cg_fwd = inputs["data:weight:aircraft:CG:fwd:x"]
        x_cg_aft = inputs["data:weight:aircraft:CG:aft:x"]

        if self.options["low_speed_aero"]:
            cl_alpha_w = inputs["data:aerodynamics:wing:low_speed:CL_alpha"]
            mach = inputs["data:aerodynamics:low_speed:mach"]
        else:
            cl_alpha_w = inputs["data:aerodynamics:wing:cruise:CL_alpha"]
            mach = inputs["data:aerodynamics:cruise:mach"]

        x_cg_mid = (x_cg_fwd + x_cg_aft) / 2.0
        x_w = fa_length - x_cg_mid

        # At Mach number = 0.0
        cl_q_wing_0 = (0.5 + 2.0 * x_w / l0_wing) * cl_alpha_w

        d_cl_wing_0_d_x_cg_aft = -cl_alpha_w / l0_wing
        d_cl_wing_0_d_x_cg_fwd = -cl_alpha_w / l0_wing
        d_cl_wing_0_d_fa_length = 2.0 / l0_wing * cl_alpha_w
        d_cl_wing_0_d_l0_wing = -2.0 * x_w / l0_wing ** 2.0 * cl_alpha_w

        b_coeff = np.sqrt(1.0 - mach ** 2.0 * np.cos(wing_sweep_25) ** 2.0)

        d_b_coeff_d_mach = (
            -2.0
            * mach
            * np.cos(wing_sweep_25) ** 2.0
            / (2.0 * np.sqrt(1.0 - mach ** 2.0 * np.cos(wing_sweep_25) ** 2.0))
        )
        d_b_coeff_d_sweep = (
            2.0
            * mach ** 2.0
            * np.cos(wing_sweep_25)
            * np.sin(wing_sweep_25)
            / (2.0 * np.sqrt(1.0 - mach ** 2.0 * np.cos(wing_sweep_25) ** 2.0))
        )

        if self.options["low_speed_aero"]:

            partials["data:aerodynamics:wing:low_speed:CL_q", "data:geometry:wing:aspect_ratio"] = (
                (1.0 - b_coeff)
                * 2.0
                * np.cos(wing_sweep_25)
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25)) ** 2.0
                * cl_q_wing_0
            )
            partials["data:aerodynamics:wing:low_speed:CL_q", "data:geometry:wing:sweep_25"] = (
                (
                    2.0 * wing_ar * np.sin(wing_sweep_25) * (1.0 - b_coeff)
                    - wing_ar * d_b_coeff_d_sweep * (wing_ar + 2.0 * np.cos(wing_sweep_25))
                )
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25)) ** 2.0
                * cl_q_wing_0
            )
            # We're mostly gonna be at sweep_25 = 0.0 so the derivative will be null when
            # computed explicitly but not with finite difference, was tested with a different
            # sweep_25 and it works
            partials["data:aerodynamics:wing:low_speed:CL_q", "data:geometry:wing:MAC:length"] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_l0_wing
            )
            partials[
                "data:aerodynamics:wing:low_speed:CL_q", "data:geometry:wing:MAC:at25percent:x"
            ] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_fa_length
            )
            partials["data:aerodynamics:wing:low_speed:CL_q", "data:weight:aircraft:CG:fwd:x"] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_x_cg_fwd
            )
            partials["data:aerodynamics:wing:low_speed:CL_q", "data:weight:aircraft:CG:aft:x"] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_x_cg_aft
            )
            partials[
                "data:aerodynamics:wing:low_speed:CL_q", "data:aerodynamics:wing:low_speed:CL_alpha"
            ] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * (0.5 + 2.0 * x_w / l0_wing)
            )
            partials[
                "data:aerodynamics:wing:low_speed:CL_q", "data:aerodynamics:low_speed:mach"
            ] = (
                -wing_ar
                * (wing_ar + 2.0 * np.cos(wing_sweep_25))
                * cl_q_wing_0
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25)) ** 2.0
            ) * d_b_coeff_d_mach
        else:

            partials["data:aerodynamics:wing:cruise:CL_q", "data:geometry:wing:aspect_ratio"] = (
                (1.0 - b_coeff)
                * 2.0
                * np.cos(wing_sweep_25)
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25)) ** 2.0
                * cl_q_wing_0
            )
            partials["data:aerodynamics:wing:cruise:CL_q", "data:geometry:wing:sweep_25"] = (
                (
                    2.0 * wing_ar * np.sin(wing_sweep_25) * (1.0 - b_coeff)
                    - wing_ar * d_b_coeff_d_sweep * (wing_ar + 2.0 * np.cos(wing_sweep_25))
                )
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25)) ** 2.0
                * cl_q_wing_0
            )
            partials["data:aerodynamics:wing:cruise:CL_q", "data:geometry:wing:MAC:length"] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_l0_wing
            )
            partials[
                "data:aerodynamics:wing:cruise:CL_q", "data:geometry:wing:MAC:at25percent:x"
            ] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_fa_length
            )
            partials["data:aerodynamics:wing:cruise:CL_q", "data:weight:aircraft:CG:fwd:x"] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_x_cg_fwd
            )
            partials["data:aerodynamics:wing:cruise:CL_q", "data:weight:aircraft:CG:aft:x"] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * d_cl_wing_0_d_x_cg_aft
            )
            partials[
                "data:aerodynamics:wing:cruise:CL_q", "data:aerodynamics:wing:cruise:CL_alpha"
            ] = (
                (wing_ar + 2.0 * np.cos(wing_sweep_25))
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25))
                * (0.5 + 2.0 * x_w / l0_wing)
            )
            partials["data:aerodynamics:wing:cruise:CL_q", "data:aerodynamics:cruise:mach"] = (
                -wing_ar
                * (wing_ar + 2.0 * np.cos(wing_sweep_25))
                * cl_q_wing_0
                / (wing_ar * b_coeff + 2.0 * np.cos(wing_sweep_25)) ** 2.0
            ) * d_b_coeff_d_mach
