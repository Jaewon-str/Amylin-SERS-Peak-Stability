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

# Opening the source workbook in Python

After plotting the spectrum in Excel, I opened the same source workbook in Python and listed its worksheets. This confirmed that Fig.4c was available for the next step. I defined the workbook path relative to the script so the code can run from another computer using the same folder structure. Below is the code: 

```python
from pathlib import Path
import pandas as pd

file_path = Path(__file__).parent / "Amylin Raw Data" / "Raw_Data.xlsx" #Amylin Raw Data 폴더 안에 있는 Raw_Data.xlsx 파일을 열어라
print("엑셀 파일을 찾는 위치:", file_path.resolve()) #Where to find the excel file

if file_path.is_file():
    workbook = pd.ExcelFile(file_path, engine="openpyxl")
    print("시트 목록:", workbook.sheet_names) # Sheet names in the excel file
else:
    print("이 위치에 엑셀 파일이 없어. file_path를 확인해 줘.") # No excel file found at this location. Please check the file_path.
```

My first attempt to open the workbook raised an ImportError because openpyxl was missing. I installed it with python3 -m pip install openpyxl, reran the script, and confirmed that Fig.4c appeared in the worksheet list.
