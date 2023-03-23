#!/bin/python3

"""
author: Marilina Cahtcarth [mcathcarth@gmail.com]
date: 03-21-2023

"""

import os
import pandas as pd
import sklearn.metrics as metrics
import math
import shutil
import matplotlib.pyplot as plt

# Define the common path for the directories
#path = '/home/mac/research/simulations/2023/silica/multi-parameters/sim_1227/compare/'
path = ''

# If the path is not previously defined, ask the user to enter it by terminal
if path == '':
     valid_path = False

     while not valid_path:
        # Ask the user to enter the path to the directory 'compare'
        path = input("\n  Enter the path to the directory 'compare':\n\n    ")

        # Check if the path is valid
        if os.path.isdir(path) and (path.endswith('compare/') or path.endswith('compare')):
             valid_path = True
             print("\n The path is valid.")
        else:
            # Print an error message if the path is invalid
            print("\n The path is invalid. Please enter a valid path.")

#verify that the directory ends with '/', if not, add it
if not path.endswith('/'):
     path = path + '/'

## Create an analysis directory

# Define the directory name and path
directory_name = 'analysis/'
directory_path = path + directory_name

# Create the directory
try:
    os.mkdir(directory_path)
    print("\n The analysis directory created successfully!")
except OSError as error:
    print("\n The analysis directory creation failed: %s" % error)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Define the list of salt concentrations
csalt = ['022', '055', '109', '216']

# Create an empty list to store the directory names
directories = []

# Create the full directory path and add it to the list
for name in csalt:
    directory = os.path.join(path, name + '/')
    directories.append(directory)

# Loop through each directory in the list and read the CSV files inside it
for directory in directories:
    # Get a list of CSV files in the directory
    csv_files = [file for file in sorted(os.listdir(directory)) if file.endswith('.csv')]

    # Create an empty list to store only the simulation files (filenames with 6 parameters separated by '_')
    sim_files = []

    # Create an empty DataFrame to store the columns from CSV files
    sim_df = pd.DataFrame()

# Loop through each CSV file and add it to the DataFrame
    id = -1

    for csv_file in csv_files:
            # Split the CSV filename into parameters
            params = os.path.splitext(csv_file)[0].split('_')
            # Create the name of each column listing the simulations
            if id >= 0:
                 sim_id = str(id)
            # Add the columns to the dataframe
            if sim_df.empty:
                sim_df = pd.read_csv(directory + csv_file, header=0, sep = ',', names=['pH', 'SCD'])    #experimental file
            else:
                new_df = pd.read_csv(directory + csv_file, header=0, sep = ',', names=['pH', 'sim'])
                sim_df = sim_df.join(new_df.set_index('pH'), rsuffix='_' + sim_id, on='pH')

            id += 1

        # Create a list of valid files (filenames with 6 parameters)
            if len(params) == 6:
                 sim_files.append(csv_file)

        # Create empty lists to store each parameter
            perA = []
            pKA = []
            pKB = []
            wA = []
            wB = []
            pKNa = []

        # Loop through each simulation file, get the parameters and add them to the corresponding list
            for file in sim_files:
            # Split the filename into parameters
                parameters = os.path.splitext(file)[0].split('_')

            # Add the parameters to the lists
                perA.append(parameters[0])
                pKA.append(parameters[1])
                pKB.append(parameters[2])
                wA.append(parameters[3])
                wB.append(parameters[4])
                pKNa.append(parameters[5])

    sim_df = sim_df.rename(columns={'sim': 'sim_0'})        # Rename the first simulation column
    #print(sim_df)

# Create a dictionary that maps the parameter names to the values
    params_dict = {'%A': perA,
                 'pK-A': pKA,
                 'pK-B': pKB,
                 'w-A': wA,
                 'w-B': wB,
                 'pKNa': pKNa}
    
# Create a parameter DataFrame with the dictionary
    params_df = pd.DataFrame(params_dict)
    #print(params_df)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# Compare the different theoretical curves with an experimental curve:

