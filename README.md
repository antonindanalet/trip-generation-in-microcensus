# Trip generation in Switzerland, 2015
This codes estimates an ordered logit from the data of the Mobility and Transport Microcensus 2015 explaining the number of trips from home to work. The outputs are available in an HTML file. The results are described in a conference paper, "<a href="http://strc.ch/2021/Danalet_EtAl.pdf">Trip generation in Switzerland, 2015-2030</a>", published for the <a href="http://strc.ch/2021.php">21th</a> <a href="http://strc.ch/">Swiss Transport Research Conference (STRC)</a>.

## Getting Started

If you want to estimate and validate the model, you need this code and the data of the Mobility and Transport Microcensus 2015.

### Prerequisites to run the code

To run the code itself, you need python 3, pandas, Geopandas and PandasBiogeme.

### Data prerequisites

You also need the raw data of the Transport and Mobility Microcensus 2015, not included on GitHub. These data are individual data and therefore not open. You can however get them by filling in this <a href="https://www.are.admin.ch/are/de/home/mobilitaet/grundlagen-und-daten/mzmv/datenzugang.html">form in German</a>, <a href="https://www.are.admin.ch/are/fr/home/mobilite/bases-et-donnees/mrmt/accesauxdonnees.html">French</a> or <a href="https://www.are.admin.ch/are/it/home/mobilita/basi-e-dati/mcmt/accessoaidati.html">Italian</a>. The cost of the data is available in the document "<a href="https://www.are.admin.ch/are/de/home/medien-und-publikationen/publikationen/grundlagen/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Mikrozensus Mobilität und Verkehr 2015: Mögliche Zusatzauswertungen</a>"/"<a href="https://www.are.admin.ch/are/fr/home/media-et-publications/publications/bases/mikrozensus-mobilitat-und-verkehr-2015-mogliche-zusatzauswertung.html">Microrecensement mobilité et transports 2015: Analyses supplémentaires possibles</a>".

### Run the code

Please copy the files haushalte.csv and zielpersonen.csv of the Mobility and Transport Microcensus 2015 that you receive from the Federal Statistical Office in the folders <a href="https://github.com/antonindanalet/trip-generation-in-microcensus/tree/main/data/input/mtmc/2015">data/input/mtmc/2015/</a>. Then run <a href="https://github.com/antonindanalet/trip-generation-in-microcensus/blob/main/src/run_trip_generation.py">run_trip_generation.py</a>.

DO NOT commit or share in any way the CSV files haushalte.csv and zielpersonen.csv! These are personal data.

