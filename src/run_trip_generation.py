import pandas as pd
from pathlib import Path
# from choice_models.home_office.logit_home_office import estimate_choice_model_home_office
import descriptive_statistics.from_microcensus
# import descriptive_statistics.from_synpop
from validate_choice_model import validate_choice_model
from estimate_choice_model import estimate_choice_model
# from apply_model_to_synthetic_population import apply_model_to_synthetic_population, \
#     validate_model_with_synthetic_population
# from calibrate_the_cuts import calibrate_the_cuts_from_microcensus, calibrate_the_cuts_from_synthetic_population


def run_trip_generation():
    estimate_choice_model()
    # validate_choice_model()
    # estimate_choice_model_home_office()
    # betas = calibrate_the_cuts_from_microcensus()
    # validate_model_with_synthetic_population(betas)
    # betas = calibrate_the_cuts_from_synthetic_population(betas)
    # apply_model_to_synthetic_population(betas)
    # compute_descriptive_statistics()
    # predicting_2015_with_2010()
    # # forecasting_2050()


def compute_descriptive_statistics():
    descriptive_statistics.from_microcensus.get_stats()


def add_person_and_household_data(df_trips):
    selected_columns = ['HHNR', 'tag']
    df_zp = get_zp(2015, selected_columns=selected_columns)
    df_trips = pd.merge(df_trips, df_zp, on='HHNR', how='left')
    return df_trips


def decompose_round_trips_in_two_parts(df_trips):
    print('Start:', len(df_trips), 'trips (MZMV 2015)')
    # Identify round trips
    df_round_trips = df_trips[((df_trips['S_X'] == df_trips['Z_X']) & (df_trips['S_Y'] == df_trips['Z_Y'])) |
                              (df_trips['wzweck2'] == 3)]
    if len(df_round_trips) != 14135:
        print('WARNING! Here:', len(df_round_trips) + "'", 'in NPVM:', 14135)
    # Join data about coordinates of the point the most far way from starting point
    # Join trip leg data
    # Delete round trips that correspond to no trip leg (-15 round trips)
    return df_trips


def add_urban_typology(df_trips):
    # Read data from the Swiss Federal Statistical Office by commune
    folder_path = Path('../data/input/StadtLandTypologie/2015/')
    df_typology = pd.read_excel(folder_path / 'Raumgliederungen.xlsx', sheet_name='Daten', header=1)
    df_typology = df_typology.iloc[1:]
    df_typology.drop(['Gemeindename', 'Kantons-nummer', 'Kanton', 'Bezirks-nummer', 'Bezirksname'],
                     axis=1, inplace=True)
    df_trips = pd.merge(df_trips, df_typology, left_on='W_BFS', right_on='BFS Gde-nummer', how='left')
    return df_trips


if __name__ == '__main__':
    run_trip_generation()
