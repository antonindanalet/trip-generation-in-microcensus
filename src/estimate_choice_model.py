import pandas as pd
import pyreadstat
from pathlib import Path
import geopandas
from choice_models.nb_trips.estimation.home_work import run_estimation_home_work
from utils_mtmc.get_mtmc_files import get_trips, get_zp, get_hh, get_hhp
from mtmc2015.utils2015.compute_confidence_interval import get_weighted_avg_and_std


def estimate_choice_model():
    # Generation of the data
    df_trips = get_trips_with_decomposed_round_trips()
    generate_data_file(df_trips)
    # Compute average number of trips
    # compute_average_number_of_trips()
    # Estimation
    data_file_directory = Path('../data/output/data/estimation/')
    data_file_name = 'nb_trips.csv'
    output_directory = '../data/output/models/nb_trips/WA/estimation/'
    run_estimation_home_work(data_file_directory, data_file_name, output_directory)


def compute_average_number_of_trips():
    output_directory = Path('../data/output/data/estimation/')
    data_file_name = 'nb_trips.csv'
    df_agg_trips = pd.read_csv(output_directory / data_file_name, sep=';')
    ''' Removing children 14 years old and younger. We assume that they do 0 trips to work. '''
    df_agg_trips.drop(df_agg_trips[df_agg_trips.age <= 14].index, inplace=True)
    ''' Removing unemployed people: They don't go to work '''
    df_agg_trips.drop(df_agg_trips[df_agg_trips.work_position == 0].index, inplace=True)
    weighted_avg_and_std = get_weighted_avg_and_std(df_agg_trips, weights='WP', list_of_columns=['WA'])
    weighted_avg = weighted_avg_and_std[0]['WA'][0]
    print('Weighted average of the number of home-based trips to work of employees:', weighted_avg)


def get_trips_with_decomposed_round_trips():
    """
    :return: A list of trips:
    - in Switzerland.
    - where round trips are decomposed in two parts,
    - including person and household information and
    - with a urban typology (Stadt-Land-Typologie) from the Swiss Federal Statical Office (FSO)
    """
    """ From the MTMC raw data:"""
    """ Important: we don't need the weights, just the number of trips. So we could decompose the round trips, without
    caring about the weights..."""
    # df_raw_trips = get_trips(2015)
    # df_raw_trips = decompose_round_trips_in_two_parts(df_raw_trips)
    # df_raw_trips = add_person_and_household_data(df_raw_trips)
    # Remove Saturday and Sunday
    # df_raw_trips = df_raw_trips[(df_raw_trips['tag'] != 6) & (df_raw_trips['tag'] != 7)]
    # df_trips = aggregate_trip_per_person(df_trips)
    # df_trips = add_urban_typology(df_trips)
    """ Directly from a cleaned version """
    folder_path = Path('../data/input/mtmc/2015/')
    df_trips, meta = pyreadstat.read_sav(str(folder_path / 'MZMV_2015_Kombiniert_Analysen.sav'))
    return df_trips


