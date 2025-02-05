# End to End Machine learning System
### System Architecture
https://github.com/qandos-git/end-to-end-machine-learning-system/blob/main/images/System%20Architecture%20.png

## Overview

This project builds an automated end-to-end machine-learning pipeline, the goal of this automation is to deploy a new model whenever there is new data and make it available for the user.
To implement these concepts, we used simple weather API ([Visual Crossing API](https://www.visualcrossing.com/)), to store historical data about weather in Buraidah city, then we trained a simple regression model on the available data, built a flask application, and finally deployed the app on Google cloud run.
The project idea will not change the world 😺, this project is just about understanding the flow to solve more complex and useful problems in the future. 

## Features
- **Automated Data Pipeline**: Retrieves, transforms, and loads weather data from the Visual Crossing API into BigQuery on a weekly schedule.
- **Model Training**: Builds a Ridge regression model using scikit-learn pipelines, achieving an R² of 0.99.
- **Orchestration with Mage**: Automates the entire workflow, ensuring the model updates with new data.
- **Flask Web App**: Provides an interactive interface for users to check daily "feels like" temperature predictions.
- **Cloud Deployment**: Uses Docker and Google Cloud Run to make the app accessible online.- 


## System main Components:
1. **Data Extraction**: Fetches data from the **Visual Crossing API**, including Date and time (datetime), Minimum temperature (min_temp), Maximum temperature (max_temp), Average temperature (temp), and feeling like (feelslike).
   (output)
3. **Data Transformation**: Converts raw data into a structured format by:
    - Change (datetime) to datetime data type.
    - Renaming and rearranging columns
    - Creating new features like day_of_week (e.g., Monday, Tuesday) and temp_range (difference between max and min temperatures)

5. **Data Loading**: The transformed data is uploaded to **BigQuery** into a Buraidah table.

6. **Automation**: This process runs weekly using **Mage**, an orchestration tool, that automates data pipeline.

7. **Model building**: train **Ridge regression** model that achieved R2 of **0.99** with sklearn pipeline to predict feeling like (feelslike) attribute.  This model is simple and good for small datasets such as our case.

8. **Interface**: using **Flask** to build an interactive interface for users to check daily predicted feelings like temperature.

9. **Deployment**: **Docker** and **Google Cloud Run**, and now the interface is online! 🤠


## Access the interface
Check out the weather in Buraidah 🌞 [App link](https://project-240296351992.asia-east1.run.app/)

I am using a free trial so the app could be removed anytime 🫥 so check out the docker instructions!

## Docker instructions
1. Build docker image (Docker must be running in the background)
   
       `docker build -t my-app . `
   
2. Run image
   
       `docker run -p 8080:8080 -e PORT=8080 my-app`


## Limitations
1. I prefer to use Google Cloud storage to store the database state, but after lots of bugs, I decided to use local storage.
2. There is no meaning in checking the data daily, as it is scheduled to be updated weekly.
3. Mage is good for data engineering and weak in building end-to-end systems, I don't think I would use it again 😅

## Resources
[Deployment](https://lesliemwubbel.com/setting-up-a-flask-app-and-deploying-it-via-google-cloud/)

[Mage documintaion](https://docs.mage.ai/introduction/overview)