## Regression Accuracy Metrics

        # Mean Squared Error (MSE)
        # Mean Absolute Error (MAE)
        # Root Mean Squared Error (RMSE)
        # R-squared (R²)

    # MSE, MAE, RMSE: lower value --> better the fit
    # R²: higher value --> better the fit

    # Create a list with the metrics to use
    metrics_ls = ['MAE', 'MSE', 'RMSE', 'R2']

    # Create an empty DataFrame to store the results of the metrics
    df_metrics = pd.DataFrame(columns = metrics_ls)

    # Calculate the metrics for each column of the simulations dataframe
    for i in sim_df.loc[:, sim_df.columns!='pH'].columns[:]:                    # Exclude column pH
         MAE = metrics.mean_absolute_error(sim_df['SCD'],sim_df[i])             # using sklearn.metrics
         MSE = metrics.mean_squared_error(sim_df['SCD'],sim_df[i])              # using sklearn.metrics 
         RMSE = math.sqrt(MSE)                                                  # using math
         R2 = metrics.r2_score(sim_df['SCD'],sim_df[i])                         # using sklearn.metrics  
         df_metrics.loc[i] = [MAE, MSE, RMSE, R2] 
    
    df_metrics = df_metrics.drop(df_metrics.index[0])                      # delete the experimental row (from the SCD column)
    df_metrics.index.name = 'sim'                                          # rename index column
    df_metrics = df_metrics.reset_index(drop=False)                        # create a new column with the index
    #print(df_metrics)

## Save the dataframes in .csv files

    print()

# Define the output file names
    sim_output_file = os.path.join(directory, 'df_SCD-pH.csv')              # Simulation DataFrames
    param_output_file = os.path.join(directory, 'df_params.csv')            # Parameters DataFrames
    metrics_output_file = os.path.join(directory, 'df_metrics.csv')         # Metrics DataFrames

# Save the DataFrame to a CSV file
    sim_df.to_csv(sim_output_file, index=False)
    params_df.to_csv(param_output_file, index=False)
    df_metrics.to_csv(metrics_output_file, index=False)
    
# Print message
    print(f' The files {os.path.basename(sim_output_file)}, {os.path.basename(param_output_file)} and' ,
          f'{os.path.basename(metrics_output_file)}' , 
          f'were created in:\n  {directory}\n')

## Move the files to the analysis directory and rename them

    # Create a list of new files to move
    df_files = [os.path.basename(sim_output_file), os.path.basename(param_output_file), os.path.basename(metrics_output_file)]
    
    # Create an empty list to store the new filenames
    cs_df_files = []

    # Iterate over the files in the source directory
    for filename in df_files:
        # Construct the new filename with the source directory name
        new_filename = directory.split("/")[-2] + "_" + filename
    
        # Construct the full paths for the source and destination files
        src_file = os.path.join(directory, filename)
        dest_file = os.path.join(directory_path, new_filename)
    
        # Move the file to the destination directory and rename it
        shutil.move(src_file, dest_file)

        # Save the new filename in a list
        cs_df_files.append(new_filename)
        #print('File %s moved successfully!' % new_filename)

# Print message
    print(' The files', ', '.join(cs_df_files[:-1]), 'and', cs_df_files[-1], 'were moved to:\n  ', directory_path)

print()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

### Create a DataFrame for each metric (with a column for each salt concentration)

## Load the dataframes for each salt concentration

# Create an empty dictionary to store the dataframes
df_dict = {}

# Iterate over the CSV prefixes (salt concentration) and read the CSV files
for prefix in csalt:
    file_path = os.path.join(directory_path, f"{prefix}_df_metrics.csv")
    df_dict[prefix] = pd.read_csv(file_path)

## Create new dataframes with the columns from each prefix

# Create an empty list to store the dataframes filenames
file_name_ls = []

