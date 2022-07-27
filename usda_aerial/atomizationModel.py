

from math import sqrt
from usda_aerial.highSpeedModel import HIGH_SPEED_MODEL
from usda_aerial.lowSpeedModel import LOW_SPEED_MODEL
from usda_aerial.nozzles import Nozzle


class AtomizationModel:
    
    def __init__(
        self, nozzle=None, orifice=None, airspeed=None, pressure=None, angle=None
    ):
        self.nozzle = nozzle
        self.orifice = orifice
        self.airspeed = airspeed
        self.pressure = pressure
        self.angle = angle
        
    """
    External Methods
    """

    """
    The Methods to call externally to recieve a calculation. Will return
    an integer for dV and %V calculations
    """

    def dv01(self) -> int:
        return self._calc(param="DV10")

    def dv05(self) -> int:
        return self._calc(param="DV50")

    def dv09(self) -> int:
        return self._calc(param="DV90")

    def p_lt_100(self) -> int:
        return self._calc(param="V100")

    def p_lt_200(self) -> int:
        return self._calc(param="V200")
    
    def rs(self, dv01=None, dv05=None, dv09=None):
        return self._rs(dv01, dv05, dv09)
    
    """
    This method is used to call externally to calculate the flow rate for a given
    orifice based on manufacturer specified flow at 40 PSI. This is not part of
    the USDA atomization model, but is employed here to facilitate flow-weighted
    mean droplet spectrum data as an estimate for composite spray setups.
    """

    def calc_gpm(self):
        return self._calc(param="GPM")
    
    """
    Internal Methods
    """
    
    def _calc(self, nozzle=None, orifice=None, airspeed=None, pressure=None, angle=None, param=None) -> int:
        # use shorthand, with instance var failovers
        n = self.nozzle if nozzle == None else nozzle
        o = self.orifice if orifice == None else orifice
        a = self.airspeed if airspeed == None else airspeed
        p = self.pressure if pressure == None else pressure
        an = self.angle if angle == None else angle
        # Ensure nozzle key will work with applicable model
        n = Nozzle._parse_nozzle(nozzle=n, airspeed=a, angle=an)
        # Attempt to get correct model, set local pressure ranges
        if n in HIGH_SPEED_MODEL.keys():
            rng = HIGH_SPEED_MODEL[n]["Speed"]
            if rng[0] <= a < rng[1]:
                model = HIGH_SPEED_MODEL
                p_rng = (30,60)
        elif n in LOW_SPEED_MODEL.keys():
            rng = LOW_SPEED_MODEL[n]["Speed"]
            if rng[0] <= a < rng[1]:
                model = LOW_SPEED_MODEL
                p_rng = (30,90)
        else:
            # No Model
            return -1
        # Coerce orifice if string
        if type(o) is str:
            orif_str_list = [str(_o) for _o in model[n]["Orifice"]]
            if o in orif_str_list:
                o = model[n]["Orifice"][orif_str_list.index(o)]
        # Is orifice explicitly in applicable model?
        if o not in model[n]["Orifice"]:
            return -1
        # Coerce angle if string
        if type(an) is str:
            angle_str_list = [str(_an) for _an in model[n]["Angle"]]
            if an in angle_str_list:
                an = model[n]["Angle"][angle_str_list.index(an)]
        # Is angle explicitly in applicable model?
        if an not in model[n]["Angle"]:
            return -1
        # Is pressure within range of applicable model?
        if not (p_rng[0] <= p <= p_rng[1]):
            return -1
        # Special case when param is GPM
        if param == "GPM":
            # Find gpm at 40 psi
            gpm_40 = model[n]["Flow"][1]
            # Correct to initialized pressure
            return gpm_40 * sqrt(p/40)
        # Perform adjustment to the 4 input parameters to run the models
        o_a = (o - model[n]["Adjust"][0]) / model[n]["Adjust"][1]
        a_a = (a - model[n]["Adjust"][2]) / model[n]["Adjust"][3]
        p_a = (p - model[n]["Adjust"][4]) / model[n]["Adjust"][5]
        an_a = (an - model[n]["Adjust"][6]) / model[n]["Adjust"][7]
        # Make calculations for requested param
        # Order of constants:
        # Intercept,Orifice,Airspeed,Pressure,Angle,Orf*AS,Orf*Press,AS*Press,Orf*Ang,
        # AS*Ang,Press*Ang,Orf^2,AS^2,Press^,Ang^2
        calc = (
            model[n][param][0]
            + o_a * model[n][param][1]
            + a_a * model[n][param][2]
            + p_a * model[n][param][3]
            + an_a * model[n][param][4]
            + o_a * a_a * model[n][param][5]
            + o_a * p_a * model[n][param][6]
            + a_a * p_a * model[n][param][7]
            + o_a * an_a * model[n][param][8]
            + a_a * an_a * model[n][param][9]
            + p_a * an_a * model[n][param][10]
            + (o_a**2) * model[n][param][11]
            + (a_a**2) * model[n][param][12]
            + (p_a**2) * model[n][param][13]
            + (an_a**2) * model[n][param][14]
        )
        return round(calc)
    
    def _rs(self, dv01=None, dv05=None, dv09=None):
        if dv01 == None:
            dv01 = self.dv01()
        if dv05 == None:
            dv05 = self.dv05()
        if dv09 == None:
            dv09 = self.dv09()
        return (dv09 - dv01) / dv05