This script will input IR spectra from .txt files (as output by Shimadzu Spectrometers).

For combinations of materials, i.e. the filename ("Pd44_glycine.txt") the software will compare the combination to each constituent.
("glycine.txt" and "Pd44"). It outputs the following: 

- Plots a .png of three spectra overlaid (matplotlib) in both absorbance and transmittance mode
- Peak picks each spectrum (scipy.signals)
- Outputs peak picked list to a .csv file

Note that it will also create directories for these files to be stored in.

Saved here as an example of recent work.
