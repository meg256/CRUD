# Streamlit CRUD 
A simple Streamlit app for interfacing with a Google sheets-based database: Create, Read, Update, Delete

The code as written requires a Google API access json (https://console.developers.google.com/apis/credentials). The app requires authentication on first use and stores credentials for use thereafter. 

The toy database was designed as a recipe tracker, with base component + additives plus an indicator column indicating whether it is a "standard" formulation. Users can display standards or add a novel formulation.

The app also contains a very primitive search function, which accepts a comma-delimited list of search terms and returns any matches to values in a database row. 
