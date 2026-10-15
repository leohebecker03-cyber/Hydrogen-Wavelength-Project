##ReadMe for Hydrogen wavelength comparison code.

##This code can be used to compare calculated hydrogen transition wavelength to experimental Data aqquired from NIST.

##The NIST data is provided in the Github repository under Hydrogen.csv

#The code will load in the data, clean it in order for it to run smoothly, filter the data for Balmer transitions. It will then calculate the predicted wavelength, comparison between experimental and calculated wavelength, percentage error, normalised difference, correlation between data and then plot the results and the residual wavelength.

##The output will include
** Table of observed and calculated wavelength
** Normalized difference
** Mean percentage error
** Mean absolute difference
** Linear Correlation
** One plot for observed vs calculated wavelength
** One plot for residual wavelength.


##Requirements
You will need to pip install pandas, numpy, and matplotlib

##Howtorun
place Hydrogen.csv and the Hydrogen_Test.py in one folder then run the python file.