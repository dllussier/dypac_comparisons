from scipy import stats
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import mean
from numpy import var
from math import sqrt
from statsmodels.formula.api import ols
import statsmodels.api as sm
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import FloatVector

sns.set_theme(style="ticks", color_codes=True)

# designate input file
input_file = "fsl_r2avg/64c_512s.csv"

# pandas read input csv
dataset = pd.read_csv(input_file, header=0,  sep=',')

print(dataset)

## statistical analyses
data1 = dataset[dataset['ATLAS_FWHM'] == 'dypac_8mm']['AVG_MASKED']
data2 = dataset[dataset['ATLAS_FWHM'] == 'dypac_5mm']['AVG_MASKED']

# 2-sample t-test
stats.ttest_ind(data1, data2)

# paired t-test
stats.ttest_rel(data1, data2)

# calculate the Cohen's d between two samples
def cohend(d1, d2):
	n1, n2 = len(d1), len(d2)
	s1, s2 = var(d1, ddof=1), var(d2, ddof=1)
	s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
	u1, u2 = mean(d1), mean(d2)
	return (u1 - u2) / s
 
d = cohend(data1, data2)
print('Cohens d: %.3f' % d)

# regression model
model = ols('AVG_MASKED ~ C(ATLAS) + C(FWHM)', dataset).fit()
print(model.summary())

print(model.f_test([0, 1, -1, 0])) 

table = sm.stats.anova_lm(model, typ=2) # Type 2 ANOVA DataFrame

print(table)

#fdr correction
pvalue_list=()

stats = importr('stats')
p_adjust = stats.p_adjust(FloatVector(pvalue_list), method = 'BH')

# plotting
sns.catplot(x="ATLAS_FWHM", y="AVG_MASKED", kind="boxen",
            data=dataset.sort_values("ATLAS_FWHM"))

sns.boxenplot(data=dataset, x="ATLAS_FWHM", y="AVG_MASKED",
              order=["dypac_5mm", "difumo_5mm", "mist_5mm",
                     "dypac_8mm", "difumo_8mm", "mist_8mm"])

g = sns.FacetGrid(dataset, col="FWHM")
g.map(sns.boxenplot, "ATLAS", "AVG_MASKED", order=["dypac", "difumo", "mist"])

plt.show()
