# Amylin-SERS-Peak-Stability
How does the smoothing window affect peak positions detected in the amide I region of amylin SERS spectra? A Python reanalysis of published data.
All dataset was downloaded from https://doi.org/10.6084/m9.figshare.23591901. This page will re-analyze the publied data, and extract insights if the smoothing window affect peak positions detected in the amide I region of amylin SERS spectra. The peaks will be compared with the data on the paper.

# Spectrum selection and initial visualization
<img width="611" height="260" alt="image" src="https://github.com/user-attachments/assets/19184e1f-22ea-4095-986a-df94779bc0b5" />

I selected the representative SERS spectrum of 10 μM human islet amyloid polypeptide (hIAPP) after 2 h of incubation at pH 5.5 from the source data for Figure 4c of Fu et al. (2023). I chose a single spectrum so that I could vary the smoothing window while keeping the sample and incubation conditions fixed.

<img width="359" height="215" alt="image" src="https://github.com/user-attachments/assets/baa44c30-4790-44fc-b8b8-94b2966d99bc" />

I first plotted the full spectrum in Excel using the Raman shift in column A and the 2 h SERS intensity in column C. This gave me a visual check that I had selected the intended columns and showed where the amide I band appeared within the full spectrum. I used the intensity values as provided, without applying additional smoothing or baseline correction. This plot serves as the reference for the subsequent peak analysis.


# Visual inspection of the amide I region

<img width="364" height="214" alt="image" src="https://github.com/user-attachments/assets/38566324-871a-41fa-ba8d-a82556cfba05" />

I plotted the 1550–1750 cm⁻¹ range to match the wavenumber range shown in Figure 4f of Fu et al. (2023). The dominant band reaches a maximum near 1655 cm⁻¹. It rises steeply from a local minimum near 1630 cm⁻¹ and decreases more gradually on the higher-wavenumber side. Two weaker features are visible near 1570 and 1605–1610 cm⁻¹.

These positions are visual estimates from the spectrum as provided. No additional smoothing or baseline correction was applied. I will use the band near 1655 cm⁻¹ as a reference when testing how the smoothing window affects the position of the corresponding minimum in the second derivative.
