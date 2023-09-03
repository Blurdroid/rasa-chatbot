# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import sqlite3
from sqlite3 import Error
from typing import Any, Dict, List, Text, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class GetFromSQLite_max(Action): # max student
    def name(self) -> Text:
        # return "action_get_data_from_sqlite"
        return "action_get_max_student"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('resourceDB.db')
            cursor = conn.cursor()

            # Execute an SQL query to retrieve the data
            query = "SELECT name FROM students WHERE total_marks= 100;"
            cursor.execute(query)

            # Fetch all the results
            results = cursor.fetchall()

            # Process the results as per your requirement
            response = "retreiving from database:.."
            for row in results:
                response += row[0] + ", "

            # Send the response to the user
            dispatcher.utter_message(response)

        except Error as e:
            dispatcher.utter_message("An error occurred while retrieving maximum total marks from the database.")

        return []

class GetFromSQLite_min(Action):
    def name(self) -> Text:
        return "action_get_min_student"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('resourceDB.db')
            cursor = conn.cursor()

            # Execute an SQL query to retrieve the data
            query = "SELECT name, min(total_marks) FROM students;"
            cursor.execute(query)

            # Fetch all the results
            results = cursor.fetchall()

            # Process the results as per your requirement
            response = "retreiving from database:.."
            for row in results:
                response += row[0] + ", "

            # Send the response to the user
            dispatcher.utter_message(response)

        except Error as e:
            dispatcher.utter_message("An error occurred while retrieving minimum total marks from the database.")

        return []

class GetFromSQLite_getmarks(Action):
    def name(self) -> Text:
        return "action_get_name_marks"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('resourceDB.db')
            cursor = conn.cursor()

            # Execute an SQL query to retrieve the data
            slot_value = tracker.get_slot('name')
            user_input = tracker.latest_message
            cursor.execute("SELECT name FROM students")
            rows = cursor.fetchall()
            query_name_list = [list(row) for row in rows] # convert sqlite3.cursor into list
            dispatcher.utter_message(slot_value) # to see what inside slot_value

            if [slot_value] not in query_name_list:
                dispatcher.utter_message("I can't find the student in the database!")
            else:
                # query = f"SELECT total_marks FROM students WHERE name={slot_value};" # to prevent SQL injection
                query = "SELECT total_marks FROM students WHERE name=?;"
                cursor.execute(query, (slot_value,))
                results = cursor.fetchall()
                if results:
                    dispatcher.utter_message(str(results))
                else:
                    dispatcher.utter_message("empty!")
        except Error as e:
            dispatcher.utter_message(f"An error occurred while retrieving total marks from the database.")    


# class GetFromSQLite_getmarks(Action):
#     def name(self) -> Text:
#         return "action_get_name_marks"
    
#     def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
#             # Retrieve the specific entity from the latest message
#             entity_value = None
#             latest_message = tracker.latest_message

#             if 'entities' in latest_message:
#                 entities = latest_message['entities']
#                 for entity in entities:
#                     if entity['entity'] == 'your_entity_name':
#                         entity_value = entity['value']
#                         break  # Exit loop if entity is found

#             # Read the required information from the user's input
#             # entity_value = tracker.latest_message.get("entities")[0].get("value")

#             # Connect to the SQLite database
#             conn = sqlite3.connect('resourceDB.db')
#             cursor = conn.cursor()

#             # Execute an SQL query to retrieve the data
#             query = f"SELECT total_marks FROM students WHERE name='{entity_value}';"
#             # bindings= (entity_value,) 
#             cursor.execute(query)

#             # Fetch all the results
#             results = cursor.fetchall()

#             if results is not None:
#                 column_name, column_value = results
#                 response = "The total marks of " + entity_value + " is " + int(column_value) #INT -> because the column name is total_marks ex:100
#             else:
#                 response = "No data found for "

#             # Process the results as per your requirement
#             # response = "retreiving from database:.."
#             # for row in results:
#             #     response += row[0] + ", "

#             # Send the response to the user

#             dispatcher.utter_message(results)

#             return []