def generate_data_file(df_trips):
    """ This function takes as input the trips per person and per category, aggregate them per person and adds data
    about the person, the household and the spaptial typology. It returns nothing, but save the output as a data file
    for Biogeme.
    :param df_trips: Dataframe with the number of trips per person and per category
    :return: Nothing. The dataframe is saved as a CSV file (separator: tab) without NA values, to be used with Biogeme.
    """
    ''' Select days from Monday to Friday '''
    df_trips = df_trips[df_trips['tag'] <= 5]
    ''' Sum the number of trips per person using the dataset from the national transport model 
    (originally: data of the Mobility and Transport Microcensus - MTMC) '''
    df_agg_trips = df_trips.groupby('HHNR').agg({'WAA': 'sum',
                                                 'WASK': 'sum',
                                                 'WBS': 'sum',
                                                 'WBU': 'sum',
                                                 'WEk': 'sum',
                                                 'WEl': 'sum',
                                                 'WN': 'sum',
                                                 'WBgK': 'sum',
                                                 'WFk': 'sum',
                                                 'WFl': 'sum',
                                                 'AAW': 'sum',
                                                 'ASKW': 'sum',
                                                 'BSW': 'sum',
                                                 'BUW': 'sum',
                                                 'EkW': 'sum',
                                                 'ElW': 'sum',
                                                 'NW': 'sum',
                                                 'BgKW': 'sum',
                                                 'FkW': 'sum',
                                                 'FlW': 'sum',
                                                 'AS': 'sum',
                                                 'SA': 'sum',
                                                 'AEkFk': 'sum',
                                                 'EkFkA': 'sum',
                                                 'EkFkEkFk': 'sum',
                                                 'SS': 'sum'})
    ''' Group the number of trips to work '''
    df_agg_trips['WA'] = df_agg_trips['WAA'] + df_agg_trips['WASK']
    del df_agg_trips['WAA']
    del df_agg_trips['WASK']
    ''' All people doing more than 4 trips from home to work per day are considered as doing only 4 trips '''
    df_agg_trips.loc[df_agg_trips['WA'] > 4, 'WA'] = 4
    ''' Add the variables from the tables of the MTMC 2015 '''
    selected_columns_zp = ['gesl', 'alter', 'AMSTAT', 'zivil', 'nation', 'f20400a', 'f41610b', 'f41610a', 'f41651',
                           'f41610c', 'f41610d', 'f41610e', 'f41610g', 'f42100a', 'f42100b', 'f42100c', 'f42100d',
                           'f42100e', 'HAUSB', 'HHNR', 'ERWERB', 'f81300', 'f81400', 'WP', 'f40800_01', 'f41100_01',
                           'sprache', 'noga_08', 'f40900', 'f40901_02', 'f40903', 'A_X_CH1903', 'A_Y_CH1903', 'nation']
    df_zp = get_zp(2015, selected_columns_zp)
    df_agg_trips = pd.merge(df_agg_trips, df_zp, on='HHNR', how='left')
    selected_columns_hh = ['F20601', 'f30100', 'W_OeV_KLASSE', 'hhtyp', 'W_REGION', 'HHNR', 'W_BFS', 'hhgr',
                           'W_X_CH1903', 'W_Y_CH1903']
    df_hh = get_hh(2015, selected_columns_hh)
    df_agg_trips = pd.merge(df_agg_trips, df_hh, on='HHNR', how='left')
    ''' Add the distance between home and work places '''
    df_agg_trips_with_work_coord = df_agg_trips[df_agg_trips.A_X_CH1903 != -999]
    geodf_home = geopandas.GeoDataFrame(df_agg_trips_with_work_coord,
                                        geometry=geopandas.points_from_xy(df_agg_trips_with_work_coord.W_Y_CH1903,
                                                                          df_agg_trips_with_work_coord.W_X_CH1903),
                                        crs='epsg:21781')
    geodf_work = geopandas.GeoDataFrame(df_agg_trips_with_work_coord,
                                        geometry=geopandas.points_from_xy(df_agg_trips_with_work_coord.A_Y_CH1903,
                                                                          df_agg_trips_with_work_coord.A_X_CH1903),
                                        crs='epsg:21781')
    df_agg_trips.loc[df_agg_trips.A_X_CH1903 != -999, 'home_work_crow_fly_distance'] = geodf_home.distance(geodf_work)
    df_agg_trips['home_work_crow_fly_distance'].fillna(-999, inplace=True)
    df_agg_trips.drop(['W_Y_CH1903', 'W_X_CH1903', 'A_Y_CH1903', 'A_X_CH1903'], axis=1, inplace=True)
    ''' Add the data about the spatial typology '''
    path_to_typology = Path('../data/input/StadtLandTypologie/2015/Raumgliederungen.xlsx')
    df_typology = pd.read_excel(path_to_typology, sheet_name='Daten',
                                skiprows=[0, 2],  # Removes the 1st row, with information, and the 2nd, with links
                                usecols='A,G')  # Selects only the BFS commune number and the column with the typology
    df_agg_trips = pd.merge(df_agg_trips, df_typology, left_on='W_BFS', right_on='BFS Gde-nummer', how='left')
    df_agg_trips.drop('BFS Gde-nummer', axis=1, inplace=True)
    ''' Generate the variable about work position:
    Code FaLC in English     FaLC in German   NPVM                       Code used below
     0   Unemployed                                                      0
     1   CEO                 Geschäftsführer  qualifizierter Mitarbeiter 1
     11  business management Geschäftsleitung qualifizierter Mitarbeiter 1
     12  management          qualifizierte MA qualifizierter Mitarbeiter 1
     20  Employee            einfache MA      einfacher Mitarbeiter      2
     3   Apprentice          Lehrling                                    3 
     In the code below, -99 corresponds to no answer/does't know to the question about work position (if working) '''
    df_agg_trips.loc[df_agg_trips['f40800_01'].isin([1,  # MTMC: "Selbstständig Erwerbende(r)"
                                                     2,  # MTMC: Arbeitnehmer in AG/GmbH, welche IHNEN selbst gehört
                                                     3]),  # MTMC: Arbeitnehmer im Familienbetrieb von Haushaltsmitglied
                     'work_position'] = 1  # NPVM: Qualifiziert
    df_agg_trips.loc[(df_agg_trips['f40800_01'] == 4) &  # MTMC: Arbeitnehmer bei einem sonstigen Unternehmen
                     (df_agg_trips['f41100_01'] == 1),  # MTMC: Angestellt ohne Cheffunktion
                     'work_position'] = 2  # NPVM: Einfach
    df_agg_trips.loc[(df_agg_trips['f40800_01'] == 4) &  # MTMC: Arbeitnehmer bei einem sonstigen Unternehmen
                     (df_agg_trips['f41100_01'].isin([2,  # MTMC: Angestellt mit Chefposition
                                                      3])),  # MTMC: Angestellt als Mitglied von der Direktion
                     'work_position'] = 1  # SynPop: Qualifiziert
    df_agg_trips.loc[df_agg_trips['f40800_01'] == 5,  # MTMC: Lehrling
                     'work_position'] = 3  # NPVM: Apprentice
    df_agg_trips.loc[df_agg_trips['f41100_01'] == 3,  # MTMC: Angestellt als Mitglied von der Direktion
                     'work_position'] = 1  # NPVM: Qualifiziert
    df_agg_trips.loc[df_agg_trips['f40800_01'] == -99,  # MTMC: Nicht erwerbstätig
                     'work_position'] = 0  # NPVM: Unemployed
    df_agg_trips.loc[(df_agg_trips['f40800_01'] == 4) & (df_agg_trips['f41100_01'].isin([-98, -97])),
                     'work_position'] = -99
    del df_agg_trips['f40800_01']
    del df_agg_trips['f41100_01']
    ''' Add data about other members of the household '''
    selected_columns_hhp = ['HHNR', 'alter']
    df_hhp = get_hhp(2015, selected_columns=selected_columns_hhp)
    # Number of children 15 years old or less
    df_hhp['less_than_15'] = df_hhp.apply(lambda x: 1 if x['alter'] <= 15 else 0, axis=1)
    df_hhp_less_than_15_per_hh = df_hhp[['HHNR', 'less_than_15']].groupby(['HHNR']).sum()
    df_agg_trips = pd.merge(df_agg_trips, df_hhp_less_than_15_per_hh, left_on='HHNR', right_on='HHNR', how='left')
    # Number of children 6 years old or less
    df_hhp['less_than_6'] = df_hhp.apply(lambda x: 1 if x['alter'] <= 6 else 0, axis=1)
    df_hhp_less_than_6_per_hh = df_hhp[['HHNR', 'less_than_6']].groupby(['HHNR']).sum()
    df_agg_trips = pd.merge(df_agg_trips, df_hhp_less_than_6_per_hh, left_on='HHNR', right_on='HHNR', how='left')
    # Rename the variables
    df_agg_trips = df_agg_trips.rename(columns={'gesl': 'sex',
                                                'alter': 'age',
                                                'AMSTAT': 'labor_market_status',
                                                'zivil': 'civil_status',
                                                'f20400a': 'driving_license',
                                                'f41610b': 'halbtax_ticket',
                                                'f41610a': 'GA_ticket',
                                                'f41651': 'GA_ticket_first_or_second',
                                                'f41610c': 'Verbund_Abo',
                                                'f41610d': 'Strecken_Abo',
                                                'f41610e': 'Gleis_7',
                                                'f41610g': 'anderes_Abo',
                                                'f42100a': 'bike_avail',
                                                'f42100b': 'moped_avail',
                                                'f42100c': 'small_moto_avail',
                                                'f42100d': 'moto_avail',
                                                'f42100e': 'car_avail',
                                                'HAUSB': 'highest_educ',
                                                'F20601': 'hh_income',
                                                'f30100': 'nb_car_in_hh',
                                                'W_OeV_KLASSE': 'public_transport_connection_quality_ARE',
                                                'hhtyp': 'hh_type',
                                                'W_REGION': 'region',
                                                'Stadt/Land-Typologie': 'city_typology',
                                                'f81300': 'home_office',
                                                'f81400': 'percentage_home_office',
                                                'hhgr': 'hh_size',
                                                'sprache': 'language',
                                                'f40900': 'full_part_time_job',
                                                'f40901_02': 'percentage_first_part_time_job',
                                                'f40903': 'percentage_second_part_time_job',
                                                'less_than_15': 'nb_less_than_15_in_hh',
                                                'less_than_6': 'nb_less_than_6_in_hh',
                                                'BSTELL': 'work_position'})
    ''' Save the file '''
    output_directory = Path('../data/output/data/estimation/')
    data_file_name = 'nb_trips.csv'
    df_agg_trips.to_csv(output_directory / data_file_name, sep=';', index=False)
