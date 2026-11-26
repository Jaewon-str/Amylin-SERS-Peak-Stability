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

### Importing and verifying the 2h spectrum

I intentially loaded columns A and C from the "Figure.4c" worksheet to choose the Raman shift and SERS intensity for 10μM hIAPP after 2h of incubation at pH 5.5. I used 'header = 1' because the first row contains the experimental conditions and the second row contains the column labels. Below is the code:

```python
spectrum = pd.read_excel(workbook, sheet_name="Fig.4c", header=1, usecols="A,C")
print(spectrum.head())
```

I compared the first five rows with the values in Excel and found that they are the same. In other words, the python program successfully imported the 2h spectrum drawn by Excel.

```text
   wavenumber        2 h
0     302.463  135.54574
1     303.991  159.43101
2     305.519  180.35156
3     307.046  198.30740
4     308.574  213.29852
```

### Checking the spectrum before smoothing

Before applyin additional smoothing, I checked the 2 h spectrum from `Fig.4c` for missing values, duplicate Raman shifts, and the order of the measurement points. And then, I calculated the spacing between consecutive points in the 1550–1750 cm⁻¹ region.

```python
spectrum.columns = ["shift", "intensity"]

print("파수 결측값 개수:", spectrum["shift"].isna().sum()) #wavenumber missing values count
print("강도 결측값 개수:", spectrum["intensity"].isna().sum()) #intensity missing values count
print("중복 파수 개수:", spectrum["shift"].dropna().duplicated().sum()) #duplicate wavenumber count
print("파수가 매 행에서 증가하는가?", spectrum["shift"].diff().iloc[1:].gt(0).all()) #Check if wavenumber increases in every row

region = spectrum.loc[spectrum["shift"].between(1550, 1750)] #looking for the region between 1550 and 1750 cm⁻¹
spacing = region["shift"].diff().dropna() #checking the spacing between wavenumbers in the region

print("1550–1750 cm⁻¹ 구간의 측정점 수:", len(region)) #number of measurement points in the 1550–1750 cm⁻¹ region
print(f"파수 간격 (최소 / 중앙 / 최대): {spacing.min():.3f} / {spacing.median():.3f} / {spacing.max():.3f} cm⁻¹") #spacing between wavenumbers (min / median / max)
```

**Terminal output**

```text
파수 결측값 개수: 0
강도 결측값 개수: 0
중복 파수 개수: 0
파수가 매 행에서 증가하는가? True
1550–1750 cm⁻¹ 구간의 측정점 수: 158
파수 간격 (최소 / 중앙 / 최대): 1.248 / 1.266 / 1.284 cm⁻¹
```

This completed my pre-smoothing data check. I recorded the median spacing so I could later relate each smoothing window, specified in points, to its approximate width in cm⁻¹.

### Selecting the amide I band and defining the tracking rule

In the Excel plot, the dominant band was located near 1655 cm⁻¹, so I selected 1640–1670 cm⁻¹ as the tracking interval because it includes the band and excludes the weaker feature near 1610 cm⁻¹. Before applying any additional smoothing, I located the measured point with the highest SERS intensity in this interval.

```python
target = region.loc[region["shift"].between(1640, 1670)] #looking for the target region between 1640 and 1670 cm⁻¹
peak = target.loc[target["intensity"].idxmax()] #finding the strongest peak in the target region, and read the corresponding wavenumber and intensity

print(f"추적 구간: 1640–1670 cm⁻¹ (측정점 {len(target)}개)")
print(f"최고 강도를 보인 파수: {peak['shift']:.3f} cm⁻¹")
print(f"그 지점의 SERS 강도: {peak['intensity']:.2f} a.u.")
```

**Terminal output**

```text
추적 구간: 1640–1670 cm⁻¹ (측정점 24개) #target region: 1640–1670 cm⁻¹ (number of measurement points)
최고 강도를 보인 파수: 1655.660 cm⁻¹ #strongest peak wavenumber
그 지점의 SERS 강도: 2158.19 a.u. #SERS intensity at that point
```

Of the 24 measured points in the interval, the highest intensity was 2158.19 a.u. at 1655.660 cm⁻¹. This gives me a reference position on the original intensity curve.

**Tracking rule for the smoothing comparison**

