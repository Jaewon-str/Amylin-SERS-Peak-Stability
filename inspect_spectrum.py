from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks # Savitzky-Golay filter and peak finding functions from scipy.signal

file_path = Path(__file__).parent / "Amylin Raw Data" / "Raw_Data.xlsx" #Amylin Raw Data 폴더 안에 있는 Raw_Data.xlsx 파일을 열어라
print("엑셀 파일을 찾는 위치:", file_path.resolve()) #Where to find the excel file

if file_path.is_file():
    workbook = pd.ExcelFile(file_path, engine="openpyxl")
    print("시트 목록:", workbook.sheet_names) # Sheet names in the excel file
    spectrum = pd.read_excel(workbook, sheet_name="Fig.4c", header=1, usecols="A,C") #엑셀의 두 번째 행 (wavenumber, 0h, 2h)을 열 제목으로 사용; usecols로 필요한 두 열 고르고, .head()로 상위 5행만 출력
    print(spectrum.head())

    spectrum.columns = ["shift", "intensity"]

    print("파수 결측값 개수:", spectrum["shift"].isna().sum()) #wavenumber missing values count
    print("강도 결측값 개수:", spectrum["intensity"].isna().sum()) #intensity missing values count
    print("중복 파수 개수:", spectrum["shift"].dropna().duplicated().sum()) #duplicate wavenumber count
    print("파수가 매 행에서 증가하는가?", spectrum["shift"].diff().iloc[1:].gt(0).all()) #Check if wavenumber increases in every row

    region = spectrum.loc[spectrum["shift"].between(1550, 1750)] #looking for the region between 1550 and 1750 cm⁻¹
    spacing = region["shift"].diff().dropna() #checking the spacing between wavenumbers in the region

    print("1550–1750 cm⁻¹ 구간의 측정점 수:", len(region)) #number of measurement points in the 1550–1750 cm⁻¹ region
    print(f"파수 간격 (최소 / 중앙 / 최대): {spacing.min():.3f} / {spacing.median():.3f} / {spacing.max():.3f} cm⁻¹") #spacing between wavenumbers (min / median / max)

    target = region.loc[region["shift"].between(1640, 1670)] #looking for the target region between 1640 and 1670 cm⁻¹
    peak = target.loc[target["intensity"].idxmax()] #finding the strongest peak in the target region, and read the corresponding wavenumber and intensity

    print(f"추적 구간: 1640–1670 cm⁻¹ (측정점 {len(target)}개)") #target region: 1640–1670 cm⁻¹ (number of measurement points)
    print(f"최고 강도를 보인 파수: {peak['shift']:.3f} cm⁻¹") #strongest peak wavenumber
    print(f"그 지점의 SERS 강도: {peak['intensity']:.2f} a.u.") #SERS intensity at that point

    shift = region["shift"].to_numpy() #raman shift values in the region of interest (1550–1750 cm⁻¹)
    intensity = region["intensity"].to_numpy()

    # 같은 파수 간격에서 세 평활화 창을 비교
    uniform_shift = np.linspace(shift[0], shift[-1], len(shift)) # uniformly spaced wavenumber values between the first and last wavenumber in the region of interest
    uniform_intensity = np.interp(uniform_shift, shift, intensity)# np.interp is used because we have checked the wavenumber spacing in the region of interest and found that it is not uniform.
                                                                     # This function interpolates the intensity values at the uniformly spaced wavenumber values.
    fig, ax = plt.subplots(figsize=(8, 5)) #set the figure size to 8 inches by 5 inches
    ax.scatter(shift, intensity, s=12, color="black", label="Original data") #data points in the region of interest (1550–1750 cm⁻¹)
   
    for window in [7, 15, 25]:
        smoothed = savgol_filter(uniform_intensity, window_length=window, polyorder=3) #savgol_filter is used to smooth the intensity values at the uniformly spaced wavenumber values. 
                                                                                          # The window_length parameter specifies the length of the filter window
                                                                                          #  and the polyorder parameter specifies the order of the polynomial used to fit the samples.
        ax.plot(uniform_shift, smoothed, label=f"{window}-point window") #smooth the intensity values at the uniformly spaced wavenumber values using a Savitzky-Golay filter with a window length of 7, 15, and 25 points, and plot the smoothed data.
   
    ax.set_xlabel("Raman shift (cm⁻¹)") #set the x-axis label to "Raman shift (cm⁻¹)"
    ax.set_ylabel("SERS intensity (a.u.)") #set the y-axis label to "SERS intensity (a.u.)"
    ax.set_title("Effect of smoothing window on the hIAPP amide I band") #set the title of the plot 
    ax.legend() #add a legend to the plot
    fig.tight_layout() #adjust the layout of the plot to make sure that all elements are visible and not overlapping


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

        minima, _ = find_peaks(-second_derivative) #local minima of the second derivative

        in_target = (
            (uniform_shift[minima] >= 1640)
            & (uniform_shift[minima] <= 1670)
            & (second_derivative[minima] < 0)
        ) #local minima that are within the target region (1640–1670 cm⁻¹) and have a negative second derivative value
        positions = uniform_shift[minima[in_target]] #extract the positions of the selected minima

        print(
            f"{window}점 창 | 후보 {len(positions)}개 | "
            f"위치(cm⁻¹): {positions.round(2)}"
        ) #print the number of candidate minima and their positions in cm⁻¹ for each smoothing window size

    ax_deriv.axhline(0, color="gray", linewidth=0.8, linestyle="--")
    ax_deriv.set_xlim(1640, 1670)
    ax_deriv.set_xlabel("Raman shift (cm⁻¹)")
    ax_deriv.set_ylabel("Second derivative [a.u. / (cm⁻¹)²]")
    ax_deriv.set_title("Second derivative of the hIAPP amide I band")
    ax_deriv.legend()
    fig_deriv.tight_layout()
    plt.show()

else:
    print("이 위치에 엑셀 파일이 없어. file_path를 확인해 줘.") # No excel file found at this location. Please check the file_path.

