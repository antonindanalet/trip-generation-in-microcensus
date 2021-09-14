import pandas as pd
from pathlib import Path
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.distributions as dist
import biogeme.messaging as msg
from biogeme.expressions import Beta, Variable, Derive, log, Elem, DefineVariable
import biogeme.models as models
import biogeme.results as res
import os


def apply_home_work_model_to_microcensus(data_file_directory_for_simulation, data_file_name_for_simulation,
                                         output_directory_for_simulation, output_file_name_for_simulation,
                                         path_to_estimation_folder, betas=None):
    """
    :author: Antonin Danalet, based on the example by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    An ordinal logit model of the number of trips from home to work.
    Seven ordered alternatives: 0, 1, 2, 3, 4+ trips from home to work."""

    # Read the data
    df = pd.read_csv(data_file_directory_for_simulation / data_file_name_for_simulation, ';')
    database = db.Database(data_file_name_for_simulation, df)

    # The Pandas data structure is available as database.data. Use all the
    # Pandas functions to investigate the database
    # print(database.data.describe())

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    ''' Removing children 14 years old and younger. We assume that they do 0 trips to work. '''
    database.data.drop(database.data[database.data.age <= 14].index, inplace=True)

    # Parameters to be estimated
    # b_car_avail_employees = Beta('b_car_avail_employees', 0, None, None, 1)
    # b_car_avail_na = Beta('b_car_avail_na', 0, None, None, 1)
    # b_ga_employees = Beta('b_ga_employees', 0, None, None, 1)
    # b_verbund = Beta('b_verbund', 0, None, None, 1)
    # b_urban = Beta('b_urban', 0, None, None, 1)
    # b_rural = Beta('b_rural', 0, None, None, 1)
    # b_intermediate = Beta('b_intermediate', 0, None, None, 1)

    # b_single_household_employees = Beta('b_single_household_employees', 0, None, None, 1)
    # b_couple_without_children_employees = Beta('b_couple_without_children_employees', 0, None, None, 1)
    b_couple_with_children = Beta('b_couple_with_children', 0, None, None, 0)
    # b_single_parent_with_children_employees = Beta('b_single_parent_with_children_employees', 0, None, None, 1)
    # b_adults_with_elderly_care = Beta('b_adults_with_elderly_care', 0, None, None, 1)
    # b_employees = Beta('b_employees', 0, None, None, 1)
    b_executives = Beta('b_executives', 0, None, None, 0)

    b_studying = Beta('b_studying', 0, None, None, 0)
    # b_inactive = Beta('b_inactive', 0, None, None, 1)
    # b_active_without_known_work_percentage = Beta('b_active_without_known_work_percentage', 0, None, None, 1)

    # b_public_transport_connection_quality_are_a = Beta('b_public_transport_connection_quality_are_a', 0, None, None, 1)
    # b_public_transport_connection_quality_are_b = Beta('b_public_transport_connection_quality_are_b', 0, None, None, 1)
    # b_public_transport_connection_quality_are_c = Beta('b_public_transport_connection_quality_are_c', 0, None, None, 1)
    # b_public_transport_connection_quality_are_d = Beta('b_public_transport_connection_quality_are_d', 0, None, None, 1)
    b_public_transport_connection_quality_are_na = Beta('b_public_transport_connection_quality_are_na', 0, None, None,
                                                        0)
    # B_hh_income_na = Beta('B_hh_income_na', 0, None, None, 1)
    # B_hh_income_less_than_2000 = Beta('B_hh_income_less_than_2000', 0, None, None, 1)
    # B_hh_income_2000_to_4000 = Beta('B_hh_income_2000_to_4000', 0, None, None, 1)
    # B_hh_income_4001_to_6000 = Beta('B_hh_income_4001_to_6000', 0, None, None, 1)
    # B_hh_income_6001_to_8000 = Beta('B_hh_income_6001_to_8000', 0, None, None, 1)
    # B_hh_income_8001_to_10000 = Beta('B_hh_income_8001_to_10000', 0, None, None, 1)
    # B_hh_income_10001_to_12000 = Beta('B_hh_income_10001_to_12000', 0, None, None, 1)
    # B_hh_income_12001_to_14000 = Beta('B_hh_income_12001_to_14000', 0, None, None, 1)
    # B_hh_income_14001_to_16000 = Beta('B_hh_income_14001_to_16000', 0, None, None, 1)
    # B_hh_income_more_than_16000 = Beta('B_hh_income_more_than_16000', 0, None, None, 1)
    # B_no_post_school_education = Beta('B_no_post_school_education', 0, None, None, 1)
    # B_secondary_education = Beta('B_secondary_education', 0, None, None, 1)
    b_tertiary_education_employees = Beta('b_tertiary_education_employees', 0, None, None, 0)
    # B_university = Beta('B_university', 0, None, None, 1)

    # B_region_lake_geneva = Beta('B_region_lake_geneva', 0, None, None, 1)
    # B_region_espace_mittelland = Beta('B_region_espace_mittelland', 0, None, None, 1)
    # B_region_northern_switzerland = Beta('B_region_northern_switzerland', 0, None, None, 1)
    # B_region_zurich = Beta('B_region_zurich', 0, None, None, 1)
    b_region_eastern_switzerland = Beta('b_region_eastern_switzerland', 0, None, None, 0)
    # B_region_central_switzerland = Beta('B_region_central_switzerland', 0, None, None, 1)
    # B_region_tessin = Beta('B_region_tessin', 0, None, None, 1)
    # B_male_employees = Beta('B_male_employees', 0, None, None, 1)
    b_working_from_home = Beta('b_working_from_home', 0, None, None, 0)
    # B_home_office_NA = Beta('B_home_office_NA', 0, None, None, 1)
    # B_percentage_home_office = Beta('B_percentage_home_office', 0, None, None, 1)
    b_french = Beta('b_french', 0, None, None, 0)
    # b_italian_employees = Beta('b_italian_employees', 0, None, None, 1)
    b_business_sector_agriculture = Beta('b_business_sector_agriculture', 0, None, None, 0)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale = Beta('b_business_sector_wholesale', 0, None, None, 0)
    # b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 1)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    # b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 1)
    # b_business_sector_services_fC = Beta('b_business_sector_services_fC', 0, None, None, 1)
    # b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 1)
    # b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 1)
    b_business_sector_non_movers = Beta('b_business_sector_non_movers', 0, None, None, 0)
    b_home_work_distance = Beta('b_home_work_distance', 0, None, None, 0)
    # b_nb_car_in_hh = Beta('b_nb_car_in_hh', 0, None, None, 1)
    # b_nationality_ch = Beta('b_nationality_ch', 0, None, None, 1)
    # b_nationality_germany = Beta('b_nationality_germany', 0, None, None, 1)
    # b_nationality_france = Beta('b_nationality_france', 0, None, None, 1)
    # b_nationality_italy = Beta('b_nationality_italy', 0, None, None, 1)
    b_nationality_nw = Beta('b_nationality_nw', 0, None, None, 0)
    # b_nationality_e = Beta('b_nationality_e', 0, None, None, 1)
    # b_nationality_south_west_europe = Beta('b_nationality_south_west_europe', 0, None, None, 1)
    # b_nationality_southeast_europe = Beta('b_nationality_southeast_europe', 0, None, None, 1)
    b_nb_less_than_6_in_hh = Beta('b_nb_less_than_6_in_hh', 0, None, None, 0)

    # Parameters for the ordered logit.
    # tau1 <= 0
    tau1 = Beta('tau1', -1, None, 0, 0)
    # delta2 >= 0
    delta2 = Beta('delta2', 2, 0, None, 0)
    tau2 = tau1 + delta2
    delta3 = Beta('delta3', 2, 0, None, 0)
    tau3 = tau2 + delta3
    delta4 = Beta('delta4', 2, 0, None, 0)
    tau4 = tau3 + delta4

    # Definition of new variables
    car_avail_NA = (car_avail < 0)
    car_avail_syn_pop = ((car_avail == 1) | (car_avail == 2))
    with_general_abo = (GA_ticket == 1)
    with_verbund_abo = (Verbund_Abo == 1)
    urban = (city_typology == 1)
    rural = (city_typology == 3)
    intermediate = (city_typology == 2)
    single_household = (hh_type == 10)
    couple_without_children = (hh_type == 210)
    couple_with_children = (hh_type == 220)
    single_parent_with_children = (hh_type == 230)
    full_time_work = (ERWERB == 1)
    part_time_work = (ERWERB == 2)
    studying = (ERWERB == 3)
    inactive = (ERWERB == 4)
    active_without_known_work_percentage = (ERWERB == 9)
    public_transport_connection_quality_ARE_A = (public_transport_connection_quality_ARE == 1)
    public_transport_connection_quality_ARE_B = (public_transport_connection_quality_ARE == 2)
    public_transport_connection_quality_ARE_C = (public_transport_connection_quality_ARE == 3)
    public_transport_connection_quality_ARE_D = (public_transport_connection_quality_ARE == 4)
    public_transport_connection_quality_ARE_NA = (public_transport_connection_quality_ARE == 5)
    hh_income_na = (hh_income == -98)
    hh_income_less_than_2000 = (hh_income == 1)
    hh_income_2000_to_4000 = (hh_income == 2)
    hh_income_4001_to_6000 = (hh_income == 3)
    hh_income_6001_to_8000 = (hh_income == 4)
    hh_income_8001_to_10000 = (hh_income == 5)
    hh_income_10001_to_12000 = (hh_income == 6)
    hh_income_12001_to_14000 = (hh_income == 7)
    hh_income_14001_to_16000 = (hh_income == 8)
    hh_income_more_than_16000 = (hh_income == 9)

    no_post_school_educ = ((highest_educ == 1) | (highest_educ == 2) | (highest_educ == 3) | (highest_educ == 4))
    secondary_education = ((highest_educ == 5) | (highest_educ == 6) | (highest_educ == 7) | (highest_educ == 8) |
                           (highest_educ == 9) | (highest_educ == 10) | (highest_educ == 11) | (highest_educ == 12))
    tertiary_education_employees = (work_position == 2) * \
                                   ((highest_educ == 13) + (highest_educ == 14) + (highest_educ == 15) +
                                    (highest_educ == 16))
    university = (highest_educ == 17)
    region_lake_geneva = (region == 1)
    region_espace_mittelland = (region == 2)
    region_northern_switzerland = (region == 3)
    region_zurich = (region == 4)
    region_eastern_switzerland = (region == 5)
    region_central_switzerland = (region == 6)
    region_tessin = (region == 7)
    male = (sex == 1)
    working_from_home = ((home_office == 1) + (home_office == 2)) & (percentage_home_office > 0)
    home_office_NA = (home_office == -99)
    percentage_if_home_office = (((home_office == 1) + (home_office == 2)) * percentage_home_office)
    # not_employed = work_position == 0
    employees = work_position == 2
    executives = work_position == 1
    french = language == 2
    business_sector_agriculture = DefineVariable('business_sector_agriculture', 1 <= noga_08 <= 7, database)
    business_sector_retail = DefineVariable('business_sector_retail', 47 <= noga_08 <= 47, database)
    business_sector_gastronomy = DefineVariable('business_sector_gastronomy', 55 <= noga_08 <= 57, database)
    business_sector_finance = DefineVariable('business_sector_finance', 64 <= noga_08 <= 67, database)
    business_sector_production = DefineVariable('business_sector_production',
                                                (10 <= noga_08 <= 35) | (40 <= noga_08 <= 44), database)
    business_sector_wholesale = DefineVariable('business_sector_wholesale',
                                               (45 <= noga_08 <= 45) | (49 <= noga_08 <= 54), database)
    business_sector_services_fC = DefineVariable('business_sector_services_fC',
                                                 (60 <= noga_08 <= 63) | (69 <= noga_08 <= 83) | (noga_08 == 58),
                                                 database)
    business_sector_other_services = DefineVariable('business_sector_other_services',
                                                    (86 <= noga_08 <= 90) | (92 <= noga_08 <= 96) | (noga_08 == 59) |
                                                    (noga_08 == 68),
                                                    database)
    business_sector_others = DefineVariable('business_sector_others', 97 <= noga_08 <= 98, database)
    business_sector_non_movers = DefineVariable('business_sector_non_movers',
                                                (8 <= noga_08 <= 9) | (84 <= noga_08 <= 85) |
                                                (noga_08 == 91) | (noga_08 == 99),
                                                database)
    work_percentage = DefineVariable('work_percentage',
                                     (full_part_time_job == 1) * 100 +
                                     percentage_first_part_time_job * (percentage_first_part_time_job > 0),  # +
                                     # percentage_second_part_time_job * (percentage_second_part_time_job > 0),
                                     database)
    home_work_distance = (home_work_crow_fly_distance * (home_work_crow_fly_distance >= 0.0) / 100000.0)
    nationality_northwestern_europe = (nation == 8204) + (nation == 8223) + (nation == 8227) + (nation == 8206) + \
                                      (nation == 8211) + (nation == 8215) + (nation == 8216) + (nation == 8217) + \
                                      (nation == 8228) + (nation == 8234)

    #  Utility
    U = models.piecewiseFormula(age, [0, 20, 65, 75, 200]) + \
        b_executives * executives + \
        b_couple_with_children * couple_with_children + \
        b_studying * studying + \
        b_public_transport_connection_quality_are_na * public_transport_connection_quality_ARE_NA + \
        b_tertiary_education_employees * tertiary_education_employees + \
        b_region_eastern_switzerland * region_eastern_switzerland + \
        b_french * french + \
        b_business_sector_agriculture * business_sector_agriculture + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale * business_sector_wholesale + \
        b_business_sector_non_movers * business_sector_non_movers + \
        models.piecewiseFormula(work_percentage, [0, 10, 50, 101]) + \
        b_home_work_distance * home_work_distance + \
        b_nationality_nw * nationality_northwestern_europe + \
        b_nb_less_than_6_in_hh * nb_less_than_6_in_hh + \
        b_working_from_home * working_from_home

    # Associate each discrete indicator with an interval.
    #   0: -infinity -> tau1
    #   1: tau1 -> tau2
    #   2: tau2 -> tau3
    #   ...
    #   4+: tau4 -> +infinity
    ChoiceProba = {0: 1 - dist.logisticcdf(U - tau1),
                   1: dist.logisticcdf(U - tau1) - dist.logisticcdf(U - tau2),
                   2: dist.logisticcdf(U - tau2) - dist.logisticcdf(U - tau3),
                   3: dist.logisticcdf(U - tau3) - dist.logisticcdf(U - tau4),
                   4: dist.logisticcdf(U - tau4)}

    # Definition of the model. This is the contribution of each
    # observation to the log likelihood function.
    # logprob = log(Elem(ChoiceProba, WAA))

    # Define level of verbosity
    # logger = msg.bioMessage()
    # logger.setSilent()
    # logger.setWarning()
    # logger.setGeneral()
    # logger.setDetailed()

    # Get the betas from the estimation
    if betas is None:
        if os.path.isfile(path_to_estimation_folder / 'ordinalLogit~00.pickle'):
            print('WARNING: There are several model outputs!')
        results = res.bioResults(pickleFile=path_to_estimation_folder / 'ordinalLogit.pickle')
        betas = results.getBetaValues()

    # Change the working directory, so that biogeme writes in the correct folder
    standard_directory = os.getcwd()
    os.chdir(output_directory_for_simulation)

    # Create the Biogeme object
    # biogeme = bio.BIOGEME(database, logprob)
    # biogeme.modelName = 'ordinalLogit'
    #
    # # Estimate the parameters
    # results = biogeme.estimate()
    # pandasResults = results.getEstimatedParameters()
    # print(pandasResults)

    biogeme = bio.BIOGEME(database, ChoiceProba)
    biogeme.modelName = 'home_work_simul'

    results = biogeme.simulate(theBetaValues=betas)
    # print(results.describe())
    df = pd.concat([df, results], axis=1)

    # print('Younger than 15:')
    # print(df.loc[df.age < 15, 0].unique())
    # print(df.loc[df.age < 15, 1].unique())
    # print(df.loc[df.age < 15, 2].unique())
    # print(df.loc[df.age < 15, 3].unique())
    # print(df.loc[df.age < 15, 4].unique())

    # People younger than 15 don't work and don't go to work
    # df.loc[df.age < 15, 0] = 1.0
    # df.loc[df.age < 15, 1] = 0.0
    # df.loc[df.age < 15, 2] = 0.0
    # df.loc[df.age < 15, 3] = 0.0
    # df.loc[df.age < 15, 4] = 0.0

    # Go back to the normal working directory
    os.chdir(standard_directory)

    ''' Save the file '''
    df.to_csv(output_directory_for_simulation / output_file_name_for_simulation, sep=';', index=False)
