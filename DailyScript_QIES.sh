# Runs Front End over 3 transactions
# Combines indvidiual output Transaction Summary Files into a Merged Transaction Summary File 
# Runs Back End using The new Merged Transaction Summary File 

# Variables:
# $1 = argument to run this script, it indicates the Day being run
# transaction = .txt input file
# output = .txt individual transaction summary file 

# Purpose:
# Runs transaction for front end with different inputs
for transaction in $1/Inputs/* ;
do
    # Runs Front End system, outputs Transaction Summary File for each transaction seperately 
    python ./FrontEndTest.py ValidServicesFile.txt ./$1/Outputs/TransactionSummaryFile"$(basename "$transaction")" < ./"$transaction" >> FrontEnd.log
done

# Purpose:
# Merges Transaction files
for output in $1/Outputs/* ;
do 
    (cat ./"$output"; echo) >> MergedTransactionSummaryFile.txt
done

# Executes Back End
python ./BackEndTest.py CentralServicesFile.txt MergedTransactionSummaryFile.txt CentralServicesFile.txt ValidServicesFile.txt >> BackEnd.log

# Empties Merged Transaction Summary File for next day
> MergedTransactionSummaryFile.txt