For each smoothing window, I will use the same 1640–1670 cm⁻¹ interval and identify local minima where the second derivative is negative. If there is one candidate, its position will be recorded. Likewise, if there are several, all their positions will be recorded. If there are none, I will record “no candidate detected.” This enables to test if the same feature remains identifiable as the smoothing window changes.

### Comparing Savitzky–Golay smoothing windows

Before calculating the second derivative, I examined how the smoothing window affected the shape of the dominant amide I band near 1655 cm⁻¹. I used the same spectrum for all three settings so that I could compare changes in the peak height and the slope on its higher-wavenumber side.

Across the 1550–1750 cm⁻¹ region, the spacing between adjacent measurements ranged from 1.248 to 1.284 cm⁻¹. I used linear interpolation to obtain 158 evenly spaced points with the same endpoints as the original data. I then applied a Savitzky–Golay filter over this full region, using window lengths of 7, 15, and 25 points and keeping the polynomial order fixed at 3. This allowed measurements on both sides of the target band to contribute to smoothing.

```python
shift = region["shift"].to_numpy()
intensity = region["intensity"].to_numpy()

uniform_shift = np.linspace(shift[0], shift[-1], len(shift))
uniform_intensity = np.interp(uniform_shift, shift, intensity)

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(shift, intensity, s=12, color="black", label="Original data")

for window in [7, 15, 25]:
    smoothed = savgol_filter(uniform_intensity, window_length=window, polyorder=3)
    ax.plot(uniform_shift, smoothed, label=f"{window}-point window")

ax.set_xlabel("Raman shift (cm⁻¹)")
ax.set_ylabel("SERS intensity (a.u.)")
ax.set_title("Effect of smoothing window on the hIAPP amide I band")
ax.legend()
fig.tight_layout()
plt.show()
```

