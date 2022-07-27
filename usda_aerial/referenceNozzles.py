from math import isnan

COLOR_DEFAULT = "#FFFFFF"

REF_NOZZLES = {
        "Very Fine": {
            "DV01": [0.0, 59.5],
            "DV05": [0.0, 134.4],
            "DV09": [134.4, 236.4],
            "RANK": 0,
            "Abbreviation": "VF",
            "Color": "#FF0000",
        },
        "Fine": {
            "DV01": [59.5, 110.3],
            "DV05": [134.4, 248.1],
            "DV09": [236.4, 409.4],
            "RANK": 1,
            "Abbreviation": "F",
            "Color": "#FFA500",
        },
        "Medium": {
            "DV01": [110.3, 162.0],
            "DV05": [248.1, 357.8],
            "DV09": [409.4, 584.0],
            "RANK": 2,
            "Abbreviation": "M",
            "Color": "#FFFF00",
        },
        "Coarse": {
            "DV01": [162.0, 191.7],
            "DV05": [357.8, 431.0],
            "DV09": [584.0, 737.1],
            "RANK": 3,
            "Abbreviation": "C",
            "Color": "#0000FF",
        },
        "Very Coarse": {
            "DV01": [191.7, 226.1],
            "DV05": [431.0, 500.9],
            "DV09": [737.1, 819.8],
            "RANK": 4,
            "Abbreviation": "VC",
            "Color": "#008000",
        },
        "Extremely Coarse": {
            "DV01": [226.1, 302.5],
            "DV05": [500.9, 658.6],
            "DV09": [819.8, 1142.2],
            "RANK": 5,
            "Abbreviation": "XC",
            "Color": "#D8D8D8",
        },
        "Ultra Coarse": {
            "DV01": [302.5, 65535],
            "DV05": [658.6, 65535],
            "DV09": [1142.2, 65535],
            "RANK": 6,
            "Abbreviation": "UC",
            "Color": "#000000",
        },
    }

class ReferenceNozzles:
    
    """
    External methods for acquiring Categories and Category Colors
    """
    
    def get_dsc(dv01: float, dv05: float, abbreviated=False) -> str:
        dsc = ReferenceNozzles._get_dsc(dv01, dv05)
        if dsc and abbreviated:
            dsc = REF_NOZZLES[dsc]["Abbreviation"]
        return dsc
        
    def get_dsc_color(dv01: float, dv05: float, color_default=COLOR_DEFAULT) -> str:
        return ReferenceNozzles._get_category_color(
            ReferenceNozzles._get_dsc(dv01, dv05),
            color_default
            )
    
    def get_dv01_category(dv01: float) -> str:
        return ReferenceNozzles._get_dv_category(dv=dv01, dv_key="DV01")
    
    def get_dv01_category_color(dv01: float, color_default=COLOR_DEFAULT) -> str:
        return ReferenceNozzles._get_category_color(
            ReferenceNozzles.get_dv01_category(dv01),
            color_default
        )
        
    def get_dv05_category(dv05: float) -> str:
        return ReferenceNozzles._get_dv_category(dv=dv05, dv_key="DV05")
    
    def get_dv05_category_color(dv05: float, color_default=COLOR_DEFAULT) -> str:
        return ReferenceNozzles._get_category_color(
            ReferenceNozzles.get_dv05_category(dv05),
            color_default
        )
        
    def get_dv09_category(dv09: float) -> str:
        return ReferenceNozzles._get_dv_category(dv=dv09, dv_key="DV09")
    
    def get_dv09_category_color(dv09: float, color_default=COLOR_DEFAULT) -> str:
        return ReferenceNozzles._get_category_color(
            ReferenceNozzles.get_dv09_category(dv09),
            color_default
        )
    
    """
    Internal Calculation methods
    """
    
    def _get_dsc(dv01: float, dv05: float) -> str:
        # Defualt to an empty string
        dsc = ""
        # Obtain the dv01 and dv05 categories
        cat_01 = ReferenceNozzles._get_dv_category(dv=dv01, dv_key='DV01')
        cat_05 = ReferenceNozzles._get_dv_category(dv=dv05, dv_key="DV05")
        # Ensure both are not empty strings
        if cat_01 and cat_05:
            # Take the min ranked category of the two
            dsc =  cat_01 if REF_NOZZLES[cat_01]["RANK"] < REF_NOZZLES[cat_05]["RANK"] else cat_05
        return dsc
        
    def _get_dv_category(dv: float, dv_key: str) -> str:
        # Default to an empty string
        dv_category = ""
        # Ensure the dv is a positive number
        if not isnan(dv) and dv > 0:
            for category in REF_NOZZLES.keys():
                if REF_NOZZLES[category][dv_key][0] <= dv <= REF_NOZZLES[category][dv_key][1]:
                    dv_category = category
                    break
        return dv_category
    
    def _get_category_color(category: str, color_default=COLOR_DEFAULT) -> str:
        color = color_default
        if category:
            color = REF_NOZZLES[category]["Color"]
        return color