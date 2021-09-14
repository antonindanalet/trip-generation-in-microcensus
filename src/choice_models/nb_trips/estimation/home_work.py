import pandas as pd
import biogeme.database as db
import biogeme.biogeme as bio
import biogeme.distributions as dist
import biogeme.messaging as msg
from biogeme.expressions import Beta, DefineVariable, log, Elem, Variable, bioMin
import biogeme.models as models
import os


def run_estimation_home_work(data_file_directory, data_file_name, output_directory):
    """ File home_work.py

    :author: Antonin Danalet, based on the example by Michel Bierlaire, EPFL, on biogeme.epfl.ch

    An ordinal logit model of the number of trips from home to work.
    Eleven ordered alternatives: 0, 1, 2, 3 and 4+ trips from home to work."""

    # Read the data
    df = pd.read_csv(data_file_directory / data_file_name, ';')
    database = db.Database(data_file_name, df)
    # The Pandas data structure is available as database.data. Use all the
    # Pandas functions to investigate the database
    # print(database.data.describe())

    # The following statement allows you to use the names of the variable as Python variable.
    globals().update(database.variables)

    ''' Removing children 14 years old and younger. We assume that they do 0 trips to work. '''
    database.data.drop(database.data[database.data.age <= 14].index, inplace=True)
    ''' Removing unemployed people: They don't go to work '''
    database.data.drop(database.data[database.data.work_position == 0].index, inplace=True)

    # Parameters to be estimated
    b_car_avail = Beta('b_car_avail', 0, None, None, 1)
    b_car_avail_na = Beta('b_car_avail_na', 0, None, None, 1)
    b_ga_employees = Beta('b_ga_employees', 0, None, None, 1)
    b_verbund = Beta('b_verbund', 0, None, None, 1)
    b_urban = Beta('b_urban', 0, None, None, 1)
    b_rural = Beta('b_rural', 0, None, None, 1)
    b_intermediate = Beta('b_intermediate', 0, None, None, 1)

    b_single_household = Beta('b_single_household', 0, None, None, 1)
    b_couple_without_children = Beta('b_couple_without_children', 0, None, None, 1)
    b_couple_without_children_30 = Beta('b_couple_without_children_30', 0, None, None, 1)
    b_couple_with_children = Beta('b_couple_with_children', 0, None, None, 0)
    b_single_parent_with_children = Beta('b_single_parent_with_children', 0, None, None, 1)
    b_employees = Beta('b_employees', 0, None, None, 1)
    b_executives = Beta('b_executives', 0, None, None, 1)

    b_studying = Beta('b_studying', 0, None, None, 0)
    b_inactive = Beta('b_inactive', 0, None, None, 1)
    b_active_without_known_work_percentage = Beta('b_active_without_known_work_percentage', 0, None, None, 1)

    b_public_transport_connection_quality_are_a = Beta('b_public_transport_connection_quality_are_a', 0, None, None, 1)
    b_public_transport_connection_quality_are_b = Beta('b_public_transport_connection_quality_are_b', 0, None, None, 1)
    b_public_transport_connection_quality_are_c = Beta('b_public_transport_connection_quality_are_c', 0, None, None, 1)
    b_public_transport_connection_quality_are_d = Beta('b_public_transport_connection_quality_are_d', 0, None, None, 1)
    b_public_transport_connection_quality_are_na_car = Beta('b_public_transport_connection_quality_are_na_car',
                                                            0, None, None, 0)
    b_public_transport_connection_quality_are_na_no_car = Beta('b_public_transport_connection_quality_are_na_no_car',
                                                               0, None, None, 0)
    b_hh_income_na = Beta('b_hh_income_na', 0, None, None, 1)
    b_hh_income_less_than_2000 = Beta('b_hh_income_less_than_2000', 0, None, None, 1)
    b_hh_income_2000_to_4000 = Beta('b_hh_income_2000_to_4000', 0, None, None, 1)
    b_hh_income_4001_to_6000 = Beta('b_hh_income_4001_to_6000', 0, None, None, 1)
    b_hh_income_6001_to_8000 = Beta('b_hh_income_6001_to_8000', 0, None, None, 1)
    b_hh_income_8001_to_10000 = Beta('b_hh_income_8001_to_10000', 0, None, None, 1)
    b_hh_income_10001_to_12000 = Beta('b_hh_income_10001_to_12000', 0, None, None, 1)
    b_hh_income_12001_to_14000 = Beta('b_hh_income_12001_to_14000', 0, None, None, 1)
    b_hh_income_14001_to_16000 = Beta('b_hh_income_14001_to_16000', 0, None, None, 1)
    b_hh_income_more_than_16000 = Beta('b_hh_income_more_than_16000', 0, None, None, 1)
    b_no_post_school_education = Beta('b_no_post_school_education', 0, None, None, 1)
    b_secondary_education = Beta('b_secondary_education', 0, None, None, 1)
    b_tertiary_education = Beta('b_tertiary_education', 0, None, None, 1)
    b_university = Beta('b_university', 0, None, None, 1)

    b_region_lake_geneva = Beta('b_region_lake_geneva', 0, None, None, 1)
    b_region_espace_mittelland = Beta('b_region_espace_mittelland', 0, None, None, 1)
    b_region_northern_switzerland = Beta('b_region_northern_switzerland', 0, None, None, 1)
    b_region_zurich = Beta('b_region_zurich', 0, None, None, 1)
    b_region_eastern_switzerland = Beta('b_region_eastern_switzerland', 0, None, None, 1)
    b_region_central_switzerland = Beta('b_region_central_switzerland', 0, None, None, 1)
    b_region_tessin = Beta('b_region_tessin', 0, None, None, 1)
    b_male_employees = Beta('b_male_employees', 0, None, None, 1)
    b_working_from_home = Beta('b_working_from_home', 0, None, None, 0)
    b_working_from_home_na = Beta('b_working_from_home_na', 0, None, None, 1)
    b_percentage_home_office = Beta('b_percentage_home_office', 0, None, None, 0)
    b_french = Beta('b_french', 0, None, None, 0)
    b_italian_employees = Beta('b_italian_employees', 0, None, None, 1)
    b_business_sector_agriculture_employee = Beta('b_business_sector_agriculture_employee', 0, None, None, 0)
    b_business_sector_agriculture_cadre = Beta('b_business_sector_agriculture_cadre', 0, None, None, 0)
    b_business_sector_production = Beta('b_business_sector_production', 0, None, None, 0)
    b_business_sector_wholesale_employee = Beta('b_business_sector_wholesale_employee', 0, None, None, 0)
    b_business_sector_wholesale_cadre = Beta('b_business_sector_wholesale_cadre', 0, None, None, 0)
    b_business_sector_retail = Beta('b_business_sector_retail', 0, None, None, 1)
    b_business_sector_gastronomy = Beta('b_business_sector_gastronomy', 0, None, None, 0)
    b_business_sector_finance = Beta('b_business_sector_finance', 0, None, None, 1)
    b_business_sector_services_fc = Beta('b_business_sector_services_fc', 0, None, None, 1)
    b_business_sector_other_services = Beta('b_business_sector_other_services', 0, None, None, 1)
    b_business_sector_others = Beta('b_business_sector_others', 0, None, None, 1)
    b_business_sector_non_movers_employee = Beta('b_business_sector_non_movers_employee', 0, None, None, 0)
    b_business_sector_non_movers_cadre = Beta('b_business_sector_non_movers_cadre', 0, None, None, 0)
    b_home_work_distance_car = Beta('b_home_work_distance_car', 0, None, None, 0)
    b_home_work_distance_no_car = Beta('b_home_work_distance_no_car', 0, None, None, 0)
    b_nb_car_in_hh = Beta('b_nb_car_in_hh', 0, None, None, 1)
    b_nationality_ch = Beta('b_nationality_ch', 0, None, None, 1)
    b_nationality_germany = Beta('b_nationality_germany', 0, None, None, 1)
    b_nationality_france = Beta('b_nationality_france', 0, None, None, 1)
    b_nationality_italy = Beta('b_nationality_italy', 0, None, None, 1)
    b_nationality_nw = Beta('b_nationality_nw', 0, None, None, 1)
    b_nationality_e = Beta('b_nationality_e', 0, None, None, 1)
    b_nationality_south_west_europe = Beta('b_nationality_south_west_europe', 0, None, None, 1)
    b_nationality_southeast_europe = Beta('b_nationality_southeast_europe', 0, None, None, 1)
    b_nb_less_than_15_in_hh = Beta('b_nb_less_than_15_in_hh', 0, None, None, 1)
    b_nb_less_than_6_in_hh = Beta('b_nb_less_than_6_in_hh', 0, None, None, 0)
    b_nb_between_6_and_15_in_hh = Beta('b_nb_between_6_and_15_in_hh', 0, None, None, 1)

    # Parameters for the ordered logit.
    # tau1 <= 0
    tau1 = Beta('tau1', -1, None, 3, 0)
    # delta2 >= 0
    delta2 = Beta('delta2', 2, 0, None, 0)
    tau2 = tau1 + delta2
    delta3 = Beta('delta3', 2, 0, None, 0)
    tau3 = tau2 + delta3
    delta4 = Beta('delta4', 2, 0, None, 0)
    tau4 = tau3 + delta4

    # Definition of new variables
    car_avail_NA = DefineVariable('car_avail_NA', car_avail < 0, database)
    car_avail_syn_pop = DefineVariable('car_avail_syn_pop', (car_avail == 1) | (car_avail == 2), database)
    with_general_abo_employees = DefineVariable('with_general_abo_employees',
                                                (GA_ticket == 1) & (work_position == 2), database)
    with_verbund_abo = DefineVariable('with_verbund_abo', Verbund_Abo == 1, database)
    urban = DefineVariable('urban', city_typology == 1, database)
    rural = DefineVariable('rural', city_typology == 3, database)
    intermediate = DefineVariable('intermediate', city_typology == 2, database)
    single_household = DefineVariable('single_household', (hh_type == 10), database)
    couple_without_children = DefineVariable('couple_without_children_employees', (hh_type == 210), database)
    couple_without_children_30 = DefineVariable('couple_without_children_30', (hh_type == 210) & (age <= 30), database)
    couple_with_children = DefineVariable('couple_with_children', hh_type == 220, database)
    single_parent_with_children = DefineVariable('single_parent_with_children_employees', hh_type == 230, database)
    studying = DefineVariable('studying', ERWERB == 3, database)
    inactive = DefineVariable('inactive', ERWERB == 4, database)
    active_without_known_work_percentage = DefineVariable('active_without_known_work_percentage', ERWERB == 9, database)
    public_transport_connection_quality_ARE_A = DefineVariable('public_transport_connection_quality_ARE_A',
                                                               public_transport_connection_quality_ARE == 1, database)
    public_transport_connection_quality_ARE_B = DefineVariable('public_transport_connection_quality_ARE_B',
                                                               public_transport_connection_quality_ARE == 2, database)
    public_transport_connection_quality_ARE_C = DefineVariable('public_transport_connection_quality_ARE_C',
                                                               public_transport_connection_quality_ARE == 3, database)
    public_transport_connection_quality_ARE_D = DefineVariable('public_transport_connection_quality_ARE_D',
                                                               public_transport_connection_quality_ARE == 4, database)
    public_transport_connection_quality_ARE_NA_car = DefineVariable('public_transport_connection_quality_ARE_NA_car',
                                                                    (public_transport_connection_quality_ARE == 5) *
                                                                    car_avail_syn_pop, database)
    public_transport_connection_quality_ARE_NA_no_car = DefineVariable('public_transport_connection_quality_ARE_NA_no_car',
                                                                       (public_transport_connection_quality_ARE == 5) *
                                                                       (1-car_avail_syn_pop), database)
    hh_income_na = DefineVariable('hh_income_na', hh_income == -98, database)
    hh_income_less_than_2000 = DefineVariable('hh_income_less_than_4000', hh_income == 1, database)
    hh_income_2000_to_4000 = DefineVariable('hh_income_2000_to_4000', hh_income == 2, database)
    hh_income_4001_to_6000 = DefineVariable('hh_income_4001_to_6000', hh_income == 3, database)
    hh_income_6001_to_8000 = DefineVariable('hh_income_6001_to_8000', hh_income == 4, database)
    hh_income_8001_to_10000 = DefineVariable('hh_income_8001_to_10000', hh_income == 5, database)
    hh_income_10001_to_12000 = DefineVariable('hh_income_10001_to_12000', hh_income == 6, database)
    hh_income_12001_to_14000 = DefineVariable('hh_income_12001_to_14000', hh_income == 7, database)
    hh_income_14001_to_16000 = DefineVariable('hh_income_14001_to_16000', hh_income == 8, database)
    hh_income_more_than_16000 = DefineVariable('hh_income_more_than_16000', hh_income == 9, database)

    no_post_school_educ = DefineVariable('no_post_school_educ',
                                         (highest_educ == 1) | (highest_educ == 2) |
                                         (highest_educ == 3) | (highest_educ == 4), database)
    secondary_education = DefineVariable('secondary_education',
                                         (highest_educ == 5) | (highest_educ == 6) | (highest_educ == 7) |
                                         (highest_educ == 8) | (highest_educ == 9) | (highest_educ == 10) |
                                         (highest_educ == 11) | (highest_educ == 12), database)
    tertiary_education = DefineVariable('tertiary_education', (highest_educ == 13) | (highest_educ == 14) |
                                                   (highest_educ == 15) | (highest_educ == 16), database)
    university = DefineVariable('university', highest_educ == 17, database)
    region_lake_geneva = DefineVariable('region_lake_geneva', region == 1, database)
    region_espace_mittelland = DefineVariable('region_espace_mittelland', region == 2, database)
    region_northern_switzerland = DefineVariable('region_northern_switzerland', region == 3, database)
    region_zurich = DefineVariable('region_zurich', region == 4, database)
    region_eastern_switzerland = DefineVariable('region_eastern_switzerland', region == 5, database)
    region_central_switzerland = DefineVariable('region_central_switzerland', region == 6, database)
    region_tessin = DefineVariable('region_tessin', region == 7, database)
    male_employees = DefineVariable('male', (sex == 1) & (work_position == 2), database)
    working_from_home = DefineVariable('working_from_home', ((home_office == 1) + (home_office == 2)) &
                                       (percentage_home_office > 0), database)
    working_from_home_na = DefineVariable('working_from_home_na', home_office == -99, database)
    percentage_if_home_office = DefineVariable('percentage_if_home_office', ((home_office == 1) +
                                                                             (home_office == 2)) *
                                               percentage_home_office, database)
    # not_employed = DefineVariable('not_employed', work_position == 0, database)
    employees = DefineVariable('employees', work_position == 2, database)
    executives = DefineVariable('executives', work_position == 1, database)
    french = DefineVariable('french', language == 2, database)
    italian_employees = DefineVariable('italian', (language == 3) & (work_position == 2), database)

    business_sector_agriculture_employee = DefineVariable('business_sector_agriculture_employee',
                                                          (1 <= noga_08 <= 7) * (work_position == 2), database)
    business_sector_agriculture_cadre = DefineVariable('business_sector_agriculture_cadre',
                                                       (1 <= noga_08 <= 7) * (work_position == 1), database)
    business_sector_retail = DefineVariable('business_sector_retail', 47 <= noga_08 <= 47, database)
    business_sector_gastronomy = DefineVariable('business_sector_gastronomy', 55 <= noga_08 <= 57, database)
    business_sector_finance = DefineVariable('business_sector_finance', 64 <= noga_08 <= 67, database)
    business_sector_production = DefineVariable('business_sector_production',
                                                         (10 <= noga_08 <= 35) | (40 <= noga_08 <= 44), database)
    business_sector_wholesale_employee = DefineVariable('business_sector_wholesale_employee',
                                               ((45 <= noga_08 <= 46) | (49 <= noga_08 <= 54)) *
                                                         (work_position == 2), database)
    business_sector_wholesale_cadre = DefineVariable('business_sector_wholesale_cadre',
                                                        ((45 <= noga_08 <= 46) | (49 <= noga_08 <= 54)) *
                                                        (work_position == 1), database)
    business_sector_services_fC = DefineVariable('business_sector_services_fC',
                                                 (60 <= noga_08 <= 63) | (69 <= noga_08 <= 83) | (noga_08 == 58),
                                                 database)
    business_sector_other_services = DefineVariable('business_sector_other_services', (86 <= noga_08 <= 90) |
                                                    (92 <= noga_08 <= 96) | (noga_08 == 59) | (noga_08 == 68), database)
    business_sector_others = DefineVariable('business_sector_others', 97 <= noga_08 <= 98, database)
    business_sector_non_movers_employee = DefineVariable('business_sector_non_movers_employee',
                                                (work_position == 2) *
                                                ((8 <= noga_08 <= 9) | (84 <= noga_08 <= 85) | (noga_08 == 91) |
                                                 (noga_08 == 99)), database)
    business_sector_non_movers_cadre = DefineVariable('business_sector_non_movers_cadre',
                                                         (work_position == 1) *
                                                         ((8 <= noga_08 <= 9) | (84 <= noga_08 <= 85) | (
                                                                     noga_08 == 91) |
                                                          (noga_08 == 99)), database)

    work_percentage = DefineVariable('work_percentage',
                                     bioMin((full_part_time_job == 1) * 100 +
                                            percentage_first_part_time_job * (percentage_first_part_time_job > 0),  # +
                                            # percentage_second_part_time_job * (percentage_second_part_time_job > 0),
                                            100),
                                     database)
    home_work_distance_car = DefineVariable('home_work_distance_car', car_avail_syn_pop * home_work_crow_fly_distance *
                                            (home_work_crow_fly_distance >= 0.0) / 100000.0,
                                            database)
    home_work_distance_no_car = DefineVariable('home_work_distance_no_car', (1-car_avail_syn_pop) *
                                               home_work_crow_fly_distance *
                                               (home_work_crow_fly_distance >= 0.0) / 100000.0,database)
    nb_car_in_hh_clean = DefineVariable('nb_car_in_hh_clean', nb_car_in_hh * (nb_car_in_hh > 0), database)

    nationality_switzerland = DefineVariable('nationality_switzerland', nation == 8100, database)
    nationality_germany_austria_lichtenstein = DefineVariable('nationality_germany_austria_lichtenstein',
                                                              (nation == 8207) | (nation == 8229) | (nation == 8222),
                                                              database)
    nationality_italy_vatican = DefineVariable('nationality_italy_vatican', (nation == 8218) | (nation == 8241),
                                               database)
    nationality_france_monaco_san_marino = DefineVariable('nationality_france_monaco_san_marino',
                                                          (nation == 8212) | (nation == 8226) | (nation == 8233),
                                                          database)
    nationality_northwestern_europe = DefineVariable('nationality_northwestern_europe',
                                                     (nation == 8204) |  # Belgium
                                                     (nation == 8223) |  # Luxembourg
                                                     (nation == 8227) |  # Netherlands
                                                     (nation == 8206) |  # Denmark
                                                     (nation == 8211) |  # Finland
                                                     (nation == 8215) |  # United Kingdom
                                                     (nation == 8216) |  # Ireland
                                                     (nation == 8217) |  # Iceland
                                                     (nation == 8228) |  # Norway
                                                     (nation == 8234),  # Sweden
                                                     database)
    nationality_south_west_europe = DefineVariable('nationality_south_west_europe',
                                                   (nation == 8231) |  # Portugal
                                                   (nation == 8236) |  # Spain
                                                   (nation == 8202),  # Andorra
                                                   database)
    nationality_southeast_europe = DefineVariable('nationality_southeast_europe',
                                                  (nation == 8224) |  # Malta
                                                  (nation == 8201) |  # Albania
                                                  (nation == 8214) |  # Greece
                                                  (nation == 8256) |  # Kosovo
                                                  (nation == 8250) |  # Croatia
                                                  (nation == 8251) |  # Slovenia
                                                  (nation == 8252) |  # Bosnia and Herzegovina
                                                  (nation == 8255) |  # Macedonia
                                                  (nation == 8205) |  # Bulgaria
                                                  (nation == 8239) |  # Turkey
                                                  (nation == 8242) |  # Cyprus
                                                  (nation == 8248) |  # Serbia
                                                  (nation == 8254),  # Montenegro
                                                  database)
    nationality_eastern_europe = DefineVariable('nationality_eastern_europe',
                                                (nation == 8230) |  # Poland
                                                (nation == 8232) |  # Rumania
                                                (nation == 8240) |  # Hungary
                                                (nation == 8243) |  # Slovakia
                                                (nation == 8244) |  # Czech Republic
                                                (nation == 8263) |  # Moldavia
                                                (nation == 8265) |  # Ukraine
                                                (nation == 8266) |  # Belarus
                                                (nation == 8260) |  # Estonia
                                                (nation == 8261) |  # Latvia
                                                (nation == 8262),  # Lithuania
                                                database)
    nb_between_6_and_15_in_hh = DefineVariable('nb_between_6_and_15_in_hh',
                                               nb_less_than_15_in_hh - nb_less_than_6_in_hh, database)

    #  Utility
    U = models.piecewiseFormula(age, [0, 20, 65, 75, 200]) + \
        b_car_avail * car_avail_syn_pop + \
        b_car_avail_na * car_avail_NA + \
        b_ga_employees * with_general_abo_employees + \
        b_verbund * with_verbund_abo + \
        b_urban * urban + \
        b_rural * rural + \
        b_intermediate * intermediate + \
        b_single_household * single_household + \
        b_couple_without_children * couple_without_children + \
        b_couple_with_children * couple_with_children + \
        b_single_parent_with_children * single_parent_with_children + \
        b_employees * employees + \
        b_executives * executives + \
        b_studying * studying + \
        b_inactive * inactive + \
        b_active_without_known_work_percentage * active_without_known_work_percentage + \
        b_public_transport_connection_quality_are_a * public_transport_connection_quality_ARE_A + \
        b_public_transport_connection_quality_are_b * public_transport_connection_quality_ARE_B + \
        b_public_transport_connection_quality_are_c * public_transport_connection_quality_ARE_C + \
        b_public_transport_connection_quality_are_d * public_transport_connection_quality_ARE_D + \
        b_public_transport_connection_quality_are_na_car * public_transport_connection_quality_ARE_NA_car + \
        b_public_transport_connection_quality_are_na_no_car * public_transport_connection_quality_ARE_NA_no_car + \
        b_hh_income_less_than_2000 * hh_income_less_than_2000 + \
        b_hh_income_2000_to_4000 * hh_income_2000_to_4000 + \
        b_hh_income_4001_to_6000 * hh_income_4001_to_6000 + \
        b_hh_income_6001_to_8000 * hh_income_6001_to_8000 + \
        b_hh_income_8001_to_10000 * hh_income_8001_to_10000 + \
        b_hh_income_10001_to_12000 * hh_income_10001_to_12000 + \
        b_hh_income_12001_to_14000 * hh_income_12001_to_14000 + \
        b_hh_income_14001_to_16000 * hh_income_14001_to_16000 + \
        b_hh_income_more_than_16000 * hh_income_more_than_16000 + \
        b_no_post_school_education * no_post_school_educ + \
        b_secondary_education * secondary_education + \
        b_tertiary_education * tertiary_education + \
        b_university * university + \
        b_region_lake_geneva * region_lake_geneva + \
        b_region_espace_mittelland * region_espace_mittelland + \
        b_region_northern_switzerland * region_northern_switzerland + \
        b_region_zurich * region_zurich + \
        b_region_eastern_switzerland * region_eastern_switzerland + \
        b_region_central_switzerland * region_central_switzerland + \
        b_region_tessin * region_tessin + \
        b_male_employees * male_employees + \
        b_working_from_home * working_from_home + \
        b_working_from_home_na * working_from_home_na + \
        b_percentage_home_office * percentage_if_home_office + \
        b_french * french + \
        b_italian_employees * italian_employees + \
        b_business_sector_agriculture_employee * business_sector_agriculture_employee + \
        b_business_sector_agriculture_cadre * business_sector_agriculture_cadre + \
        b_business_sector_retail * business_sector_retail + \
        b_business_sector_gastronomy * business_sector_gastronomy + \
        b_business_sector_finance * business_sector_finance + \
        b_business_sector_production * business_sector_production + \
        b_business_sector_wholesale_employee * business_sector_wholesale_employee + \
        b_business_sector_wholesale_cadre * business_sector_wholesale_cadre + \
        b_business_sector_services_fc * business_sector_services_fC + \
        b_business_sector_other_services * business_sector_other_services + \
        b_business_sector_others * business_sector_others + \
        b_business_sector_non_movers_employee * business_sector_non_movers_employee + \
        b_business_sector_non_movers_cadre * business_sector_non_movers_cadre + \
        models.piecewiseFormula(work_percentage, [0, 10, 50, 101]) + \
        b_home_work_distance_car * home_work_distance_car + \
        b_home_work_distance_no_car * home_work_distance_no_car + \
        b_nb_car_in_hh * nb_car_in_hh_clean + \
        b_nationality_ch * nationality_switzerland + \
        b_nationality_germany * nationality_germany_austria_lichtenstein + \
        b_nationality_italy * nationality_italy_vatican + \
        b_nationality_france * nationality_france_monaco_san_marino + \
        b_nationality_nw * nationality_northwestern_europe + \
        b_nationality_south_west_europe * nationality_south_west_europe + \
        b_nationality_southeast_europe * nationality_southeast_europe + \
        b_nationality_e * nationality_eastern_europe + \
        b_nb_less_than_15_in_hh * nb_less_than_15_in_hh + \
        b_couple_without_children_30 * couple_without_children_30 + \
        b_nb_less_than_6_in_hh * nb_less_than_6_in_hh + \
        b_nb_between_6_and_15_in_hh * nb_between_6_and_15_in_hh

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
    logprob = log(Elem(ChoiceProba, WA))

    # Define level of verbosity
    logger = msg.bioMessage()
    # logger.setSilent()
    #logger.setWarning()
    #logger.setGeneral()
    #logger.setDetailed()

    # Change the working directory, so that biogeme writes in the correct folder, i.e., where this file is
    standard_directory = os.getcwd()
    os.chdir(output_directory)

    # Create the Biogeme object
    biogeme = bio.BIOGEME(database, logprob)
    biogeme.modelName = 'ordinalLogit'

    # Estimate the parameters
    results = biogeme.estimate()

    # Get the results in LaTeX
    results.writeLaTeX()

    # Get the results as Pandas DataFrame
    pandasResults = results.getEstimatedParameters()
    print(pandasResults)

    # Go back to the normal working directory
    os.chdir(standard_directory)
