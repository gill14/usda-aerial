from usda_aerial.lowSpeedModel import LOW_SPEED_MODEL
from usda_aerial.highSpeedModel import HIGH_SPEED_MODEL

NOZZLES = [
        "CP11TT 20°FF",  # 0
        "CP11TT 40°FF",  # 1
        "CP11TT 60°FF",  # 2
        "CP11TT 80°FF",  # 3
        "CP11TT 110°FF",  # 4
        "CP11TT SS",  # 5
        "CP03",  # 6
        "CP09",  # 7
        "Davidon TriSet",  # 8
        "Steel Disc Core 45",  # 9
        "Ceramic Disc Core 45",  # 10
        "Steel Disc Core SS",  # 11
        "Ceramic Disc Core SS",  # 12
        "Standard 40°FF",  # 13
        "Standard 80°FF",  # 14
    ]  

class Nozzle:
    
    """
    External Methods
    """
    
    def get_nozzles() -> list[str]:
        return NOZZLES
    
    def get_orifices_for_nozzle(nozzle: str) -> list[str]:
        return Nozzle._params_for_nozzle(nozzle, "Orifice")
    
    def get_deflections_for_nozzle(nozzle: str) -> list[str]:
        return Nozzle._params_for_nozzle(nozzle, "Angle")
    
    """
    Internal Methods
    """
    
    """
    This method is designed to be called internally, returning a list of available
    options for a requested parameter. This is used for external convenience methods
    of gettings lists of available orifice size and deflection.
    """
    
    def _params_for_nozzle(nozzle, param):
        nozzles = [nozzle]
        # Check if nozzle has alternate ss/def models
        if nozzle == "CP09":
            nozzles.extend(["CP09 SS", "CP09 Deflection"])
        if nozzle == "Davidon TriSet":
            nozzles.extend(["Davidon TriSet SS", "Davidon TriSet Deflection"])
        vals = []
        for n in nozzles:
            if n in HIGH_SPEED_MODEL.keys():
                vals.extend(HIGH_SPEED_MODEL[n][param])
            if n in LOW_SPEED_MODEL.keys():
                vals.extend(LOW_SPEED_MODEL[n][param])
        return sorted(set(vals))
    
    """
    This method is designed to be called internally. It accounts for differences
    in nozzle names in the LS and HS models. Nozzles without differences have thier 
    names passed, Nozzles with differences have their names altered to reflect which 
    model (LS or HS) their airspeed corresponds to.
    """
    
    def _parse_nozzle(nozzle, airspeed, angle):
        if nozzle == "CP09":
            _nozzle = "CP09 SS" if int(angle) == 0 else "CP09 Deflection"
            if (
                LOW_SPEED_MODEL[_nozzle]["Speed"][0]
                <= airspeed
                < LOW_SPEED_MODEL[_nozzle]["Speed"][1]
            ):
                nozzle = _nozzle
        if nozzle == "Davidon TriSet":
            _nozzle = (
                "Davidon TriSet SS" if int(angle) == 0 else "Davidon TriSet Deflection"
            )
            if (
                LOW_SPEED_MODEL[_nozzle]["Speed"][0]
                <= airspeed
                < LOW_SPEED_MODEL[_nozzle]["Speed"][1]
            ):
                nozzle = _nozzle
        return nozzle