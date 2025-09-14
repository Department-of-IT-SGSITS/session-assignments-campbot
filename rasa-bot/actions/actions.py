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

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import datetime

# This is a custom action to log unanswered queries.
# The `utter_fallback` response is sent after this action.
class ActionLogUnansweredQuery(Action):
    def name(self) -> Text:
        # The name of the action. It must match the name in domain.yml.
        return "action_log_unanswered_query"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the user's latest message and the current timestamp.
        user_message = tracker.latest_message.get('text')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log the user's message to a text file. In a real-world scenario,
        # you would log this to a database for easier analysis.
        log_entry = f"{timestamp} - Unanswered Query: '{user_message}'\n"
        with open("unanswered_queries.txt", "a") as log_file:
            log_file.write(log_entry)
        
        # The action_log_unanswered_query itself does not send a response,
        # it simply logs the message. The RulePolicy in stories.yml
        # will handle the `utter_fallback` response.
        return []
