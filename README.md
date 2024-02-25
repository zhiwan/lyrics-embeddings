## STEP 1 Install the bot requirements
* ```python3 -m venv mp_env && source mp_env/bin/activate```
* for windows, instead of source, use ```mp_env\Scripts\activate```
* pip install -r requirements.txt

## STEP 2
* add your api's from genius and openai to your environment configuration file
* reload the configuration file: ```source ~/.bash_profile``` or ```source ~/.bashrc```

## SHORTCUT STEP 3 Get artist names + embeddings
### master_lyrics_embeddings.py
* example: ```python3 master_lyrics_embeddings.py 'The Beatles' 10```
* process: runs Step 3 and Step 4 together
* input: artist names and number of songs
* output: json file with from lyric genius + embeddings

## SHORTCUT STEP 4 Reduce dimensionality (No need to run the steps below)
### master_combine_plot.py
* example: ```python3 master_combine_plot.py 'The_Beatles' 'Taylor_Swift'```
* process: runs Step 5, Step 6, and Step 7 (both 2d and 3d) together
* input: the names of the artists and data you want to combine
* output: json files that combine the data, 2D + 3D dim reduction, and a 2d and 3d plot. 

## STEP 3 Importing data from Lyric Genius
### geniusExportLyrics.py
* example: ```python3 geniusExportLyrics.py 'The Beatles' 10```
* input: artist name and number of most popular songs
* output: json file with the lyrics of the most popular songs. file saved to 'genius_export' within a folder named after the artist with the spaces ``` ``` replaced by ```_```

## STEP 4 Getting embeddings
### embeddings.py
* example: ```python3 embeddings.py 'The_Beatles'```
* process: gets embeddings for the text field of each entry
* input: json. the name is the artist is with the spaces ``` ``` replaced by ```_```. It will automatically look in the 'genius_export' folder
* output: json file with embeddings_vector. filename will have ```_embeddings``` added

## STEP 5 Combine data
### combine_data.py
* example: ```python3 combine_data.py 'The_Beatles' 'Taylor_Swift' 'The_Cure' ... as many as you want```
* process: combines the json file embeddings into one json file. file is renamed with ```_vs_``` in between each artist data you inputted. it will place the new json file in a folder called 'plot'
* input: json. the name is the artist is with the spaces ``` ``` replaced by ```_```. It will automatically look for the artists in the 'genius_export' folder
* output: new combined json file of inputted artists

## STEP 6 Reduce dimensionality
### tSNE.py
* example: ```python3 tSNE.py 'The_Beatles_vs_Taylor_Swift'```
* process: reduce dimensionality of embeddings using tSNE
* input: json. file created from Step 5 with ```_vs_``` in between each artist. It will automatically look in the 'plot' folder and select the correct file
* output: new json with 2D + 3D dim reduction. filename will have ```_2d``` and ```_3d``` added respectively

## STEP 7 Plot data
### plotly2d.py or plotly3d
* plots in 2D + 3D with fields by using the 'tsne_embeddings' field
* example to plot in 2D: ```plotly2d.py 'The_Beatles_vs_Taylor_Swift'```
* example to plot in 3D: ```plotly3d.py 'The_Beatles_vs_Taylor_Swift'```
* input: json. file is renamed with ```_vs_``` in between each artist. It will automatically look in the 'plot' folder and select the correct file based on whether it is 2d or 3d
* output: 2d or 3d plot. an html file will be created and saved in the folder

## Helpful commands
* pip freeze > requirements.txt

# lyrics-embeddings
pipeline for lyrics -> json -> embeddings -> tSNE -> visualization
