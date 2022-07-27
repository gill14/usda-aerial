from usda_aerial.atomizationModel import AtomizationModel
from usda_aerial.referenceNozzles import REF_NOZZLES, ReferenceNozzles
from usda_aerial.nozzles import NOZZLES, Nozzle

print("Choose a Nozzle from the following:")
print(NOZZLES)
nozzle = input("Nozzle:  ")
print("Choose an Orifice from the following:")
print(Nozzle.get_orifices_for_nozzle(nozzle))
orifice = input("Orifice:  ")
print("Choose a Deflection angle from the following:")
print(Nozzle.get_deflections_for_nozzle(nozzle))
angle = input("Deflection:  ")
pressure = int(input("Pressure:  "))
airspeed = int(input("Airspeed:  "))
# Run Model
model = AtomizationModel(nozzle, orifice, airspeed, pressure, angle)
# Print Results
dv01 = model.dv01()
dv05 = model.dv05()
dv09 = model.dv09()
print("-----")
print("Results")
print("-----")
print(f"DSC = {ReferenceNozzles.get_dsc(dv01, dv05)}")
print(f"DV_01 = {str(dv01)}")
print(f"DV_05 = {str(dv05)}")
print(f"DV_09 = {str(dv09)}")
print(f"Relative Span = {model.rs():.2f}")
print(f"%<100 = {str(model.p_lt_100())}")
print(f"%<200 = {str(model.p_lt_200())}")