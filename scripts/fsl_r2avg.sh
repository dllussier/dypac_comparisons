#!/bin/bash
#SBATCH --account={account}
#SBATCH --job-name=fslavg
#SBATCH --output=output_error/fslavg_%j.out
#SBATCH --error=output_error/fslavg_%j.err
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
#SBATCH --mail-type=FAIL
#SBATCH --mail-user={email}
#SBATCH --time=120:00:00
#SBATCH --cpus-per-task=10
#SBATCH --mem=40G

pwd; hostname; date

module load StdEnv/2020
module load gcc/9.3.0
module load fsl/6.0.3


for resolution in 64c_256s_5mm 64c_256s_8mm 64c_512s_5mm 64c_512s_8mm 128c_512s_5mm 128c_512s_8mm 128c_1024s_5mm 128c_1024s_8mm 256c_1024s_5mm 256c_1024s_8mm  
do

	for mask in dypac schaefer yeo mist shen gordon smith difumo_256 difumo_512 difumo_1024
	do

		i="0"

		while [ $i -lt  937 ]
		do
		
			fslstats r2maps/dev_aging_sz/${resolution}/${mask}_${i}.nii.gz -m -M >> fsl_r2avg/${resolution}_${mask}.txt

			i=$[$i+1]
			
		done
   
    sed 's/ \+/,/g' fsl_r2avg/${resolution}_${mask}.txt > fsl_r2avg/${resolution}_${mask}.csv
    
	done
done

date
