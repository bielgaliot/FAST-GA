"""
Test module for OpenMDAO versions of basicICEngine.
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
import openmdao.api as om
from fastoad.constants import EngineSetting

from ..openmdao import OMBasicICEngineComponent

from tests.testing_utilities import run_system

THRUST_SL = np.array(
    [
        165.55463516,
        363.74098297,
        561.92733079,
        760.11367861,
        958.30002643,
        1156.48637424,
        1354.67272206,
        1552.85906988,
        1751.04541769,
        1949.23176551,
        2147.41811333,
        2345.60446114,
        2543.79080896,
        2741.97715678,
        2940.16350459,
        3138.34985241,
        3336.53620023,
        3534.72254804,
        3732.90889586,
        3931.09524368,
        4129.2815915,
        4327.46793931,
        4525.65428713,
        4723.84063495,
        4922.02698276,
        5120.21333058,
        5318.3996784,
        5516.58602621,
        5714.77237403,
        5912.95872185,
    ]
)
THRUST_SL_LIMIT = np.array(
    [
        3992.47453905,
        4354.01018556,
        4627.19987747,
        4851.0636332,
        5044.6557686,
        5220.57194688,
        5390.01724447,
        5560.09096074,
        5735.92640037,
        5912.95872185,
    ]
)
SPEED = np.array(
    [
        5.0,
        15.69362963,
        26.38725926,
        37.08088889,
        47.77451852,
        58.46814815,
        69.16177778,
        79.85540741,
        90.54903704,
        101.24266667,
    ]
)
EFFICIENCY_SL = np.array(
    [
        [
            0.10624897,
            0.18013462,
            0.21651981,
            0.22807006,
            0.22721517,
            0.22083446,
            0.21221014,
            0.20288339,
            0.19375159,
            0.18521768,
            0.17695007,
            0.16861719,
            0.16072916,
            0.15320241,
            0.14590992,
            0.13921122,
            0.1334496,
            0.12795466,
            0.12241574,
            0.11577645,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
            0.11271665,
        ],
        [
            0.27467896,
            0.4344713,
            0.50019948,
            0.52210089,
            0.52331264,
            0.51450441,
            0.50108722,
            0.48583145,
            0.47029896,
            0.45541008,
            0.44104008,
            0.42584508,
            0.41088675,
            0.3965363,
            0.3823869,
            0.36810154,
            0.35501908,
            0.34370124,
            0.33279269,
            0.32200437,
            0.31026176,
            0.29307527,
            0.28733591,
            0.28733591,
            0.28733591,
            0.28733591,
            0.28733591,
            0.28733591,
            0.28733591,
            0.28733591,
        ],
        [
            0.39000222,
            0.57044741,
            0.63699228,
            0.66146452,
            0.66549523,
            0.66001213,
            0.64930646,
            0.63598725,
            0.62156858,
            0.60764123,
            0.59469412,
            0.57995927,
            0.56458934,
            0.54967715,
            0.53514192,
            0.52045092,
            0.50471251,
            0.49125795,
            0.47913675,
            0.46718454,
            0.45538279,
            0.44289265,
            0.42604793,
            0.40954706,
            0.40954706,
            0.40954706,
            0.40954706,
            0.40954706,
            0.40954706,
            0.40954706,
        ],
        [
            0.45696153,
            0.63245969,
            0.69803342,
            0.72446018,
            0.73281662,
            0.73178886,
            0.72538282,
            0.71598956,
            0.70509116,
            0.69372407,
            0.6836798,
            0.67181609,
            0.65838315,
            0.64512732,
            0.63194556,
            0.61905296,
            0.60503622,
            0.59093406,
            0.57890255,
            0.56763984,
            0.55636957,
            0.54503321,
            0.53306416,
            0.51715615,
            0.49662567,
            0.49662567,
            0.49662567,
            0.49662567,
            0.49662567,
            0.49662567,
        ],
        [
            0.47572647,
            0.65142816,
            0.71998696,
            0.75036676,
            0.76306201,
            0.76643601,
            0.76440373,
            0.75915986,
            0.75198267,
            0.74433328,
            0.73669419,
            0.72755218,
            0.71693665,
            0.7058908,
            0.69470578,
            0.68367562,
            0.67205808,
            0.65958055,
            0.64809168,
            0.63756928,
            0.627485,
            0.61741439,
            0.60709627,
            0.59588947,
            0.58106966,
            0.56259329,
            0.56259329,
            0.56259329,
            0.56259329,
            0.56259329,
        ],
        [
            0.46755441,
            0.64686877,
            0.72044175,
            0.7562094,
            0.77394705,
            0.78185907,
            0.78396766,
            0.78252236,
            0.77890522,
            0.77465356,
            0.76942822,
            0.76247608,
            0.7543838,
            0.74564022,
            0.7366293,
            0.72748983,
            0.71776748,
            0.70736368,
            0.69732461,
            0.68787651,
            0.67878305,
            0.66980521,
            0.66084096,
            0.65160745,
            0.64117342,
            0.62731614,
            0.61203777,
            0.61203777,
            0.61203777,
            0.61203777,
        ],
        [
            0.44964411,
            0.62979713,
            0.71092595,
            0.75259286,
            0.77515639,
            0.78705554,
            0.79282371,
            0.79475707,
            0.79457721,
            0.7930026,
            0.7898828,
            0.78503361,
            0.77907539,
            0.77244989,
            0.76540475,
            0.75804781,
            0.75010758,
            0.74151402,
            0.73300844,
            0.72486176,
            0.71688625,
            0.70899465,
            0.70108463,
            0.69306823,
            0.68471333,
            0.67504824,
            0.66188233,
            0.64998888,
            0.64998888,
            0.64998888,
        ],
        [
            0.41597783,
            0.6106596,
            0.69887042,
            0.74406057,
            0.77069263,
            0.78662226,
            0.79581753,
            0.80082936,
            0.80345225,
            0.80415093,
            0.8028508,
            0.79994596,
            0.79585717,
            0.79108738,
            0.78578353,
            0.77999311,
            0.77361158,
            0.76666696,
            0.75959304,
            0.75263267,
            0.74580499,
            0.73897916,
            0.73207307,
            0.72509322,
            0.71792275,
            0.71028881,
            0.70132514,
            0.68838938,
            0.67973214,
            0.67973214,
        ],
        [
            0.39388674,
            0.59361286,
            0.68254224,
            0.73406677,
            0.76407991,
            0.78323456,
            0.79552201,
            0.80329205,
            0.80823338,
            0.81082741,
            0.81117791,
            0.80987937,
            0.80751355,
            0.80434656,
            0.80055104,
            0.79619451,
            0.79120453,
            0.78566054,
            0.77985385,
            0.77403874,
            0.76825303,
            0.76237137,
            0.75641685,
            0.7503678,
            0.74418538,
            0.73774801,
            0.73069332,
            0.72233462,
            0.70917405,
            0.70352754,
        ],
        [
            0.37986866,
            0.57166131,
            0.66845157,
            0.72246303,
            0.75663953,
            0.77839387,
            0.79349744,
            0.80353619,
            0.81049222,
            0.81452268,
            0.81642655,
            0.81673453,
            0.81581215,
            0.81398968,
            0.81151883,
            0.80843284,
            0.80466699,
            0.80034478,
            0.79568565,
            0.79085532,
            0.78600398,
            0.78104705,
            0.77593328,
            0.77067985,
            0.76533983,
            0.759812,
            0.75399333,
            0.74748603,
            0.73970246,
            0.72610238,
        ],
    ]
)

THRUST_CL = np.array(
    [
        130.02473826,
        286.71392915,
        443.40312004,
        600.09231092,
        756.78150181,
        913.47069269,
        1070.15988358,
        1226.84907447,
        1383.53826535,
        1540.22745624,
        1696.91664713,
        1853.60583801,
        2010.2950289,
        2166.98421978,
        2323.67341067,
        2480.36260156,
        2637.05179244,
        2793.74098333,
        2950.43017421,
        3107.1193651,
        3263.80855599,
        3420.49774687,
        3577.18693776,
        3733.87612864,
        3890.56531953,
        4047.25451042,
        4203.9437013,
        4360.63289219,
        4517.32208307,
        4674.01127396,
    ]
)
THRUST_CL_LIMIT = np.array(
    [
        3143.48677725,
        3428.45974096,
        3644.13600906,
        3821.24591387,
        3974.64021074,
        4114.38712534,
        4249.22691158,
        4384.69046768,
        4524.95060164,
        4674.01127396,
    ]
)
EFFICIENCY_CL = np.array(
    [
        [
            0.10608816,
            0.18034658,
            0.21668281,
            0.22807476,
            0.22706235,
            0.22055878,
            0.21184539,
            0.20245902,
            0.19328207,
            0.1847079,
            0.17642882,
            0.16809556,
            0.16020603,
            0.15268613,
            0.145397,
            0.13871568,
            0.13296437,
            0.12745844,
            0.12187893,
            0.11501007,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
            0.11261989,
        ],
        [
            0.27437851,
            0.43483937,
            0.50046579,
            0.52210109,
            0.5230512,
            0.51403102,
            0.50044969,
            0.48506752,
            0.46943296,
            0.45444031,
            0.44001314,
            0.42481021,
            0.40983547,
            0.39547941,
            0.38130631,
            0.36702687,
            0.35398164,
            0.3426632,
            0.33173048,
            0.32089245,
            0.30894696,
            0.29021217,
            0.28715199,
            0.28715199,
            0.28715199,
            0.28715199,
            0.28715199,
            0.28715199,
            0.28715199,
            0.28715199,
        ],
        [
            0.38955417,
            0.57085698,
            0.63719913,
            0.66140144,
            0.66521047,
            0.65951903,
            0.64865822,
            0.63520988,
            0.62067866,
            0.60662068,
            0.59357506,
            0.57882788,
            0.56343443,
            0.54851317,
            0.53395338,
            0.51923439,
            0.50350864,
            0.49005808,
            0.47792195,
            0.46594175,
            0.45409059,
            0.44139855,
            0.42397755,
            0.40932274,
            0.40932274,
            0.40932274,
            0.40932274,
            0.40932274,
            0.40932274,
            0.40932274,
        ],
        [
            0.45561907,
            0.63276693,
            0.69812978,
            0.72431866,
            0.73248072,
            0.73128936,
            0.72476624,
            0.71525397,
            0.7042555,
            0.69273891,
            0.68260341,
            0.67074194,
            0.65728513,
            0.64400762,
            0.6308024,
            0.61789298,
            0.60385179,
            0.58971891,
            0.57769924,
            0.56641794,
            0.55510551,
            0.54372095,
            0.53160721,
            0.51513089,
            0.49638912,
            0.49638912,
            0.49638912,
            0.49638912,
            0.49638912,
            0.49638912,
        ],
        [
            0.47585855,
            0.65158176,
            0.71994647,
            0.75014468,
            0.76268261,
            0.76592657,
            0.76379348,
            0.7584549,
            0.7511925,
            0.74336715,
            0.73568604,
            0.72656528,
            0.71592465,
            0.70486546,
            0.6936497,
            0.68259358,
            0.670996,
            0.65846917,
            0.64695721,
            0.6364223,
            0.62631211,
            0.61620639,
            0.60583408,
            0.59445407,
            0.57916424,
            0.56234249,
            0.56234249,
            0.56234249,
            0.56234249,
            0.56234249,
        ],
        [
            0.46767189,
            0.64593106,
            0.71993781,
            0.75574295,
            0.77343038,
            0.78128505,
            0.78332623,
            0.7818116,
            0.77808668,
            0.7737207,
            0.7684629,
            0.76155754,
            0.75344859,
            0.74469707,
            0.7356597,
            0.72649847,
            0.71678839,
            0.70636234,
            0.6962931,
            0.68681983,
            0.67770403,
            0.66870286,
            0.65970997,
            0.65041342,
            0.63981451,
            0.6254655,
            0.61178354,
            0.61178354,
            0.61178354,
            0.61178354,
        ],
        [
            0.44513886,
            0.62874897,
            0.71032027,
            0.75204099,
            0.77458361,
            0.78635328,
            0.79210351,
            0.79400371,
            0.7936974,
            0.79206531,
            0.78898049,
            0.78414413,
            0.77820458,
            0.77156226,
            0.7644998,
            0.75713663,
            0.74921362,
            0.74061084,
            0.7320752,
            0.72389855,
            0.71589941,
            0.70798877,
            0.70005254,
            0.69200947,
            0.68360997,
            0.6737865,
            0.66000601,
            0.64973358,
            0.64973358,
            0.64973358,
        ],
        [
            0.41286626,
            0.60976727,
            0.69812203,
            0.7431451,
            0.76990787,
            0.78586351,
            0.7949721,
            0.79993854,
            0.80250421,
            0.80319149,
            0.80196185,
            0.79909761,
            0.79500433,
            0.79022682,
            0.78491469,
            0.77912962,
            0.77277299,
            0.76583082,
            0.75873595,
            0.751745,
            0.74489843,
            0.73805432,
            0.73113139,
            0.72413379,
            0.71693525,
            0.7092516,
            0.70015481,
            0.6863676,
            0.67947196,
            0.67947196,
        ],
        [
            0.39274883,
            0.59105147,
            0.68133411,
            0.73315527,
            0.76300913,
            0.78228744,
            0.79447731,
            0.80224646,
            0.80717386,
            0.80985899,
            0.81021727,
            0.80899167,
            0.80664047,
            0.80348132,
            0.79968891,
            0.79534928,
            0.79039593,
            0.7848619,
            0.77904345,
            0.77320609,
            0.76740301,
            0.76150944,
            0.75554648,
            0.74948449,
            0.74328696,
            0.73682998,
            0.7297194,
            0.72125358,
            0.70668174,
            0.70325717,
        ],
        [
            0.37372212,
            0.57015445,
            0.6664333,
            0.72116761,
            0.75521021,
            0.77720271,
            0.792199,
            0.80231108,
            0.80932662,
            0.81341586,
            0.81541422,
            0.81579073,
            0.81487394,
            0.81308074,
            0.81063329,
            0.80757868,
            0.80384315,
            0.79954793,
            0.7948973,
            0.7900533,
            0.78518887,
            0.78022594,
            0.77511,
            0.76985526,
            0.76450674,
            0.75896819,
            0.75313416,
            0.7465912,
            0.73871676,
            0.72264884,
        ],
    ]
)


def test_OMBasicICEngineComponent():
    """Tests ManualBasicICEngine component."""
    # Same test as in test_basicIC_engine.test_compute_flight_points
    engine = OMBasicICEngineComponent(flight_point_count=(2, 5))

    machs = [0, 0.3, 0.3, 0.5, 0.5]
    altitudes = [0, 0, 0, 4000, 8000]
    thrust_rates = [0.8, 0.5, 0.5, 0.4, 0.7]
    thrusts = [3193.97963124, 480.58508079, 480.58508079, 145.47341988, 241.10415143]
    phases = [
        EngineSetting.TAKEOFF,
        EngineSetting.TAKEOFF,
        EngineSetting.CLIMB,
        EngineSetting.IDLE,
        EngineSetting.CRUISE,
    ]  # mix EngineSetting with integers
    expected_sfc = [2.414166e-16, 1.356846e-05, 1.356846e-05, 2.939614e-05, 2.172072e-05]

    ivc = om.IndepVarComp()
    ivc.add_output("data:propulsion:IC_engine:max_power", 130000, units="W")
    ivc.add_output("data:propulsion:IC_engine:fuel_type", 1)
    ivc.add_output("data:propulsion:IC_engine:strokes_nb", 4)
    ivc.add_output("data:TLAR:v_cruise", 158.0, units="kn")
    ivc.add_output("data:aerodynamics:propeller:cruise_level:altitude", 8000.0, units="ft")
    ivc.add_output("data:geometry:propulsion:engine:layout", 1.0)
    ivc.add_output("data:aerodynamics:propeller:sea_level:speed", SPEED, units="m/s")
    ivc.add_output("data:aerodynamics:propeller:sea_level:thrust", THRUST_SL, units="N")
    ivc.add_output("data:aerodynamics:propeller:sea_level:thrust_limit", THRUST_SL_LIMIT, units="N")
    ivc.add_output("data:aerodynamics:propeller:sea_level:efficiency", EFFICIENCY_SL)
    ivc.add_output("data:aerodynamics:propeller:cruise_level:speed", SPEED, units="m/s")
    ivc.add_output("data:aerodynamics:propeller:cruise_level:thrust", THRUST_CL, units="N")
    ivc.add_output(
        "data:aerodynamics:propeller:cruise_level:thrust_limit", THRUST_CL_LIMIT, units="N"
    )
    ivc.add_output("data:aerodynamics:propeller:cruise_level:efficiency", EFFICIENCY_CL)

    ivc.add_output("data:propulsion:mach", [machs, machs])
    ivc.add_output("data:propulsion:altitude", [altitudes, altitudes], units="ft")
    ivc.add_output("data:propulsion:engine_setting", [phases, phases])
    ivc.add_output("data:propulsion:use_thrust_rate", [[True] * 5, [False] * 5])
    ivc.add_output("data:propulsion:required_thrust_rate", [thrust_rates, [0] * 5])
    ivc.add_output("data:propulsion:required_thrust", [[0] * 5, thrusts], units="N")

    problem = run_system(engine, ivc)

    np.testing.assert_allclose(
        problem["data:propulsion:SFC"], [expected_sfc, expected_sfc], rtol=1e-2
    )
    np.testing.assert_allclose(
        problem["data:propulsion:thrust_rate"], [thrust_rates, thrust_rates], rtol=1e-2
    )
    np.testing.assert_allclose(problem["data:propulsion:thrust"], [thrusts, thrusts], rtol=1e-2)
