# oGaze — An Advanced Biosignal Interface for Gaze-Centric Economic Experiment

oGaze is an innovative tool presented in this repository that facilitates the integration of live biofeedback into economic experiments, specifically focusing on decision-based behavior. Developed as an advanced biosignal interface, oGaze enhances oTree, a widely used open-source platform for behavioral research in economics and psychology, by providing real-time transmission of gaze data among participants during experiments. It is optimized for efficient handling, processing, and transmission of large volumes of biodata in real-time, while ensuring the protection of personal data by operating within a local data environment and avoiding dependence on third-party providers. As such, oGaze serves as a crucial open-source extension for oTree, enabling researchers to incorporate and analyze biosignals, such as gaze data, in their experiments in a standardized and secure manner.


## Table of Contents

- [oGaze — An Advanced Biosignal Interface for Gaze-Centric Economic Experiment](#ogaze--an-advanced-biosignal-interface-for-gaze-centric-economic-experiment)
  - [Table of Contents](#table-of-contents)
- [1. Technical Function and Practical Use](#1-technical-function-and-practical-use)
- [2. Quick Guide](#2-quick-guide)
  - [2.1 Preparation](#21-preparation)
  - [2.2 Initital Setup and Usage](#22-initital-setup-and-usage)
  - [2.3 Quick Guide FAQ](#23-quick-guide-faq)
- [3. Theory of Functioning](#3-theory-of-functioning)
    - [3.1 Network Components: TimescaleDB, oTree and Clients](#31-network-components-timescaledb-otree-and-clients)
    - [3.2 StartProgram](#32-startprogram)
      - [3.2.1 Functionality](#321-functionality)
      - [3.2.2 Graphical User Interface (GUI)](#322-graphical-user-interface-gui)
    - [3.3 StartPage](#33-startpage)
    - [3.4 Eye Tracking Data](#34-eye-tracking-data)
    - [3.5 Eye Tracking Visualizations](#35-eye-tracking-visualizations)
    - [3.6 Repository Overview](#36-repository-overview)
      - [The vienna\_experiment folder](#the-vienna_experiment-folder)
      - [The static folder and README file](#the-static-folder-and-readme-file)
    - [3.6 Code Structure](#36-code-structure)
      - [Python Functions](#python-functions)
      - [Python Classes](#python-classes)
      - [JavaScript Functions](#javascript-functions)
      - [JavaScript Classes](#javascript-classes)
    - [Other Important Functions](#other-important-functions)
- [4. Frequently Asked Questions (FAQs)](#4-frequently-asked-questions-faqs)
    - [4.1 What pre-built visualisation does oGaze contain?](#41-what-pre-built-visualisation-does-ogaze-contain)
    - [4.2 How to adjust the pre-built visualizations to your own needs?](#42-how-to-adjust-the-pre-built-visualizations-to-your-own-needs)
    - [4.3 How can biofeedback be presented to specific participants only?](#43-how-can-biofeedback-be-presented-to-specific-participants-only)
    - [4.4 Why does the oGaze repository contain each experiment multiple times?](#44-why-does-the-ogaze-repository-contain-each-experiment-multiple-times)
- [5. Appendix](#5-appendix)
  - [5.1 Contributing](#51-contributing)
  - [5.2 Scientific Background](#52-scientific-background)
  - [5.3 License](#53-license)

# 1. Technical Function and Practical Use
The continuous development of economic experiments, particularly in an academic setting, is vital for unveiling fresh insights in research. Customized applications like labjs and oTree are becoming increasingly favored due to their design, which is specifically tailored for economic experiments. These tools facilitate the creation of interactions and visualizations in economic experiments by offering standardized programming functionalities, accompanied by detailed instructions for researchers. However, executing complex experiments involving real-time biosignal transmission is only partially feasible with these applications and often comes with challenges. This limitation is attributed to oTree's constrained ability to transmit large volumes of data, such as eye tracking, in real time, and the absence of standardized add-on solutions for oTree.

Enter oGaze, a solution designed to harness the full potential of oTree and, through a suitable extension, enable the execution of economic experiments involving real-time biosignal transmission between multiple participants. oGaze represents a comprehensive solution adaptable to various biosignals and experiments. The development, verification, validation, and explanation of oGaze are illustrated using two well-known economic experiments: the prisoner's dilemma and a Dutch auction. These experiments facilitated the real-time transmission of gaze direction and pupil width as indicators of arousal. The implementation of oGaze involved considering several influencing factors, detailed in the following section.

Firstly, the study design must be customized to the infrastructure of the specific research institution. Often, the infrastructure provided by various universities facilitates the standardized implementation of such experiments onsite. This infrastructure includes several computers and the university's intranet. Moreover, conducting experiments locally necessitates the connection of additional devices required for biosignal acquisition. Hence, oGaze offers a standardized installation and setup procedure, enabling its use over the local network without the need for third-party servers. This feature makes oGaze accessible to researchers with limited programming experience while ensuring high levels of data protection during biofeedback data experiments.

Secondly, the live transmission of biosignals involves the transmission and storage of a considerable volume of data. For instance, a single eye-tracking experiment can accumulate over 12 million data points per participant. To ensure seamless operation without delays, oGaze mandates that each client independently writes its own data and reads the necessary data. Additionally, the data is centrally stored in a time-scale database optimized for handling large data volumes.

# 2. Quick Guide
The Quick Guide is designed to provide a concise and straightforward overview of the necessary steps to ensure a smooth installation and execution of the oGaze tool. It will walk you through the essential processes, from installing required Python libraries to setting up the TimescaleDB and oTree components.

The primary aim of this Quick Guide is to:

* Simplify the technical jargon and present the steps in an easy-to-understand manner.
* Offer a step-by-step approach to setting up both the hardware (eye tracker) and software components.
* Ensure that users, regardless of their technical expertise, can follow along and successfully set up the experiment.

By the end of this guide, you should have a clear understanding of the installation process, initial setup, and usage of the developed prototype for the experiment. 
Let's dive in and get started!


## 2.1 Preparation


It is recommended to begin the installation by setting up a virtual environment on the server that runs the oTree experiment. Once the virtual environment has been established and activated, oGaze requires a set of various Python libraries, which are listed in the `requirements.txt` file.
To install these libraries, run:

```bash
pip install -r requirements.txt
```
The oGaze tool was developed for the `Tobii Eye Tracker 4 Pro`. If exactly this eye tracker is used, the corresponding eye tracking software for the eye tracker must be installed on each of the client devices, i.e. the devices on which the study participants will later take part in the experiment. [*Tobii Eye Tracking Software*](https://gaming.tobii.com/getstarted/) 
If another type of eye tracker is used, this is theoretically possible. In this case, adjustments may have to be made to the application and its code base.

## 2.2 Initital Setup and Usage

The initial setup and use oGaze is explained below, assuming that all services and components are set up and configured as required by oTree.

1. TimescaleDB
    - Before conducting the experiment, the TimescaleDB database server must be set up. 
    - It must be accessible in the local network and has to be in the same network as the oTree server and the client devices. (check firewall) 
    - The access data (IP, username, password, database, table) for a user with read and write rights must be written directly into the programme code of the oTree application and in the StartProgram on the clients devices.
    - [*Setup local TimescaleDB server via Docker*](https://docs.timescale.com/self-hosted/latest/install/installation-docker/)

2. Clients & eye tracker
    - Participants need a computer with a mounted eye tracker. 
    - The Tobii Eye Tracker 4 Pro requires the `Tobii Eye Tracking Software` to be installed on the devices. On the one hand, to calibrate the EyeTracker for each participant and, on the other hand, to be able to communicate reliably with oGaze.

  
3. oTree
    In order to integrate oGaze into your oTree environment, you need to setup an oTree project.
    ```bash
    otree startproject myproject
    cd myproject
    ```
    Copy the folder *vienna_experiment* of this repository into your *myproject* folder.

    To start the experiment in development mode, run the following command. For this command to workyou need to be in the vienna_experiment folder:

    ```bash
    cd vienna_experiment
    otree devserver
    ```
    Then open a web browser and go to http://localhost:8000.

    To start the experiment in production, run the following command:

    ```bash
    otree prodserver 8000
    ```
    Next, open a web browser and go to http://localhost:8000. 
    External clients need the IP address of the server in order to access the oTree experiment via http://SERVER-IP:8000.
    [*Further oTree instructions*](https://otree.readthedocs.io/en/latest/install-nostudio.html)

4. Final Setup
  After the Timescale database server, the client computers and the oTree/oGaze server have been set up and are running, you can proceed with the final setup. 
  * To do this, call up the IP address of the oTree/oGaze server on the client computers in the browser and land on the StartPage of the oGaze tool. At the top right there is a green button with the label `Download InitAssistant`. 
  * Download the InitAssistant (synonymous with StartProgram) and execute the [*StartProgram*](#32-StartProgram).
  
  *You should now be able to conduct an experiment based on the pre-designed study with live biosignals. You can now adapt it as you wish, or integrate the mechanisms and visualisations into your own experiments.*

## 2.3 Quick Guide FAQ

* [What pre-built visualisation does oGaze contain?](#41-Whatpre-builtvisualisationdoesoGazecontain?)
* [How to adjust the pre-built visualizations to your own needs?](#42-Howtoadjustthepre-builtvisualizationstoyourownneeds?)
* [How is the IPA metric calculated?](#43-HowistheIPAmetriccalculated?)
# 3. Theory of Functioning 
The oGaze Prototype consists of a number of components that interact in order to enable scientists to conduct economic experiments involving real-time biosignal transmission between multiple participants with live bio-feedback such as eye tracking data in a realiable, scalable and data secure manner. 
![IT Infrastructure Model](/static/img/networkComponents.svg)
### 3.1 Network Components: TimescaleDB, oTree and Clients

The programme was developed to meet the high data protection standards in a scientific project with sensitive data. Therefore, the complete communication of all network components takes place within an intranet and is stored locally.

oGaze uses TimescaleDB for storing eye-tracking data. TimescaleDB is a PostgreSQL database with time-series functionality and an IOT-opimised operation. The connection to the TimescaleDB is established using the `psycopg2` library.

The oTree backend is used for the experiment logic. oTree is an open-source platform for behavioral research in economics, psychology, and other fields.

The clients communicate with the oTree server via http on the intranet. In addition to interacting with the oTree server to conduct the experiments, the eye trackers of the individual participants continuously send data to the clients computer which redirects the data to the TimescaleDB server located on the intranet. 


![Communication Layer](/static/img/RIRO2.png)

### 3.2 StartProgram
#### 3.2.1 Functionality
The StartProgram is a part of oGaze that performs a variety of tasks related to the initialization of the clients computer and the operation of a Tobii Pro eye tracker. This program is designed to be used in conjunction with a TimescaleDB database for storing and retrieving eye tracking data and an oTree server to map each eye tracker with the regarding participant of the oTree experiment.

The StartProgram operates in several stages:

1. **Generating Unique ID (mappingID)**: The function `generate_unique_id()` is used to create a unique identifier, known as the mappingID. This ID is used to map the collected gaze data to a specific participant. The mappingID is also sent to the web application running the experiment, allowing the data to be associated with the correct participant and session in the experiment.
   
2. **Establishing a Database Connection**: The `establishConnection(serverIP)` function is used to connect to a TimescaleDB database. It takes the database server IP address as an input. If the table does not exist, the StartProgram will create a new table with the correct data structure. *It is recommended to let the start program create the table automatically.*

3. **Initializing the Eye Tracker**: The `initializeTracker()` function is used to detect the connected eye tracker device and initiate communication with it.

4. **Checking and Applying Licenses**: The `checkLicense(license_file)` function is used to apply the license to the eye tracker.

5. **Starting the Tracking**: The `startTracking(serverIP, filepath, tmp_mappingID)` function is used to start the eye tracker and begin collecting gaze data. This function also initiates the connection to the database.

6. **Stopping the Tracking**: The `stopTracking()` function is used to stop the eye tracker and terminate the connection to the database.

7. **Data Collection and Processing**: During tracking, gaze data is collected and processed in real-time. The gaze data includes information such as gaze origin, gaze point, and pupil diameter. This data is then used to calculate gaze averages, and other metrics such as the Index of Pupillary Activity (IPA).
   
![SetupProcess](/static/img/RIRO1.png) 

#### 3.2.2 Graphical User Interface (GUI)
The StartProgram provides a graphical user interface (GUI) built with Tkinter for user-friendly interaction. The GUI contains several input fields and buttons for operations such as entering the oTree server IP address, initiating and stopping the tracking process, and selecting the license file.

Key elements of the GUI include:

*IP Address Input Field*: Where the user enters the IP address of the PostgreSQL server.

*Start and Stop Buttons*: Buttons that initiate and stop the eye tracking process.

*File Selection Button*: Allows the user to select the license file required to operate the eye tracker.

*Text Widget*: Displays the output from the StartProgram, allowing the user to monitor the status of the eye tracker and the data collection process.

*Label for Instructions*: Guides the user through the process of using the application by providing timely instructions.

![GUI](/static/img/GUIStartProgram.png)

### 3.3 StartPage
The StartPage is first in the order of the oTree pages. 
**Initial setup of the client**
1. during the first setup of the clients, the StartPage can be called manually via the IP address of the oTree server. 
2. by clicking on the green button ("Download InitAssistant") in the upper right corner, the initialization assistant (StartProgram) can be downloaded to the client computer. 

**Regular operation**
1. In regular operation, the StartPage is automatically called by the client via the executed StartProgram. 
2. in this process the browser opens, which reads and saves the StartPage. 
3. with a few seconds delay the page opens again and the InitAssistant transmits the *mappingID* of the client to oTree in order to link the data of the EyeTracker with the *participantID* (and thus the client) unambiguously. 
4. oTree server updates the StartPage by the transmission. As a result, the StartPage displays the *mappingID* and only now displays the *Next* button to start the experiment. 
5. If you click on the *Next* button, the actual start page of the experiment follows, which is intended for the participant.



![StartPage1](/static/img/InitAssistant.png) |  ![StartPage1](/static/img/InitAssistant2.png) 
:-------------------------:|:-------------------------:


### 3.4 Eye Tracking Data 
The Tobii Pro eye tracker is a high-performance device that tracks eye movement and pupil dilation with a 90 Hz frequency. It provides besides other data detailed and precise data about where a person is looking (gaze point), the position of the eye (gaze origin), and the size of the pupil (pupil diameter). These data points are critical for understanding a person's visual attention and cognitive load.

The eye tracker provides the following data:

1. **Device Time Stamp**: The time at which the data was recorded by the device.
2. **Gaze Origin**: The point in 3D space from which the gaze vector originates, in both the trackbox coordinate system and the user coordinate system.
3. **Gaze Point**: The point in 3D space that the user is looking at, in both the user coordinate system and the display area coordinate system.
4. **Pupil Diameter**: The diameter of the pupil, provided for both the left and right eye.
5. **Validity Flags**: Indicators of the validity of the gaze origin, gaze point, and pupil diameter data, for both the left and right eye.
6. **Metrics**: Metrics such as the Index of Pupillary Activity (IPA) are used to interpret eye tracking data such as pupil dilation and make connections to cognitive load or stress, for example.
  
This data is collected continuously while the tracker is running, providing a real-time stream of data. The data is processed and used for various analyses, such as determining the average gaze position and calculating the IPA. The IPA is a measure of the rapid, minute fluctuations in pupil 
diameter, which can be an indicator of cognitive workload or arousal.

Every 30 datapoints are streamed to the TimescaleDB database.

![Dataponts](/static/img/datapoints.png) 



#### 3.4.1 Real-Time IPA 

TThe `calculate_normalized_ripa` function computes the normalized Real-time Index of Pupillometric Activity (RIPA) from raw pupil diameter data. The function takes five parameters: `raw_data`, `buffer_length`, `m_sg`, `n_sg`, and `threshold_factor`.

1. **Low-pass and High-pass Filtering**: The function first applies a Savitzky-Golay filter to the raw data to compute the low-pass filtered data (`x_lowpass`). The high-pass filtered data (`x_highpass`) is then computed by subtracting the low-pass filtered data from the raw data.
    
2. **Low-to-High-Frequency Ratio**: The ratio of the low-pass to high-pass filtered data (`x_ratio`) is computed.
    
3. **Modulus Maxima**: The modulus maxima (`m`) of `x_ratio` is then computed. This involves iterating over `x_ratio` and assigning to `m` the value of `x_ratio` at a given point if it is greater than the values immediately before and after it.
    
4. **Threshold Calculation**: A threshold is calculated as the product of `threshold_factor` and the standard deviation of `m`.
    
5. **RIPA Computation**: The RIPA count is computed as the sum of the absolute values of `x_ratio` that are greater than `m` plus the threshold.
    
6. **Normalization**: The RIPA is then normalized by subtracting the RIPA count divided by the buffer length from 1.

The function returns the normalized RIPA.



### 3.5 Eye Tracking Visualizations 

### 3.6 Repository Overview
The repository contains in the top hierarchy level:
* the *vienna_experiment folder* 
* the *static folder*  
* the *README file* .

#### The vienna_experiment folder
The *vienna_experiment folder* contains:
* the *startPage, payout, game and questionnaire folders* with their respective logic, functionalities and design.
* the *static folder* with the *startProgram*, the locally stored *javascript libraries* and all the *images* needed to visualize the instructions.
* the *db.sqlite3 file* that contains all the data generated by oTree.
* the *settings.py* that contains the configuration settings for the oTree experiment, such as the order of the pages, or the amount of sessions or players per session.

#### The static folder and README file
The *README file* contains all the information needed to install,run and modify the prototype. The *static* folder contains images to illustrate the contents of the *REAMDE file*.




### 3.6 Code Structure

#### Python Functions

- `startTracking(serverIP, file_path, mappingID)`: Starts the eye tracking.
- `calculate_normalized_ripa(raw_data, buffer_length, m_sg, n_sg, threshold_factor)`: Calculates the Real-Time IPA for each eye 
- `ipa(dilation_data)`: Calculates the LHIPA. Outdated and currently not in use.
- `modmax(d)`: Computes signal modulus. 
- `checkLicense(license_file)`: Checks the license.
- `format_gaze_data(input_tuple)`: Preprocesses the gaze data.
- `stopTracking()`: Stops the eye tracking.
- `establishConnection(serverIP)`: Establishes a connection to the Timescale database.
- `button_clicked(entry.get())`: Called when the 'Init' button is clicked in the GUI.
- `file_clicked()`: Called when the 'Choose File' button is clicked in the GUI.
- `startTimescaleDBConnection(file_path)`: Called when the 'Start TimescaleDB Connection' button is clicked in the GUI.
- `generate_unique_id()`: Generates a unique ID.
- `get_plot(self)`: Creates a Pupil Dilation Visualization for each player.
- `creating_session(subsession)`: Creates a session for the oTree experiment.
- `set_winner(group)`: Sets the winner of a group in the oTree experiment.


#### Python Classes

- `Constants(BaseConstants)`: Defines constants for the oTree experiment.
- `Subsession(BaseSubsession)`: Defines a subsession for the oTree experiment.
- `Group(BaseGroup)`: Defines a group for the oTree experiment.
- `Player(BasePlayer)`: Defines a player for the oTree experiment.

#### JavaScript Functions

- `posData()`: Gets the positions and sizes of the buttons relative to the viewport and the document.
- `getCellPosition(cellId)`: Gets the position of a cell in a table.
- `downloadZip()`: Downloads a zip file.

#### JavaScript Classes

- `base-timer`: Styles the timer in the HTML templates.
- `base-timer__svg`: Styles the SVG in the timer.
- `base-timer__circle`: Styles the circle in the timer.
- `base-timer__path-elapsed`: Styles the elapsed path in the timer.
- `wide-button`: Styles the buttons in the HTML templates.

### Other Important Functions

- The project uses a unique mapping ID for each participant. This ID is generated using the `generate_unique_id()` function.
- The project uses JavaScript for updating the graph using the `updateGraph()` function. This function is called every 1000 milliseconds.
- The project uses the `liveRecv(data)` function to receive live data. This function is used to update the graph and show the results.
- The project uses the `liveSend({'type': 'load'});` function to send live data.

# 4. Frequently Asked Questions (FAQs)

### 4.1 What pre-built visualisation does oGaze contain?
<details><summary>Area of Interest (AOI) visualization</summary>
The Area of Interest (AOI) visualization remains static, based on predefined AOIs. In order to use the visualization, it is necessary to adapt the specific areas individually to the experiment. However, challenges posed by varying screen resolutions are mitigated by oGaze automatically. It dynamically converts the resolutions and sizes of the different screens and browsers. Therefore, a manual adjustment to different screens or browsers is not necessary. The AOI visualization shows the gaze data of the opponent in real-time. 
</details>
<details><summary>Visualization of pupil dilation Var1</summary>
The visualization of pupil dilation in the form of the IPA metric uses a simple gauge visualization. It is detached from different experiments and screen resolutions and can therefore be reused for other games without adaptation. 
</details>
<details><summary>Visualization of pupil dilation Var2</summary>
The third visualization displays two eyes, where the pupil either expands or contracts based on the opponent's pupil size variation. The changes are calculated in relation to a baseline that is different for each participant. This baseline is currently the first value of the respective participant. Relative to the baseline, the pupil displayed by oGaze can either expand or contract by 50\%. 
</details>
<br></br>

![Visualizations](/static/img/Vis.png) 

### 4.2 How to adjust the pre-built visualizations to your own needs?
The code for the individual visualisations is directly embedded in the code of the individual oTree experiments. Initialisation takes place via method calls, using oTree's own `liveSend`/`live_method`/`liveRecv` methods for this and also for the ongoing synchronisation.

### 4.3 How can biofeedback be presented to specific participants only?

According to the study design for which oGaze was developed, in some games the live biofeedback of the player is only shown to a specific player. This is done in the frontend, i.e. the `.html` file of the respective experiment. In the `_init.py` of the experiment, the following code is used to select only the players with even Ids from a group. 
```bash
  def vars_for_template(self):
        is_even = self.id_in_group % 2 == 0
        return {'is_even': is_even}
```
In a game with 2 participants, only `player 2` is selected under the variable `is_even`. In the fontend, i.e. the `.html` file, the visualisation is only displayed if `is_even` is `True`. This means that the visualisation is only displayed when `player 2` calls up the page. Consequently, `player 1` does not see the visualisation. 


### 4.4 Why does the oGaze repository contain each experiment multiple times?

According to the study design for which oGaze was developed, different conditions exist under which the experiments are conducted. In addition, there are two different visualisations for the Dutch Auction, which were implemented in separate experiments. 

# 5. Appendix
## 5.1 Contributing
Contributions are welcome! 

## 5.2 Scientific Background
For more information, especially about the scientific background of the development of oGaze and the study in the framework of which oGaze was developed, please see the accompanying paper.

## 5.3 License
This project is licensed under the terms of the MIT license. See the LICENSE file for details.
