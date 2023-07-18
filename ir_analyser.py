from scipy.signal import find_peaks
from matplotlib import pyplot as plt
import math
import pandas as pd
import os 
import glob

class spectrum:
    def __init__(self, name, wavenumbers, transmittances, window=30):
        self.name = name
        self.wavenumbers = wavenumbers
        self.transmittances_raw = transmittances
        self.absorbances_raw = [2-math.log10(i) for i in self.transmittances_raw]
        self.absorbances = [i/max(self.absorbances_raw)*0.5 for i in self.absorbances_raw]
        self.transmittances = [i for i in self.transmittances_raw]
        threshold = max(self.absorbances)/4
        self.peaks = peak_find(wavenumbers, self.absorbances, self.transmittances, window, threshold)
        self.peak_positions = [i.position for i in self.peaks]
        
class peak:
    def __init__(self, position, intensity, transmittance):
        self.position = position
        self.intensity = intensity
        self.transmittance = transmittance
        
def file_check(file_path):
    filename = file_path.split("\\")[-1]
    print(filename)
    if len(filename.split("_")) != 1 and filename[-1] == "t":
        return True

def folder_check(subfolders):    
    x = os.getcwd()
    for i in subfolders:
        if os.path.exists(f"{x}/{i}"):
            pass
        else:
            os.mkdir(i)
            print(f"{i} folder not present, folder added to {x}")        

def peak_find(wavenumbers, absorbances, transmittances, window, threshold):
    peaks = find_peaks(absorbances, height = threshold, distance=window)
    peak_heights = list(peaks[1]["peak_heights"])
    peak_wavenumbers = list([wavenumbers[i] for i in peaks[0]])
    transmittance_values = list([transmittances[i] for i in peaks[0]])
    output_peaks = [peak(i, j, k) for i, j, k in zip(peak_wavenumbers, peak_heights, transmittance_values)]
    return output_peaks

def clean_and_round(list1, list2, list3):
    max_length = max(len(list1), len(list2), len(list3))
    for i in [list1, list2, list3]:
        while len(i) < max_length:
            i.append(0)
    x = [round(i) for i in list1]
    y = [round(i) for i in list2]
    z = [round(i) for i in list3]
    return x, y, z
    
def import_spectrum(file):
    with open(f"{file}.txt", "r") as f:
        x = f.readlines()
        wavenumbers = []
        transmittances = []
        for i in x[4:]:
            w = i.split("\t")
            wavenumbers.append(float(w[0]))
            transmittances.append(float(w[1]))
        return spectrum(file, wavenumbers, transmittances)
    
def combi_find(mixture):
    x = mixture.split("_")
    return x[0], x[1]
     
def plot_trigraph_abs(file):
    folder_check(["absorbance_plots"])
    os.chdir(main_folder)
    plt.figure(figsize = (14, 10))
    x = import_spectrum(file)
    plt.plot(x.wavenumbers, x.absorbances, color="red")
    plt.scatter([i.position for i in x.peaks], [i.intensity for i in x.peaks], color="red", label=file)
    print(f"Plotting absorbance spectrum for {file} mixture...")
    palladium, coformer = combi_find(file)
    try:
        y = import_spectrum(palladium)
    except:
        print(f"######No {palladium} complex found, skipping...######")
        plt.close()
        return 10
    plt.plot(y.wavenumbers, y.absorbances, color = "green")
    plt.scatter([i.position for i in y.peaks], [i.intensity for i in y.peaks], color="green", label=palladium)
    try:
        z = import_spectrum(coformer)
    except:
        print(f"######No {coformer} spectrum found, skipping...######")
        plt.close() 
        return 10
    plt.plot(z.wavenumbers, z.absorbances, color = "blue")
    plt.scatter([i.position for i in z.peaks], [i.intensity for i in z.peaks], color="blue", label=coformer)
    plt.legend(fontsize=20)
    plt.xlim(2200, 400)
    plt.ylabel("Normalised Absorbance", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel("Wavenumber / cm$^{-1}$", fontsize=20)
    plt.title(f"Comparison of {file} mixture to individual {palladium} and {coformer}", fontsize=20)
    plt.tight_layout()
    plt.savefig(f"absorbance_plots//{file}.png")
    #plt.show()
    plt.close()
    
def plot_trigraph_trans(file):
    folder_check(["transmittance_plots"])
    os.chdir(main_folder)
    plt.figure(figsize = (14,10))
    x = import_spectrum(file)
    plt.plot(x.wavenumbers, x.transmittances, color="red")
    plt.scatter([i.position for i in x.peaks], [i.transmittance for i in x.peaks], color="red", label=file)
    print(f"Plotting transmittance spectrum for {file} mixture...")
    palladium, coformer = combi_find(file)
    try:
        y = import_spectrum(palladium)
    except:
        print(f"######No {palladium} complex found, skipping...######")
        plt.close()
        return 10
    plt.plot(y.wavenumbers, y.transmittances, color = "green")
    plt.scatter([i.position for i in y.peaks], [i.transmittance for i in y.peaks], color="green", label=palladium)
    try:
        z = import_spectrum(coformer)
    except:
        print(f"######No {coformer} spectrum found, skipping...######")
        plt.close() 
        return 10
    plt.plot(z.wavenumbers, z.transmittances, color = "blue")
    plt.scatter([i.position for i in z.peaks], [i.transmittance for i in z.peaks], color="blue", label=coformer)
    plt.legend(fontsize=20)
    plt.xlim(2200, 400)
    plt.ylabel("Transmittance / %", fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.xlabel("Wavenumber / cm$^{-1}$", fontsize=20)
    plt.title(f"Comparison of {file} mixture to individual {palladium} and {coformer}", fontsize=20)
    plt.tight_layout()
    plt.savefig(f"transmittance_plots//{file}.png")
    #plt.show()
    plt.close()
    
def output_peaks(file):
    folder_check(["picked_peaks"])
    os.chdir(main_folder)
    print(f"Outputting peak summary for {file} mixture...\n")
    try:
        x = import_spectrum(file)
    except:
        print(f"######No {file} spectrum found, skipping...######")
        return 10
    palladium, coformer = combi_find(file)
    try:
        y = import_spectrum(palladium)
    except:
        print(f"######No {palladium} complex found, skipping...######")
        return 10
    try:
        z = import_spectrum(coformer)
    except:
        print(f"######No {coformer} spectrum found, skipping...######")
        return 10
    x, y, z = clean_and_round(x.peak_positions, y.peak_positions, z.peak_positions)
    data = {f"{file}":x, f"{palladium}":y, f"{coformer}":z}
    df = pd.DataFrame(data=data)
    df.to_csv(f"picked_peaks//{file}_peak_position_summary.csv")
    
main_folder = os.getcwd()
all_files = (glob.glob(f"{main_folder}/*.*"))
combi_files = [i.split("\\")[-1][:-4] for i in all_files if file_check(i) == True]
print(combi_files)
print(f"\n{len(combi_files)} files found. Commencing...\n")
    
for i in combi_files: 
    plot_trigraph_abs(i)
    plot_trigraph_trans(i)
    output_peaks(i)