# Tutorial: How to create a Brick model for a building dataset using VizBrick

# Introduction

**VizBrick** (https://github.com/liza183/vizbrick) is a web-based tool with a graphical user interface that helps users to create Brick models (https://brickschema.org/) for their building datasets more easily in an interactive way, without having to know the detailed syntax of RDF TTL(Terse RDF Triple Language) that is used to describe Brick models. In this tutorial, we explain how to create a Brick model using **VizBrick** with the *Ecobee* building dataset (link).

# Installation & how to run

VizBrick requires Python version 3.X, and using Anaconda is recommended. Please download Anaconda from [https://www.anaconda.com/download/](https://www.anaconda.com/download/) and install it first.

Once you installed Anaconda (with Python 3.X), clone the repository by doing

    git clone https://github.com/liza183/vizbrick

Go to the VizBrick directory and create a new Anaconda/Python environment for VizBrick by doing:

    conda env create -f environment.yml --name vizbrick

Please refer to the environent.yml for dependencies.

To activate an environment:

- On Windows, in your Anaconda Prompt, run
    activate vizbrick
- On macOS and Linux, in your Terminal Window, run
    conda activate vizbrick

You will see the active environment in parentheses at the beginning of your command prompt:

    (vizbrick) $

You need to run two Python scripts to start up the VizBrick. Please go to the data_API folder and run the following command:

    (vizbrick) slzmacbookpro:data_API slz$ python api_server.py 
    * Loading Done

The VizBrick API server is now up and running. Then, we need to start up the web server. Go to the web_interface folder and run the following command: 

    (base) slzmacbookpro:web_interface slz$ python ui_server_test.py 
    
    # Web Server started .. now listening port 8088 ..

Then, open any web browser and go to ``http://localhost:8088/` . If you see the following interface, now, you’re ready to use the VizBrick.

![Figure 1. VizBrick web-interface](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652796548853_Screen+Shot+2022-05-17+at+10.08.37+AM.png)

# Example: Creating a Brick model for a Ecobee dataset using VizBrick

To demonstrate how a Brick model can be created using VizBrick for a real-world building dataset, we explain the steps to create a Brick model for the Ecobee dataset. Ecobee dataset is a building dataset and it has 26 data points.

## 1. Preparation of a metadata in a CSV file

The first step to creating a Brick model is to prepare a metadata CSV (comma-separated values) file that contains the list of data labels (data points) and their description.

The structure of the metadata file required by VizBrick is very simple. The first column is for the row number index. The second column (Data Label) contains the name of the data label (data point) and the last column contains the description of the corresponding data label in natural language or keywords. We created Table 1 for the Ecobee dataset using spreadsheet software and saved it as a CSV file named ecobee.csv. 

| **Index** | **Data Label**              | **Description**                                 |
| --------- | --------------------------- | ----------------------------------------------- |
| 0         | T_ctrl                      | Indoor averaged measured temperature            |
| 1         | T_stp_cool                  | Indoor cooling setpoint                         |
| 2         | T_stp_heat                  | Indoor heating setpoint                         |
| 3         | Humidity                    | Indoor humidity                                 |
| …         | …                           | Run time for other heat source 1                |
| 22        | Remote_Sensor_5_Temperature | Measured temperature at remote sensor 5         |
| 23        | Remote_Sensor_5_Motion      | Detected motion at remote sensor 5              |
| 24        | T_out                       | Outdoor temperature for nearest weather station |
| 25        | RH_out                      | Outdoor humidity for nearest weather station    |

The CSV file will look like the following:

    Index,Data Label,Description
    0,T_ctrl,Indoor averaged measured temperature
    1,T_stp_cool,Indoor cooling setpoint
    2,T_stp_heat,Indoor heating setpoint
    3,Humidity,Indoor humidity
    4,auxHeat1,Run time for other heat source 1
    5,auxHeat2,Run time for other heat source 2
    6,auxHeat3,Run time for other heat source 3
    ...

Note that the list of data labels and their descriptions are often provided by the personnel or organizations that collected the data. Such information can be used for these steps. There is no specific syntax or requirement for the data label and description values, however, VizBrick will later use the patterns of terms and keywords that show up in both the data label and description for Brick class matching and search. Thus, using more descriptive and semantically clear terms with consistent rules is strongly recommended. For instance, the data label name ‘Humidity’ is better than ‘h1’. Naming the data labels starting with ‘T_’ for temperature sensors is recommended rather than randomly naming them.

When the CSV file is ready. Open a web browser window and load the CSV file by clicking the ‘Load (Start from Scratch)’ button to load the file with VizBrick.

![Figure 2. Loading a metadata csv file with VizBrick](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652799748963_Screen+Shot+2022-05-17+at+11.00.35+AM.png)


When the metadata is successfully loaded by VizBrick. You will see the metadata table loaded. 

![Figure 3. Loaded metadata table in VizBrick](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652799910992_Screen+Shot+2022-05-17+at+11.04.29+AM.png)

## 2. Creating Brick entities for data labels

Next, we will create Brick entities for data points by finding the best matching class for each data label from the Brick ontology. Searching and browsing the Brick ontology to find the best matching class for each data point can be repetitive and time-consuming. To speed up the process, VizBrick provides a suggestion capability. When you click the ‘Suggest All’ button on top of the metadata table, VizBrick will iterate each row in the metadata table and automatically find the most appropriate Brick class for each data label based on keywords included in the data label and the description. The suggestion can take a few minutes or more depending on the number of data labels in the metadata table. Figure 4 shows the result of the suggestion.

![Figure 4.  Brick classes are automatically suggested for each data label.](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652801256959_Screen+Shot+2022-05-17+at+11.27.18+AM.png)


Although VizBrick can suggest Brick classes automatically, the accuracy of this automatic matching largely depends on the quality of the data label and description. Thus, we need to manually confirm if these suggestions were correct. For instance, VizBrick thinks that the best matching Brick class for the data label ‘T_stp_cool’ and ‘T_stp_heat’ are ‘Cooling Temperature Setpoint’ and ‘Heating Temperature Setpoint’ respectively, which is correct. Matchings for ‘Humidity’ and ‘auxHeat1’ are correct. However, the most appropriate Brick class for the data label ‘T_ctrl’ should be ‘Average Zone Air Temperature Sensor’ not the ‘Temperature Setpoint’. In this case. we need to correct the matching.

Select the row with ID 0 (the row for T_ctrl) and click ‘Inspect’, then you can see the details of this data label and make modifications as you want in the Brick Object Creator.

![Figure 5. Brick Object creator](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652801877137_Screen+Shot+2022-05-17+at+11.36.25+AM.png)


Now we see that the Brick class matched for this label is ‘Temperature Setpoint’. What we will do is to get another suggestion give more hints to VizBrick and select manually from the result. On the left side of the Brick Object Creator panel, you will see Search & Suggest panel. You can provide more keywords as hints to VizBrick to generate better suggestion results or you can perform a keyword search too. The difference between suggestion and search is that suggestion uses the description of the data label and keywords provided by the user but search only uses the keywords provided by the user. In this example, we give one keyword ‘average’ as an additional keyword and click the ‘Suggest on Selected & Keywords’ button to get the suggestion list. Rank 1 from the list was ‘Average Zone Air Temperature Sensor’ which we think is correct, so we select and click ‘Update Class’.

![Figure 6. Search & Suggest panel](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652802129446_Screen+Shot+2022-05-17+at+11.41.55+AM.png)


Once we confirm that all the matchings are good for all data labels. Now it is to create Brick entities. 

First, we start with creating Brick entities that are not data points but the ones have relationships with the data points. Locations, equipments, and other things that are helpful to semantically describe the dataset can be created as Brick entities. Figure 7 shows an example of creating an entity for a hvac zone. First, we click the ‘Clear’ button to initialize the Brick object creator tool. Then, update the name with ‘hvac_zone’ by typing in and clicking the ‘Update Object Name’ button. After searching with keywords ‘hvac zone’ in the left panel and we updated the Brick class of the entity to be the ‘HVAC Zone’. Then, clicking ‘Add to Canvas’ button will create a Brick entity with the information shown in the Brick object creator panel and add it in the Canvas, where the current in-progress Brick model is visualized. Each Brick entity is represented as a node (vertex) in the Canvas panel.


![Figure 7. Creating a Brick entity.](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652802740778_Screen+Shot+2022-05-17+at+11.52.07+AM.png)


Just like we created the ‘hvac_zone’ entity, we created other entities such as outside, rooms, and hvac_system. The terms between the parentheses are the Brick class names. How many Brick entities and what should be created depend on the dataset and user’s knowledge about the dataset, but it is recommended to be descriptive, but not unnecessarily complex.

![Figure 8. Created Brick entities](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652809920191_Screen+Shot+2022-05-17+at+11.51.40+AM.png)


Then, next, we create Brick entities for the data labels. Since we already assigned Brick classes to each data label, we can simply click the ‘Add All to Canvas’ button in the metadata table panel. Then, entities will be created for data labels and added to the canvas panel.

## 3. Creating Brick relationships across entities

In the previous step, we created Brick entities and they are added to the canvas panel. Each entity is represented as a node in the network, and the next thing we need to do is to describe the relationships across them. One way of creating relationships is using the Rule-based Edge Creator panel. For instance, we know that the room_1, room_2, …, and room_5 are parts of the hvac_zone, so we need to create edges between all the pairs with the Brick relationship type ‘isPartOf’. So we type in ‘room’ to be the value of the form ‘From Node (must include)’ and ‘hvac_zone’ in the form ‘To Node (must include)’. Then, we click ‘Create Edges’. This means that we want to create edges between any entities that contain the keyword ‘room’ in their data labels or descriptions to any entities that contain ‘hvac_zone’ in their data labels or descriptions.

![Figure 9. Creating relationships using ruled-based edge creator](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652810604577_Screen+Shot+2022-05-17+at+2.02.38+PM.png)


As a result, 5 relationships will be created as shown in Figure 10.

![Figure 10. Created Brick relationships between entities](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652810995165_Screen+Shot+2022-05-17+at+2.07.57+PM.png)


If a single edge between specific two Brick entities needs to be created, a user can use a Brick Edge Creator panel. By selecting an entity in the canvas and clicking ‘From’ or ‘To’ button in the edge creator panel, we set up what entities to be connected. Next is to select a relationship type and click ‘Create’ button. Figure 11 shows an example.

![Figure 11. Creating an edge between Thermostat_Temperature entity and hvac_zone entity with a relationship type ‘isPointOf’](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652811329596_Screen+Shot+2022-05-17+at+2.11.20+PM.png)


Relationships across entities are represented as directional edges on the canvas. Depending on the complexity of the model that is being created, intermediate results may need to be created. Progress can be saved by clicking the ‘Save Checkpoint’ button and the file name can be given by the user. Loading the progress can be done similarly, but it needs to be carefully done as loading from a file can override your current progress.

![Figure 12. Intermediate progress can be saved as a JSON file.](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652811486262_Screen+Shot+2022-05-17+at+2.17.42+PM.png)


Creating relationships requires many iterative processes of choosing things to connect with and assigning proper relationship types. Figure 13 shows the final result visualized in the canvas after a few iterations of creating relationships. The result can be saved as a TTL file by simply clicking the ‘Save Brick button'

![Figure 13. Ecobee Brick model visualized by VizBrick](https://paper-attachments.dropbox.com/s_5AEBC4E7DCA06DB394BC0A6C46EA3A506569679FC6989D084D41AA65AF030204_1652811874991_Screen+Shot+2022-05-17+at+2.24.13+PM.png)


The following file shows the first few lines of the created ttl file. 


    @prefix bldg: <https://url_of_this_data#> .
    @prefix brick: <https://brickschema.org/schema/1.1/Brick#> .
    @prefix btag: <https://brickschema.org/schema/1.0.2/BrickTag#> .
    @prefix gtc: <https://brickschema.org/schema/1.0.2/building_example#> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix tag: <https://brickschema.org/schema/1.1/BrickTag#> .
    @prefix xml: <http://www.w3.org/XML/1998/namespace> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    
    bldg:auxHeat1 a brick:Run_Time_Sensor .
    bldg:auxHeat2 a brick:Run_Time_Sensor .
    bldg:auxHeat3 a brick:Run_Time_Sensor .
    bldg:compCool1 a brick:Run_Time_Sensor .
    bldg:compCool2 a brick:Run_Time_Sensor .
    bldg:compHeat1 a brick:Run_Time_Sensor .
    bldg:compHeat2 a brick:Run_Time_Sensor .
    bldg:fan a brick:Run_Time_Sensor .
    bldg:Humidity a brick:Humidity_Sensor .
    bldg:hvac_system a brick:HVAC_System .
    bldg:hvac_zone a brick:HVAC_Zone .
    bldg:outside a brick:Outside .
    
    ...


## 4. Finalization of the created Brick model

The first line needs to be manually updated to assign a proper url for this Brick model. It is also very important to validate the create ttl file using a RDF validator tool such as RDF Validator (https://www.w3.org/2015/03/ShExValidata/).  Also, visualizing the created Brick model file with another visualization tool such as Brick TTL Viewer (https://viewer.brickschema.org/) is very helpful to check if the final outcome is created as expected correctly.

# Conclusions

VizBrick enables creating Brick models for building datasets without having to program or understand the syntax of RDF language or details of Brick ontology. The tool provides several assist capabilities such as Brick class suggestion, rule-based mapping, interactive manipulation of the network, and visualization. In this document, we demonstrated how to install, run, and use VizBrick to create a Brick model for building a dataset. We chose Ecobee dataset as our example dataset and explained every step of the process. 