# Iterate over the metrics names and create the corresponding dataframe
for metric in metrics_ls:
    metric_df = pd.DataFrame({
        'sim': df_dict['022']['sim'],
        '022': df_dict['022'][metric],
        '055': df_dict['055'][metric],
        '109': df_dict['109'][metric],
        '216': df_dict['216'][metric]
    })

    # Add a new column that is the sum of the last 4 columns
    last_4cols = metric_df.columns[-4:]
    metric_df['sum'] = metric_df[last_4cols].sum(axis=1)

    # Sort the simulations from best to worst
    if metric == 'R2':                                                      # Sort from highest to lowest
        metric_df = metric_df.sort_values('sum', ascending=False)
    else:                                                                   # Sort from lowest to highest
        metric_df = metric_df.sort_values('sum')

    # Define the filename for the CSV file and add it to the list
    file_name = f"{metric}.csv"

    # Save the file name in a list to create the message
    file_name_ls.append(file_name)

    # Save the dataframe to a CSV file
    metric_df.to_csv(os.path.join(directory_path, file_name), index=False)

    #print(metric_df)

# Print message
print(' The files', ', '.join(file_name_ls[:-1]), 'and', file_name_ls[-1], 
      'were created in the directory:\n  ', directory_path, '\n')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

## Ask the user if they want to do the analysis

do_analysis = True                                  # Keep doing the analysis until the user indicates otherwise

# Initialize a second response that will be used after the first full loop
sec_answer = ''