![hIAPP amide I spectrum with 7-, 15-, and 25-point Savitzky–Golay smoothing windows](https://github.com/user-attachments/assets/553b45db-ffa5-4b36-891e-b0d1d747e31d)

*Figure 3. Effect of smoothing window length on the SERS spectrum of 10 μM hIAPP after 2 h at pH 5.5. Black dots show the original measurements. The 7-, 15-, and 25-point windows span approximately 7.6, 17.7, and 30.4 cm⁻¹ from the first to the last point.*

The highest measured intensity was 2158.19 a.u. at 1655.660 cm⁻¹. All three smoothed curves retained the dominant band near this position and its gradual decline toward higher wavenumbers. The clearest difference was at the top of the band: the 7- and 15-point curves nearly overlapped, while the 25-point window produced a visibly lower maximum. The smaller feature near 1570 cm⁻¹ was also less pronounced with the widest window.

To determine how sensitive the detected peak position is to smoothing, I will next compare the locations of negative local minima in the second derivative within the predefined 1640–1670 cm⁻¹ interval.

### Comparing second-derivative minima across smoothing windows

All three smoothing windows preserved the dominant amide I band in Figure 3, and i checked if they also placed its second-derivative minimum at the same Raman shift. The second derivative was calculated from the same evenly spaced spectrum using 7-, 15-, and 25-point Savitzky–Golay windows. I kept the polynomial order fixed at 3 and compared the curves within the predefined 1640–1670 cm⁻¹ interval.

I calculated each derivative across the full 1550–1750 cm⁻¹ region so that points just outside the tracking interval could contribute to the estimate near its boundaries. I used the spacing between adjacent points on the interpolated grid as `delta`, then zoomed in on 1640–1670 cm⁻¹ for Figure 4.


```python
# Use the evenly spaced Raman shifts and intensities prepared for Figure 3.
delta_shift = uniform_shift[1] - uniform_shift[0]
fig_deriv, ax_deriv = plt.subplots(figsize=(8, 5))

for window in [7, 15, 25]:
    second_derivative = savgol_filter(
        uniform_intensity,
        window_length=window,
        polyorder=3,
        deriv=2,
        delta=delta_shift,
    )
    ax_deriv.plot(
        uniform_shift, second_derivative, label=f"{window}-point window"
    )

ax_deriv.axhline(0, color="gray", linewidth=0.8, linestyle="--")
ax_deriv.set_xlim(1640, 1670)
ax_deriv.set_xlabel("Raman shift (cm⁻¹)")
ax_deriv.set_ylabel("Second derivative [a.u. / (cm⁻¹)²]")
ax_deriv.set_title("Second derivative of the hIAPP amide I band")
ax_deriv.legend()
fig_deriv.tight_layout()
plt.show()
```


<img width="800" height="500" alt="Figure 2_Second Derivative of the hlAPP amide I band" src="https://github.com/user-attachments/assets/3e5ffdca-8ae7-4ee9-8f8f-bcd8f5da3df9" />

*Figure 4. Second derivative of the SERS spectrum of 10 μM hIAPP after 2 h at pH 5.5, calculated with 7-, 15-, and 25-point Savitzky–Golay windows. The dashed line marks zero.*

I estimated the minimum position for each window by visually locating the bottom of its curve in Figure 4.

| Window length | Approximate minimum (cm⁻¹) | Appearance |
|:---:|:---:|:---:|
| 7 points | 1652 | Deepest and narrowest minimum |
| 15 points | 1654 | Intermediate depth and width |
| 25 points | 1655 | Shallowest and broadest minimum |

Each curve showed one visible negative minimum in the tracking interval. As the window increased from 7 to 25 points, the minimum became broader and shallower, and its apparent position moved by about 3 cm⁻¹ toward higher Raman shift.

This comparison matters because a band position can inform a proposed structural assignment. Here, changing only the smoothing window moved the estimated minimum within a single spectrum. The broad feature remained visible across all three settings, but its precise location depended on how I processed the data. I will quantify that sensitivity by extracting the minimum positions in Python and comparing their spread with the spacing between measured points.

### Quantifying the effect of window length on the minimum position

In Figure 4, I estimated the positions of the second-derivative minima by eye. How large is the apparent shift compared with the spacing between measured points?

To answer this question, I will use the same rule for all three smoothing windows. Within 1640–1670 cm⁻¹, I will record every local minimum with a negative second-derivative value. If each window yields one candidate, the difference between the highest and lowest candidate positions will be calculated and compared with the median spacing of the original measurements (1.266 cm⁻¹). If a window yields zero or multiple candidates, I will report that count explicitly.

I estimated the minimum positions by eye in Figure 4, then checked those estimates in Python. For each window, I used `find_peaks(-second_derivative)` to locate the valleys in the second-derivative curve. I kept every local minimum within 1640–1670 cm⁻¹ whose second-derivative value was below zero.


<summary> Python code for detecting and reporting the minima</summary>

I added `find_peaks` to the existing SciPy import at the top of `inspect_spectrum.py`.

```python
from scipy.signal import savgol_filter, find_peaks
```

Inside the loop that generated Figure 4, I added the following lines immediately after `ax_deriv.plot(...)`. For each window, `find_peaks(-second_derivative)` locates the valleys by turning them into peaks. I searched the full curve first so that points near the boundaries of the tracking interval could still be compared with their neighbors on both sides.

```python
minima, _ = find_peaks(-second_derivative)

in_target = (
    (uniform_shift[minima] >= 1640)
    & (uniform_shift[minima] <= 1670)
    & (second_derivative[minima] < 0)
)
positions = uniform_shift[minima[in_target]]

print(
    f"{window}점 창 | 후보 {len(positions)}개 | "
    f"위치(cm⁻¹): {positions.round(2)}"
)
```

`minima` contains array indices. I used `uniform_shift` to convert the selected indices into Raman shifts and printed every candidate so I could check how many each window produced. I rounded the positions to two decimal places for display.




**Terminal output**

```text
7점 창 | 후보 1개 | 위치(cm⁻¹): [1652.4]
15점 창 | 후보 1개 | 위치(cm⁻¹): [1653.67]
25점 창 | 후보 1개 | 위치(cm⁻¹): [1654.93]
```

Each window yielded one candidate. Its position on the interpolated grid increased from 1652.40 cm⁻¹ with the 7-point window to 1653.67 cm⁻¹ with the 15-point window and 1654.93 cm⁻¹ with the 25-point window. These values agreed with my visual estimates from Figure 4.

The difference between the 7- and 25-point results was 2.53 cm⁻¹, about twice the median spacing between adjacent points in the original spectrum (1.266 cm⁻¹). Across the three settings, I could consistently detect one minimum in the target interval, but its estimated position depended on the smoothing window. Since all three calculations used the same 2 h spectrum, this spread shows how much the processing choice alone affected the position I would report for this band.
