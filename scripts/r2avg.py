import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

sns.set_theme(style="ticks", color_codes=True)


#designate input file
input_file = "fsl_r2avg/64c_512s.csv"

#pandas read input csv
dataset = pd.read_csv(input_file, header = 0,  sep=',')

sns.catplot(x="ATLAS", y="AVG_MASKED", kind="boxen",
            data=dataset.sort_values("ATLAS"))

g = sns.FacetGrid(dataset, col="FWHM")
g.map(sns.boxenplot, "ATLAS", "AVG_MASKED", order=["dypac", "difumo", "mist"])

plt.show()
