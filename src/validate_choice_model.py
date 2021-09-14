import pandas as pd
from pathlib import Path
from choice_models.nb_trips.estimation.home_work import run_estimation_home_work
from choice_models.nb_trips.apply_home_work_model_to_microcensus import apply_home_work_model_to_microcensus
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std


def validate_choice_model():
    # Read the data used for estimation
    df_nb_trips = get_nb_trips()
    # Save 80% of the data for estimation and 20% of the data for simulation for simulation (and shuffles the data set)
    save_slices(df_nb_trips)
    # Estimate the model on 80% of the data
    data_file_directory_for_estimation = Path('../data/output/data/validation/estimation/')
    data_file_name_for_estimation = 'nb_trips80.csv'
    output_directory_for_estimation = Path('../data/output/models/nb_trips/WA/validation/estimation/')
    run_estimation_home_work(data_file_directory_for_estimation, data_file_name_for_estimation,
                             output_directory_for_estimation)
    # Simulate the model on 20% of the data
    data_file_directory_for_simulation = Path('../data/output/data/validation/simulation/')
    data_file_name_for_simulation = 'nb_trips20.csv'
    output_directory_for_simulation = Path('../data/output/models/nb_trips/WA/validation/simulation/')
    output_file_name_for_simulation = 'nb_trips20_with_predicted_nb_trips.csv'

    path_to_estimation_folder = Path('../data/output/models/nb_trips/WA/validation/estimation/')
    apply_home_work_model_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                                         output_directory_for_simulation, output_file_name_for_simulation,
                                         path_to_estimation_folder)

    # Compute the number of trips to work in the data and in the simulation
    compute_nb_trips()


def compute_nb_trips():
    ''' Get the data '''
    simulation_results_directory = Path('../data/output/models/nb_trips/WA/validation/simulation/')
    data_file_name = 'nb_trips20_with_predicted_nb_trips.csv'
    df_persons = pd.read_csv(simulation_results_directory / data_file_name, sep=';')
    ''' Compare the number of trips in the total population '''
    print('--- Total population ---')
    print('Observed average number of trips:', df_persons['WA'].mean())
    df_persons['expected nb of trips'] = df_persons['1'] + 2 * df_persons['2'] + 3 * df_persons['3'] + \
                                         4 * df_persons['4']
    print('Predicted average number of trips:', df_persons['expected nb of trips'].mean())
    ''' Compare the number of trips among employees '''
    print('--- Employees ---')
    df_persons_employees = df_persons[(df_persons['work_position'] == 2)]
    print('Number of observations:', len(df_persons_employees))
    weighted_avg_and_std_observed = get_weighted_avg_and_std(df_persons_employees, weights='WP', list_of_columns=['WA'])
    avg_nb_trips_observed = round(weighted_avg_and_std_observed[0]['WA'][0], 3)
    std_nb_trips_observed = round(weighted_avg_and_std_observed[0]['WA'][1], 3)
    print('Observed average number of trips:', avg_nb_trips_observed, '(+/-' + str(std_nb_trips_observed) + ')')
    weighted_avg_and_std_predicted = get_weighted_avg_and_std(df_persons_employees,
                                                              weights='WP', list_of_columns=['expected nb of trips'])
    avg_nb_trips_predicted = round(weighted_avg_and_std_predicted[0]['expected nb of trips'][0], 3)
    std_nb_trips_predicted = round(weighted_avg_and_std_predicted[0]['expected nb of trips'][1], 3)
    print('Predicted average number of trips:', avg_nb_trips_predicted, '(+/-' + str(std_nb_trips_predicted) + ')')
    ''' Compare the number of trips in the population group PG 1 '''
    print('--- Employees, younger than 24, with car available, without PT subscription ---')
    # Add a column for having any kind of public transport subscription
    df_persons.loc[(df_persons['GA_ticket'] == -99) | (df_persons['Verbund_Abo'] == -99), 'PT_subscription'] = -99
    df_persons.loc[(df_persons['GA_ticket'] == 1) | (df_persons['Verbund_Abo'] == 1), 'PT_subscription'] = 1
    df_persons.loc[(df_persons['GA_ticket'] == 2) & (df_persons['Verbund_Abo'] == 2), 'PT_subscription'] = 0
    df_persons_employees_PG1 = df_persons[(df_persons['work_position'] == 2) &
                                          (df_persons['age'] <= 24) &
                                          (df_persons['PT_subscription'] == 0) & (df_persons['car_avail'].isin([1, 2]))]
    print('Number of observations:', len(df_persons_employees_PG1))
    weighted_avg_and_std_observed = get_weighted_avg_and_std(df_persons_employees_PG1,
                                                             weights='WP', list_of_columns=['WA'])
    avg_nb_trips_observed = round(weighted_avg_and_std_observed[0]['WA'][0], 3)
    std_nb_trips_observed = round(weighted_avg_and_std_observed[0]['WA'][1], 3)
    print('Observed average number of trips:', avg_nb_trips_observed, '(+/-' + str(std_nb_trips_observed) + ')')
    weighted_avg_and_std_predicted = get_weighted_avg_and_std(df_persons_employees_PG1,
                                                              weights='WP', list_of_columns=['expected nb of trips'])
    avg_nb_trips_predicted = round(weighted_avg_and_std_predicted[0]['expected nb of trips'][0], 3)
    std_nb_trips_predicted = round(weighted_avg_and_std_predicted[0]['expected nb of trips'][1], 3)
    print('Predicted average number of trips:', avg_nb_trips_predicted, '(+/-' + str(std_nb_trips_predicted) + ')')


def save_slices(df_nb_trips):
    # Shuffle the data set (sampling the full fraction of the data, i.e., all data)
    df_nb_trips = df_nb_trips.sample(frac=1)
    # Save 80% of the data for estimation
    estimation_output_directory = Path('../data/output/data/validation/estimation/')
    estimation_data_file_name = 'nb_trips80.csv'
    number_of_observations = len(df_nb_trips)
    first_80_percent_of_observations = round(0.8 * number_of_observations)
    df_nb_trips.head(first_80_percent_of_observations).to_csv(estimation_output_directory / estimation_data_file_name,
                                                              sep=';', index=False)
    # Save the remaining 20% of the data for simulation
    last_20_percent_of_observations = number_of_observations - first_80_percent_of_observations
    simulation_output_directory = Path('../data/output/data/validation/simulation/')
    simulation_data_file_name = 'nb_trips20.csv'
    df_nb_trips.tail(last_20_percent_of_observations).to_csv(simulation_output_directory / simulation_data_file_name,
                                                             sep=';', index=False)


def get_nb_trips():
    full_sample_directory = Path('../data/output/data/estimation/')
    data_file_name = 'nb_trips.csv'
    df_nb_trips = pd.read_csv(full_sample_directory / data_file_name, sep=';')
    return df_nb_trips
