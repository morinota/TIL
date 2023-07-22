## title

Implementing a Stateful Architecture with Streamlit

## link

https://towardsdatascience.com/implementing-a-stateful-architecture-with-streamlit-58e52448efa1

## Streamlit

Streamlit has come a long way since its inception back in October of 2019. It has empowered the software development community and has effectively democratized the way we develop and deploy apps to the cloud. However as with all new tools, there is still some way to go, and while the Streamlit team works tirelessly on addressing requests for new features, we developers ourselves can create ad hoc work arounds in the meantime.

A feature that Streamlit currently lacks, is the ability to implement programmable state for its apps. In its current form, there is no internal state that can store volatile data such as user inputs, dataframes and values entered into widgets. Given that Streamlit innately re-runs the entire script when the user triggers an action in the event of pressing a button or switching between pages, the app will reset all inputs and dataframes. While for many applications, this is a non-issue, for others it can be a deal breaker. Just imagine if you are trying to build an app with sequential logic using incremental steps, the absence of a stateful architecture would render Streamlit as an unsuitable framework. The founders have committed to releasing a stateful version in the near future, but until then, one can use an open source database such as PostgreSQL to develop a hack as I will explain below.

## PostgreSQL

PostgreSQL or Postgres for short is a free and open source relational database system that is often the database of choice for most developers due to its ease of use and extended capabilities. While it is ostensibly a structured database management system, it can also store non-structured data such as arrays and binary objects, which makes it rather useful for open-ended projects. In addition, its graphical user interface is highly intuitive and straightforward ensuring that the learning curve is very shallow.

In our implementation of a stateful architecture, we will be using a local Postgres server to store our state variables such as the user inputs and dataframes generated in our Streamlit app. Before we proceed, please download and install Postgres using this link. During the installation you will be prompted to configure a username, password and local TCP port to forward your database server to. The default port is 5432 which you may keep as is. Once the installation is completed, you will be able to login to your server by running the ‘pgAdmin 4' application which will then open your server’s portal on your browser as shown below.

By default there should also be a database called ‘Postgres’ shown in the left sidebar, if there isn’t however, you may right click on ‘Databases’ and select ‘Create’ to provision a new database.

## Implementation

Now that we got the logistics out of the way, lets head over to Python for our implementation. Aside from the usual suspects (Pandas and obviously Streamlit itself) you will also need to download the following packages.

## Sqlalchemy

We will be using this package to create and execute our SQL queries. Sqlalchemy makes it rather simple to write complex queries and if you are passing your query strings as parameters (not concatenated) it has anti-SQL-injection capabilities that ensure your queries are secure. You can download it using the following command.

In addition, we will need to import a method called ‘get_report_ctx’ from the Streamlit library. This function creates a unique session ID every time we run our app. This ID will be associated with each of our state variables to ensure that we are retrieving the correct states from our Postgres database.

Proceed by importing the following packages into your Python script.

First we will create a function that extracts the session ID of our app instance. Please note that the ID is updated each and every time the app is refreshed i.e. when you hit F5. Since the session ID will be used as the name of the tables storing our state variables, we will need to adhere to Postgres’s table naming convention which decrees that names must start with underscores or letters (not numbers), must not contain dashes and must be less than 64 characters long.

Next we will create four functions that can be used to read and to write the states of our user inputs and dataframes from Streamlit to Postgres as follows.

Now we will create the main function of our multi-page Streamlit app. First we setup the PostgreSQL client using a connection string that contains our username, password and database name. Please note that a more secure way to store your database credentials is to save them in a configuration file and then to invoke them as parameters in your code. Then we acquire our session ID which should look something along these lines:

Subsequently, we will create a table with one column called ‘size’ with a datatype of ‘text’ using the current session ID. We need to ensure that every time our state variable is updated, it is overwritten on the previous state. Therefore we will query the length of the table and if it is zero we will insert a new row with the state. Otherwise we will just update the existing row if a previous state from the current session ID already exists.

Finally we will create two pages that can be toggled using a ‘st.selectbox’ in the sidebar. The first page contains the text ‘Hello world’ and the second page contains a text input widget that is used to generate a sparse matrix with the corresponding size specified by the user. The state of the text input and generated dataframe is saved into our Postgres database and is queried every time the script is re-run by Streamlit itself. Should the script find an existing state within the same session ID, it will update the input and dataframe accordingly.

## Results

Running the app naturally with a stateless implementation resets the text input and dataframe each time we toggle the page as shown below.

However, running the app with the stateful implementation achieves a persistent state, whereby the text input and dataframe are being stored and retrieved even after we toggle the pages as shown below.

Concurrently, you can also see that our Postgres database is being updated in real time with our state variable and dataframe as shown below.

Any other variable can have its state saved and read with the following commands:

Similarly, any dataframe can be saved and read with the following commands:

## Conclusion

This method can be extended to other widgets and can also be used to store binary files that are generated or uploaded to Streamlit. In addition, if one would like to track their user’s inputs or would like to record timestamps with each action then this method can be further extended to address such features. The only caveat here is that not all widgets in Streamlit have values that can be stored, for instance, ‘st.button’ serves only as an event trigger and does not have a value associated with it that can be saved as a state.

If you want to learn more about data visualization, Python, and deploying a Streamlit web application to the cloud then check out the following (affiliate linked) courses:
