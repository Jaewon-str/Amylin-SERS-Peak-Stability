# Amylin-SERS-Peak-Stability
How does the smoothing window affect peak positions detected in the amide I region of amylin SERS spectra? A Python reanalysis of published data.
All dataset was downloaded from https://doi.org/10.6084/m9.figshare.23591901. This page will re-analyze the publied data, and extract insights if the smoothing window affect peak positions detected in the amide I region of amylin SERS spectra. The peaks will be compared with the data on the paper.

# Spectrum selection and initial visualization
<img width="611" height="260" alt="image" src="https://github.com/user-attachments/assets/19184e1f-22ea-4095-986a-df94779bc0b5" />

I selected the representative SERS spectrum of 10 μM human islet amyloid polypeptide (hIAPP) after 2 h of incubation at pH 5.5 from the source data for Figure 4c of Fu et al. (2023). I chose a single spectrum so that I could vary the smoothing window while keeping the sample and incubation conditions fixed.

<img width="359" height="215" alt="image" src="https://github.com/user-attachments/assets/baa44c30-4790-44fc-b8b8-94b2966d99bc" />

I first plotted the full spectrum in Excel using the Raman shift in column A and the 2 h SERS intensity in column C. This gave me a visual check that I had selected the intended columns and showed where the amide I band appeared within the full spectrum. I used the intensity values as provided, without applying additional smoothing or baseline correction. This plot serves as the reference for the subsequent peak analysis.