# Start loop for analysis
while do_analysis:
    correct_answer = False                          # Keep asking the user to enter an answer until they type a valid one

    # Inner loop to validate user's answer
    while not correct_answer:
        if sec_answer == '':                                                                      # First iteration of the loop
            # Ask user if they want to analyze results now
            answer = input(' Do you want to analyze the results now?: (y/n)    ').lower()         # convert to lowercase
        else:
            # Use the answer from the previous iteration
            answer = sec_answer

        if answer == 'y' or answer == 'yes':
            correct_answer = True                   # The user gave a correct answer
            # Create a list of valid options
            num = ['1', '2', '3', '4']
            correct_selec = False                   # Keep asking the user to select a metric until a valid selection is made

            # Inner loop to validate the chosen metric
            while not correct_selec:
                # Ask the user to select a metric and display the options
                chosen_id = input('\n Choose a metric:\n\n' +
                                    '    1. MAE\n' +
                                    '    2. MSE\n' +
                                    '    3. RMSE\n' +
                                    '    4. R²\n' +
                                    '\n select the corresponding number: ')
                if chosen_id not in num:
                    # Print an error message
                    print("\n Invalid selection, try again")
                else:
                    correct_selec = True            # User selected a valid metric
                    # Generate the index to search the lists
                    chosen_id = int(chosen_id) - 1
                    # Select metric from index
                    chosen_metric = metrics_ls[chosen_id]
                    print("\n - - - - - - - - - - - - - - - ", chosen_metric ," - - - - - - - - - - - - - - -\n")

                    # Metric description

                    MAE_desc = (' Mean Absolute Error (MAE): This metric measures the average absolute difference between the '
                                'predicted and actual values. It is less sensitive to outliers than MSE. A lower MAE indicates ' 
                                'better accuracy\n')

                    MSE_desc = (' Mean Squared Error (MSE): This metric measures the average squared difference between the '
                                'predicted and actual values. A lower MSE indicates better accuracy.\n')
                    
                    RMSE_desc = (' Root Mean Squared Error (RMSE): This metric measures the square root of the average squared '
                                 'difference between the predicted and actual values. It is similar to MSE but has the advantage '
                                 'of being in the same units as the target variable. A lower RMSE indicates better accuracy\n')
                    
                    R2_desc = (' R-squared (R²): This metric measures the proportion of the variance in the dependent variable '
                               'that is explained by the independent variable(s) in a regression model. A higher value indicates ' 
                               'a better fit of the model to the data.\n')

                    description_ls = [MAE_desc, MSE_desc, RMSE_desc, R2_desc]

                    # Print the description of the chosen metric
                    print(description_ls[chosen_id])
                    
                    # Read the index DataFrame of the chosen metric
                    chosen_file_ix = pd.read_csv(os.path.join(directory_path, f"{chosen_metric}.csv"))
                    #print(chosen_file)

                    # Report which simulation generates the best results according to the chosen metric
                    print(' The simulation that obtains the best results according to the', chosen_metric,
                          'metric is:', chosen_file_ix['sim'].iloc[0], '\n')
                    
                    # Read the Metric DataFrame of the chosen metric
                    chosen_file = pd.read_csv(os.path.join(directory_path, f"{chosen_metric}.csv"))
                    #print(chosen_file

                    # Define the list of salt concentrations
                    conc = [' 22 mM', ' 55 mM', '109 mM', '216 mM']

                    # Display metric results for each salt concentration
                    print(' The results for each salt concentration are:\n')
                    s = 0
                    for cs in csalt:
                        print(f"    {conc[s]}: {chosen_file[cs].iloc[0]}")
                        s += 1

                    # Best index for the chosen metric
                    ix = int(chosen_file_ix['sim'].iloc[0].split('_')[1])
                    
                    # Create a parameter list from dictionary keys
                    params_ls = []
                    for key in params_dict.keys():
                        params_ls.append(key)

                    # Display parameters of best simulation
                    print('\n The simulation parameters are:\n')
                    for param in params_ls:
                        if len(param) == 2:
                            print_par = '  ' + param
                        elif len(param) == 3:
                            print_par = ' ' + param
                        else:
                            print_par = param
                        print(f"    {print_par}: {params_df[param].iloc[ix]}")
                    
                    ## Ask the user if they want to see the graphics of the best simulation
                    cor_ans = False                                               # Keep asking until a valid response
                    while not cor_ans:
                        thi_answer = input('\n Do you want to see the graph of the best simulation?: (y/n)    ').lower()

                        if thi_answer == 'y' or thi_answer == 'yes':
                            cor_ans = True                                        # The user gave a correct answer

                            ## Create the graph

                            # Load dataframes for each salt concentration
                            df22 = pd.read_csv(os.path.join(directory_path, '022_df_SCD-pH.csv'))
                            df55 = pd.read_csv(os.path.join(directory_path, '055_df_SCD-pH.csv'))
                            df109 = pd.read_csv(os.path.join(directory_path, '109_df_SCD-pH.csv'))
                            df216 = pd.read_csv(os.path.join(directory_path, '216_df_SCD-pH.csv'))

                            # Define the plot colors
                            colors = ['black', 'green', 'red', 'blue']

                            # Loop through each dataframe and plot the data
                            for i, df in enumerate([df22, df55, df109, df216]):
                                # Extract data for plotting
                                x = df.iloc[:, 0]
                                y_exp = df.iloc[:, 1]
                                y_theo = df.iloc[:, (ix + 2)]
                                
                                # Plot the experimental data with dots and theoretical data with continuous lines
                                plt.plot(x, y_exp, '.', color=colors[i], label=f'Exp. {conc[i]}')
                                plt.plot(x, y_theo, '-', color=colors[i], label=f'Theo. {conc[i]}')

                            # Add labels, title, and legend
                            plt.xlabel('pH')
                            plt.ylabel('Surface charge density [C/m²]')
                            title = 'Experimental and Theoretical (Simulation ' + str(ix) + ') Curves'
                            plt.title(title)
                            plt.legend()

                            # Show the plot
                            plt.show()

                            # Save the plot as a PNG file
                            pt_name = 'SCD_vs_pH_sim' + str(ix)
                            plt.savefig(pt_name)

                        elif thi_answer == 'n' or thi_answer == 'no':
                            cor_ans = True                                        # The user gave a correct answer
                        
                        else:
                            print('\n Wrong answer, try again')                      # The user gave an invalid answer

                    # Ask user if they want to analyze the results of another metric
                    corr_sec = False
                    while not corr_sec:
                        sec_answer = input('\n Do you want to analyze the results of another metric?: (y/n)    ').lower()
                        if sec_answer == 'y' or sec_answer == 'yes' or sec_answer == 'n' or sec_answer == 'no':
                            corr_sec = True
                        else:
                            print('\n Wrong answer, try again')                      # The user gave an invalid answer                  
          
        elif answer == 'n' or answer == 'no':
            print('- Exit -')
            correct_answer = True                   # The user gave a correct answer
            do_analysis = False                     # User doesn't want to analyze results now

        else:
            # The user gave an invalid answer
            print('Wrong answer, try again')

# Endprogram

# - Mac -