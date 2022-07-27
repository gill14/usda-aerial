

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