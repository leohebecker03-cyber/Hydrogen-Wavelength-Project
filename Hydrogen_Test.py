import pandas as pd

data = pd.read_csv("Hydrogen.csv")
#Remove empty extra column Since I only care about complete columns
data = data.drop(columns=["Unnamed: 18"])
#Because the data included some weird notations and was defined as strings I cleaned up the data with this small code section.
data["obs_wl_vac(nm)"] = (
    data["obs_wl_vac(nm)"]
    .astype(str)
    .str.replace('="', '', regex=False)
    .str.replace('"', '', regex=False)
)
#I did the same for the experimental uncertainty data
data["unc_obs_wl"] = (
    data["unc_obs_wl"]
    .astype(str)
    .str.replace('="', '', regex=False)
    .str.replace('"', '', regex=False)
)
#and then converted the strings of data into numerical values. 
data["obs_wl_vac(nm)"] = pd.to_numeric(
    data["obs_wl_vac(nm)"],
    errors="coerce"
)
data["unc_obs_wl"] = pd.to_numeric(
    data["unc_obs_wl"],
    errors="coerce"
)
#Cleaned up the quantum state numbers of the data.
for column in ["conf_i", "conf_k"]:
    data[column] = (
        data[column]
        .astype(str)
        .str.replace('="', '', regex=False)
        .str.replace('"', '', regex=False)
    )
#The next part of the code filters the data so that only balmer series states without fine structure are included in the analysis.
balmer = data[
    (data["conf_i"] == "2") &
    (data["conf_k"].isin(["3", "4", "5", "6", "7", "8", "9"]))
]
print(
    balmer[
        ["conf_i", "conf_k", "obs_wl_vac(nm)", "unc_obs_wl"]
    ]
)

print(data.head())

import numpy as np

R_H = 1.0967758e7   
# Rydberg constant for hydrogen

balmer["n_upper"] = balmer["conf_k"].astype(int)
#Here the system calculates the predicted wavelength using the Rydberg formula. 
balmer["predicted_wavelength_nm"] = (
    1 / (
        R_H * (
            1 / 2**2
            - 1 / balmer["n_upper"]**2
        )
    )
) * 1e9
#Then the difference between experimental and calculated wavelength is calculated. 
balmer["difference_nm"] = (
    balmer["obs_wl_vac(nm)"]
    - balmer["predicted_wavelength_nm"]
)
#As well as the percentage error. 
balmer["percentage_error"] = (
    abs(balmer["difference_nm"])
    / balmer["obs_wl_vac(nm)"]
    * 100
)

print(
    balmer[
        [
            "n_upper",
            "obs_wl_vac(nm)",
            "predicted_wavelength_nm",
            "difference_nm",
            "percentage_error"
        ]
    ]
)
#The mean percentage error and mean absolute difference are calculated.
mean_percentage_error = balmer["percentage_error"].mean()

print("Mean percentage error:", mean_percentage_error)

mean_absolute_difference = abs(balmer["difference_nm"]).mean()

print("Mean absolute difference:", mean_absolute_difference, "nm")
#Here we calculate the normalized difference is calculated to look at the precision of the Rydberg predictions.
balmer["normalized_difference"] = (
    balmer["difference_nm"]
    / balmer["unc_obs_wl"]
)

print(
    balmer[
        [
            "n_upper",
            "difference_nm",
            "unc_obs_wl",
            "normalized_difference"
        ]
    ]
)

import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
#Then we plot our results. First the observed vs calculated wavelengths. 
plt.errorbar(
    balmer["predicted_wavelength_nm"],
    balmer["obs_wl_vac(nm)"],
    yerr=balmer["unc_obs_wl"],
    fmt="o",
    capsize=4,
    label="NIST measurements"
)
minimum = balmer["predicted_wavelength_nm"].min()
maximum = balmer["predicted_wavelength_nm"].max()
plt.plot(
    [minimum, maximum],
    [minimum, maximum],
    "--",
    label="Perfect agreement"
)

plt.xlabel("Calculated wavelength (nm)")
plt.ylabel("Observed wavelength (nm)")
plt.title("Calculated vs Experimental Hydrogen Wavelengths")
plt.legend()
plt.grid()

plt.show()
#and then the residual wavelength differences.
plt.errorbar(
    balmer["n_upper"],
    balmer["difference_nm"],
    yerr=balmer["unc_obs_wl"],
    fmt="o",
    capsize=4
)

plt.axhline(0, linestyle="--")

plt.xlabel("Upper quantum number n")
plt.ylabel("Observed - Calculated wavelength (nm)")
plt.title("Difference Between Experiment and Rydberg Prediction")
plt.grid()

plt.show()
correlation = balmer["obs_wl_vac(nm)"].corr(
    balmer["predicted_wavelength_nm"]
)

print("Correlation:", correlation)