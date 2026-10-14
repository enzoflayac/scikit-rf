import skrf as rf
from skrf.vi.vna.keysight.ena import ENA

# Remplace par l'IP de ton E5071C ou E5061B
vna = ENA("TCPIP0::192.168.1.50::inst0::INSTR")

print("Connecté avec succès !")
ch1 = vna.channels[1]

# 1. Tester la lecture
print(f"Fréquence de départ : {ch1.freq_start / 1e6} MHz")
print(f"Fréquence de fin    : {ch1.freq_stop / 1e9} GHz")
print(f"Nombre de points    : {ch1.npoints}")

# 2. Tester l'écriture
print("\nModification des paramètres...")
ch1.freq_start = "100 MHz"
ch1.freq_stop = "1 GHz"
ch1.npoints = 401

print(f"Nouvelle config : {ch1.frequency}")