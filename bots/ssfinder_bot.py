# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import re
import phonenumbers
import json
import os
import random
import csv
import numpy as np
import uuid
import pickle
import seaborn as sns

import matplotlib.pyplot as plt


#import PySide2
import pandas as pd
from pandas import DataFrame

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext, CardFactory
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions, Attachment, Activity, ActivityTypes
from validate_email import validate_email
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OneHotEncoder

CARDS = [
    "resources/Choice_Card1.json",
    "resources/Choice_Card2.json",
    "resources/Choice_Card3.json",
    "resources/Choice_Card4.json",
    "resources/Choice_Card5.json",
    "resources/Choice_Card6.json",
    "resources/Choice_Card7.json",
    "resources/Choice_Card8.json"
]

userResponseDataBase = open("UserResponseDataBase.txt", "a")

userResponseCSV = pd.read_csv("UserResponse.csv")




#userResponses = open("UserResponse.csv", 'w')

#userResponses.close()



#userResponseCSV.insert(1,"Question3","test")



print(userResponseCSV.head())

userAnswers = pd.Series([])

userResponseDataBase.write("Respondent \n")
approach = False
ideas = False
socialGatherings = False
counter = 0;
counterName = 0;
my_number = 0;
phoneNumberCounter = 0;
nonetypeCounter = 0;
inputCounter = 0;
contactDetailsCounter = 0;
emailCounter = 0;
excelCounter = 0;
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

recommendationString = ""

card1Inputs = ["<2", ">2-4", ">4-6", ">6-10", ">10-15", ">15-20", ">20"]
card2Inputs = ["Get a better job", "Become an expert in the field so that market approaches me", "Start my own business", "Continue with family business", "My interest", "Market trend", "Wider range of career options", "High earnings"]
card3Inputs = ["Operations", "Business Head", "Human Resource", "Information Technology", "Marketing", "Finance", "None of the above"]
card4Inputs = ["< $10,000", "$11,000 - $20,000", "$21,000 - $50,000", "$51,000 - $80,000", "> $80,000"]
card5Inputs = ["I don't mind working with people, but I like working alone", "I like working in a team", "I like leading people"]
card6Inputs = ["I like giving presentations", "I like qualitative work more than the quantitative one", "I am good at managing data and information", "I have an eye for detail"]
card7Inputs = ["I go to the gym", "I like doing volunteer work", "I like doing household work and home improvement", "I like learning, creating art forms, music and designing"]
card8Inputs = ["Social Science", "Language", "Science", "Maths"]


MBAPredictionChoice = ["Finance", "Marketing", "Operations", "Human Resources", "Information Technology"]

class SSFinderBot(ActivityHandler):
    """
    This bot will respond to the user's input with suggested actions.
    Suggested actions enable your bot to present buttons that the user
    can tap to provide input.
    """

    

    

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Send a welcome message to the user and tell them what actions they may perform to use this bot
        """

        return await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to the users choice and display the suggested actions again.
        """
        global counterName;

        global my_number; 
        
        global phoneNumberCounter;

        global nonetypeCounter;

        global inputCounter;

        global contactDetailsCounter;

        global emailCounter;
        global excelCounter;

        global recommendationString;
        
        NoneType = type(None)

       

        

        #print("nonetypeCounter: ")
        #print(nonetypeCounter)
        print(turn_context.activity.channel_id)

        if type(turn_context.activity.text) == NoneType:

            result = str(turn_context.activity.value) 

            spl_word = ':'
            rem_char1 = "}"
            rem_char2 = "'"


            partition_word = result.partition(spl_word)[2]
            trimmed_word = partition_word.strip()
            no_curly_braces = trimmed_word.replace(rem_char1, "")
            userSelection = no_curly_braces.replace(rem_char2, "")
            
            #print("Result is: ")
            #print(userSelection)
            self._DataBaseAdder(userSelection, inputCounter)
            inputCounter = inputCounter + 1   
            
            #print("Value: ")
            #print(turn_context.activity.value)

            if nonetypeCounter == 0:
                nonetypeCounter = nonetypeCounter + 1;
                return await self._send_suggested_actions2(turn_context)
            elif nonetypeCounter == 1:
                nonetypeCounter = nonetypeCounter + 1;
                return await self._send_suggested_actions3(turn_context)
            elif nonetypeCounter == 2:
                nonetypeCounter = nonetypeCounter + 1;
                return await self._send_suggested_actions4(turn_context)
            elif nonetypeCounter == 3:
                nonetypeCounter = nonetypeCounter + 1;
                return await self._send_suggested_actions5(turn_context) 
            elif nonetypeCounter == 4:
                nonetypeCounter = nonetypeCounter + 1;
                return await self._send_suggested_actions6(turn_context)
            elif nonetypeCounter == 5:
                nonetypeCounter = nonetypeCounter + 1;
                userResponseDataBase.write("Do you often spend time exploring unrealistic yet intriguing ideas?\n")
                
                return await self._send_suggested_actions7(turn_context) 
            elif nonetypeCounter == 6:
                nonetypeCounter = nonetypeCounter + 1;
                userResponseDataBase.write("Do you enjoy social gatherings?\n")
                return await self._send_suggested_actions10(turn_context)
            elif nonetypeCounter == 7:
                nonetypeCounter = nonetypeCounter + 1;
                id = uuid.uuid4();
                
                userResponseCSV.insert(1, id, userAnswers, allow_duplicates = True)
                userResponseCSV.to_csv("UserResponse.csv", index = False)

                df = pd.read_csv("UserResponse.csv")

                X1 = pd.read_excel("trained_data_final.xlsx")
                df = df.T
                df.reset_index(drop=True,inplace=True)
                df.rename(columns=df.iloc[0], inplace = True)
                df = df.iloc[1: , :]
                df = df.iloc[0:1,:]
                df
                df.rename(columns={'Please mention your current work experience before you begin pursuing MBA? ':'experience','Which of the following options are the most valueable to you when considering future goals? ':'future_goals',
                                  'What is your current functional area? ':'functional_area','What are your expected/desired earning goals (in USD)/annum after completing your MBA? ':'earning_goals','Which working style do you like the most? ':'working_style',
                                  'What is your strength? ':'strength','Do you often spendtime exploring unrealistic yet intriguing ideas? ':'ideas',
                                  'Do you have careful and methodical approach to life? ':'approach','What do you like to do outside of your work? ':'outside_of_work',
                                  'Do you enjoy social gatherings? ':'gatherings','Which was your favorite subject in school? ':'fav_sub'},inplace=True)
                df
                df = df.assign(future_goals=df['future_goals'].str.split(',')).explode('future_goals')
                df = df.assign(strength=df['strength'].str.split(',')).explode('strength')
                df.reset_index(drop=True,inplace=True)
                feature_cols = df.columns
                encoder = OneHotEncoder(handle_unknown='ignore')
                X_test_encoded = pd.DataFrame(encoder.fit_transform(df[feature_cols]).toarray())
                X_test_encoded.columns=encoder.get_feature_names(feature_cols)
                df.drop(feature_cols,axis=1,inplace=True)
                df = pd.concat([df,X_test_encoded],axis=1)
                df
                for column in X1.columns:
                    if column not in df.columns:
                        df[column]=0
                for column in df.columns:
                    if column not in X1.columns:
                        df.drop([column], axis=1,inplace=True)



                pkl_filename = "v.1_3_8_2021_trainedModelFinal.pkl"

                with open(pkl_filename,'rb') as file:
                    pickle_model=pickle.load(file)



                pickle_model.best_estimator_.predict(df)
                pred_prob = np.round(pickle_model.best_estimator_.predict_proba(df),3)
                pred_prob

                pred_prob1 = pd.DataFrame(pred_prob)
                pred_prob1 = df.join(pd.DataFrame(pred_prob))
                d_t = pred_prob1.iloc[:,-16:]
                pred_prob1['stream'] = np.argmax(d_t.values,axis=1)
                pred_prob1['pred_prob'] = pred_prob.max(axis=1)

                pred_prob1['Spec_stream'] = np.where(pred_prob1['stream']==0, 'Business Analytics',
                                                     np.where(pred_prob1['stream']==1, 'Entrepreneurship',
                                                              np.where(pred_prob1['stream']==2, 'Finance',
                                                                    np.where(pred_prob1['stream']==3, 'General management',
                                                                             np.where(pred_prob1['stream']==4, 'Health Care',
                                                                                      np.where(pred_prob1['stream']==5, 'Human Resources',
                                                                                               np.where(pred_prob1['stream']==6, 'Information Technology',
                                                                                                        np.where(pred_prob1['stream']==7, 'International Business',
                                                                                                                 np.where(pred_prob1['stream']==8, 'International Marketing',
                                                                                                                          np.where(pred_prob1['stream']==9,'Marketing',
                                                                                                                                   np.where(pred_prob1['stream']==10,'Operations',
                                                                                                                                            np.where(pred_prob1['stream']==11,'Production & Operations Management',
                                                                                                                                                    np.where(pred_prob1['stream']==12,'Rural Management',
                                                                                                                                                             np.where(pred_prob1['stream']==13,'Senior Managemen',
                                                                                                                                                                      np.where(pred_prob1['stream']==14,'SMP',
                                                                                                                                                                               np.where(pred_prob1['stream']==15,'Strategy Management','NAN'))))))))))))))))
                                                                                                              
                pred_prob1.drop(columns=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],inplace=True,axis=1)
                Specialization_Stream  = pred_prob1['Spec_stream'][pred_prob1.pred_prob == pred_prob1.pred_prob.max()]
                Specialization_Stream.reset_index(drop=True,inplace=True)

                print(Specialization_Stream[0])
                recommendationString = Specialization_Stream[0]
                #print(pickle_model.best_estimator_.predict(df1))
                
                return await self._send_response12(turn_context)                                                     
            else:            
            
                await turn_context.send_activity(
                        MessageFactory.text(
                                
                            f"Please choose a valid option"
                                
                        )
                    )
        else:

            text = turn_context.activity.text.lower();

            
            print(turn_context.activity.text)
            
            #print(phoneNumberCounter)
            if text != '' and all(chr.isalpha() or chr.isspace() for chr in text) and phoneNumberCounter == 0 and counterName == 0:
                
                counterName = 1;

                userResponseDataBase.write(turn_context.activity.text)
                userResponseDataBase.write("\n")   
                
                #userResponseCSV.insert(1,"Answers",turn_context.activity.text)
                userAnswers[0] = turn_context.activity.text
                #userResponseCSV[“Answers”].iloc[1:2]
                
                return await self._send_suggested_actions_Contact_Details(turn_context)

               
                 
            
            elif( text.isalpha() == False or text.isspace() == False) and counterName == 0:
                await turn_context.send_activity(
                        MessageFactory.text(
                            
                            f"Please enter only alphabets and spaces while entering name"
                            
                        )
                    )    
            elif contactDetailsCounter == 0:
                contactDetailsCounter = contactDetailsCounter + 1;

                counterName = 1;
               
                if turn_context.activity.text == "Yes":


                    await turn_context.send_activity(
                            MessageFactory.text(
                                
                                f"Please enter your email address"
                                
                            )
                    )
                
                else:
                    emailCounter = emailCounter + 1;
                    return await self._send_suggested_actions(turn_context)


            
            elif validate_email(text):
                userResponseDataBase.write("Email:")
                userResponseDataBase.write(turn_context.activity.text)
                userResponseDataBase.write("\n")
                userAnswers[1] = turn_context.activity.text
                phoneNumberCounter = phoneNumberCounter + 1;
                userResponseDataBase.write("Phone Number:")
                emailCounter = emailCounter + 1;
                await turn_context.send_activity(
                        MessageFactory.text(
                            
                            f"Please enter phone number with country code like +91 9988776655"
                                
                        )
                    )
                         
            elif validate_email(text) == False and phoneNumberCounter == 0 and emailCounter == 0:
                #contactDetailsCounter = contactDetailsCounter + 1;
                
                await turn_context.send_activity(
                        MessageFactory.text(
                            
                            f"Please enter valid email address"
                                
                        )
                    )
            elif (text.startswith("0") or text.startswith("+")) and len(text) >=3 and phoneNumberCounter == 1:
                """
                my_number = phonenumbers.parse(text)
                if phonenumbers.is_valid_number(my_number):
                    return await self._send_suggested_actions(turn_context)
                else:
                    await turn_context.send_activity(
                        MessageFactory.text(
                            
                            f"Please enter a valid phone number"
                            
                        )
                    )
                """
                try:
                    if carrier._is_mobile(number_type(phonenumbers.parse(text))):
                        userResponseDataBase.write(turn_context.activity.text)
                        userResponseDataBase.write("\n")
                        userAnswers[2] = turn_context.activity.text
                        return await self._send_suggested_actions(turn_context)
                    else:
                        await turn_context.send_activity(
                            MessageFactory.text(
                                
                                f"Please enter a valid phone number"
                                
                            )
                        )
                except:
                    await turn_context.send_activity(
                            MessageFactory.text(
                                
                                f"Please enter a valid phone number"
                                
                            )
                        )
            #elif turn_context.activity.text == "< 2 years" or turn_context.activity.text == "> 2-4 years" or turn_context.activity.text == "> 4-6 years" or turn_context.activity.text == "> 6-10 years" or turn_context.activity.text == "> 10-15 years" or turn_context.activity.text == "> 15-20 years" or turn_context.activity.text == "> 20 years":
                #return await self._send_suggested_actions2(turn_context)
            #elif turn_context.activity.text == "Get a better job" or turn_context.activity.text == "Become an expert in the field so that market approaches me rather than I searching for a job" or turn_context.activity.text == "Start my own business" or turn_context.activity.text == "Continue with family business" or turn_context.activity.text == "My interest" or turn_context.activity.text == "Market trend" or turn_context.activity.text == "Wider range of career options" or turn_context.activity.text == "High earnings":
                #return await self._send_suggested_actions3(turn_context)
            #elif turn_context.activity.text == "Operations" or turn_context.activity.text == "Business Head" or turn_context.activity.text == "Human Resource" or turn_context.activity.text == "Information Technology" or turn_context.activity.text == "Marketing" or turn_context.activity.text == "Finance":
                #return await self._send_suggested_actions4(turn_context)
            #elif turn_context.activity.text == "> $80,000" or turn_context.activity.text == "$51,000 - $ 80,000" or turn_context.activity.text == "$21,000-$50,000" or turn_context.activity.text == "$11,000-$20,000" or turn_context.activity.text == "< $10,000":
                #return await self._send_suggested_actions5(turn_context)
            #elif turn_context.activity.text == "I don't mind working with people, but I like working alone" or turn_context.activity.text == "I like working in a team" or turn_context.activity.text == "I like leading people":
                #return await self._send_suggested_actions6(turn_context)    
            #elif turn_context.activity.text == "I like giving presentations" or turn_context.activity.text == "I like qualitative work more than the quantitative one" or turn_context.activity.text == "I am good at managing data and information" or turn_context.activity.text == "I have an eye for detail":
                #return await self._send_suggested_actions7(turn_context) 
            elif turn_context.activity.text == "Yes" or turn_context.activity.text == "No" or turn_context.activity.text == "Sometimes" or turn_context.activity.text == "Not sure":
                userResponseDataBase.write(turn_context.activity.text)
                userResponseDataBase.write("\n")

                if excelCounter == 0:
                    userAnswers[9] = turn_context.activity.text
                    excelCounter = excelCounter + 1
                elif excelCounter == 1:
                    userAnswers[10] = turn_context.activity.text
                    excelCounter = excelCounter + 1
                elif excelCounter == 2:
                     userAnswers[12] = turn_context.activity.text
                     excelCounter = excelCounter + 1
                else:
                    print("An error occured in writing to csv file")

                global counter
                
                if counter == 0 and ideas == False and approach == False and socialGatherings == False:
                    
                    counter = 1;
                    userResponseDataBase.write("Do you have careful and methodical approach to life?\n")
                    userAnswers[10] = turn_context.activity.text
                    return await self._send_suggested_actions8(turn_context)
                elif counter == 1 and ideas == False and approach == False and socialGatherings == False:
                    counter = 2
                    #userResponseDataBase.write("What do you like to do outside of your work?\n")
                    return await self._send_suggested_actions9(turn_context)
                elif counter == 2 and ideas == False and approach == False and socialGatherings == False:
                    #userResponseDataBase.write("And which subject did you like the most in school?\n")
                    return await self._send_suggested_actions11(turn_context)
                else:
                    await turn_context.send_activity(
                            MessageFactory.text(
                                
                                f"The options choice had a clash"
                                
                            )
                        )
            elif turn_context.activity.text == "I go to the gym" or turn_context.activity.text == "I like doing volunteer work" or turn_context.activity.text == "I like doing household work and home improvement" or turn_context.activity.text == "I like learning, practicing and creating art forms, music, designing etc.":
                userResponseDataBase.write("Do you enjoy social gatherings?")
                return await self._send_suggested_actions10(turn_context)  
            elif turn_context.activity.text == "Social science" or turn_context.activity.text == "Language" or turn_context.activity.text == "Science" or turn_context.activity.text == "Maths":
                #userResponseCSV.insert(1, "Answer", userAnswers)
                userResponseDataBase.close()
                userResponseCSV.to_csv("UserResponse.csv", index = False)

                
                return await self._send_response12(turn_context)
            else:
                
                
                await turn_context.send_activity(
                        MessageFactory.text(
                                
                            f"Please choose one of the valid options"
                                
                        )
                    )




        #return await turn_context.send_activity(MessageFactory.text(f"i am here"))
        
        

    async def _send_welcome_message(self, turn_context: TurnContext):
        userResponseDataBase.write("Name:")
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    MessageFactory.text(
                        
                        f"Hi User, welcome to SSfinderbot."
                        f" My aim is to help you in your MBA journey."
                        f" Please enter your name"
                        
                    )
                )

                

    
    

    async def _send_suggested_actions_Contact_Details(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        
        replyConact = MessageFactory.text("Would you like to share your contact details?")
        

        replyConact.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Yes",
                    type=ActionTypes.im_back,
                    value="Yes",
                ),
                CardAction(
                    title="No",
                    type=ActionTypes.im_back,
                    value="No",
                    
                ),
            ]
        )

        return await turn_context.send_activity(replyConact)   
        

    async def _send_suggested_actions(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        reply = MessageFactory.text("Please mention your current work experience before pursuing MBA")
        reply2 = MessageFactory.text("Test")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="< 2 years",
                    type=ActionTypes.im_back,
                    value="< 2 years",
                    choice="choice 1",
                    image="https://via.placeholder.com/20/FF0000?text=R",
                    image_alt_text="R",
                ),
                CardAction(
                    title="> 2-4 years",
                    type=ActionTypes.im_back,
                    value="> 2-4 years",
                    image="https://via.placeholder.com/20/FFFF00?text=Y",
                    image_alt_text="Y",
                ),
                CardAction(
                    title="> 4-6 years",
                    type=ActionTypes.im_back,
                    value="> 4-6 years",
                    image="https://via.placeholder.com/20/0000FF?text=B",
                    image_alt_text="B",
                ),
                CardAction(
                    title="> 6-10 years",
                    type=ActionTypes.im_back,
                    value="> 6-10 years",
                    image="https://via.placeholder.com/20/0000FF?text=B",
                    image_alt_text="B",
                ),
                CardAction(
                    title="> 10-15 years",
                    type=ActionTypes.im_back,
                    value="> 10-15 years",
                    image="https://via.placeholder.com/20/0000FF?text=B",
                    image_alt_text="B",
                ),
                CardAction(
                    title="> 15-20 years",
                    type=ActionTypes.im_back,
                    value="> 15-20 yearss",
                    image="https://via.placeholder.com/20/0000FF?text=B",
                    image_alt_text="B",
                ),
                CardAction(
                    title="> 20 years",
                    type=ActionTypes.im_back,
                    value="> 20 years",
                    image="https://via.placeholder.com/20/0000FF?text=B",
                    image_alt_text="B",
                ),
            ]
        )

        return await turn_context.send_activity(reply)
        """
        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment()],
        )

        return await turn_context.send_activity(message)
        

    
    async def _send_suggested_actions2(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply2 = MessageFactory.text("Which of the options are the most valuable to you when considering future goals?")

        reply2.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Get a better job",
                    type=ActionTypes.im_back,
                    value="Get a better job",
                    
                ),
                CardAction(
                    title="Become an expert in the field so that market approaches me rather than I searching for a job",
                    type=ActionTypes.im_back,
                    value="Become an expert in the field so that market approaches me rather than I searching for a job",
                    
                ),
                CardAction(
                    title="Start my own business",
                    type=ActionTypes.im_back,
                    value="Start my own business",
                    
                ),
                CardAction(
                    title="Continue with family business",
                    type=ActionTypes.im_back,
                    value="Continue with family business",
                    
                ),
                CardAction(
                    title="My interest",
                    type=ActionTypes.im_back,
                    value="My interest",
                    
                ),
                CardAction(
                    title="Market trend",
                    type=ActionTypes.im_back,
                    value="Market trend",
                    
                ),
                CardAction(
                    title="Wider range of career options",
                    type=ActionTypes.im_back,
                    value="Wider range of career options",
                    
                ),
                CardAction(
                    title="High earnings",
                    type=ActionTypes.im_back,
                    value="High earnings",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply2)

        """
        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment2()],
        )


        return await turn_context.send_activity(message)


    async def _send_suggested_actions3(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply3 = MessageFactory.text("What is your current functional area?")

        reply3.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Operations",
                    type=ActionTypes.im_back,
                    value="Operations",
                ),
                CardAction(
                    title="Business Head",
                    type=ActionTypes.im_back,
                    value="Business Head",
                    
                ),
                CardAction(
                    title="Human Resource",
                    type=ActionTypes.im_back,
                    value="Human Resource",
                    
                ),
                CardAction(
                    title="Information Technology",
                    type=ActionTypes.im_back,
                    value="Information Technology",
                    
                ),
                CardAction(
                    title="Marketing",
                    type=ActionTypes.im_back,
                    value="Marketing",
                    
                ),
                CardAction(
                    title="Finance",
                    type=ActionTypes.im_back,
                    value="Finance",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply3)
        """
        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment3()],
        )

        return await turn_context.send_activity(message)

    async def _send_suggested_actions4(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply4 = MessageFactory.text("What are your expected/desired earning goals (in USD)/annum after completing your MBA?")

        reply4.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="> $80,000",
                    type=ActionTypes.im_back,
                    value="Operations",
                ),
                CardAction(
                    title="$51,000 - $ 80,000",
                    type=ActionTypes.im_back,
                    value="$51,000 - $ 80,000",
                    
                ),
                CardAction(
                    title="$21,000-$50,000",
                    type=ActionTypes.im_back,
                    value="$21,000-$50,000",
                    
                ),
                CardAction(
                    title="$11,000-$20,000",
                    type=ActionTypes.im_back,
                    value="$11,000-$20,000",
                    
                ),
                CardAction(
                    title="< $10,000",
                    type=ActionTypes.im_back,
                    value="< $10,000",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply4)

        """
        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment4()],
        )

        return await turn_context.send_activity(message)
    

    async def _send_suggested_actions5(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply5 = MessageFactory.text("Which working style do you like the most?")

        reply5.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="I don't mind working with people, but I like working alone",
                    type=ActionTypes.im_back,
                    value="I don't mind working with people, but I like working alone",
                ),
                CardAction(
                    title="I like working in a team",
                    type=ActionTypes.im_back,
                    value="I like working in a team",
                    
                ),
                CardAction(
                    title="I like leading people",
                    type=ActionTypes.im_back,
                    value="I like leading people",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply5)
        """
        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment5()],
        )

        return await turn_context.send_activity(message)


    async def _send_suggested_actions6(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply6 = MessageFactory.text("What is your strength?")


        reply6.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="I like giving presentations",
                    type=ActionTypes.im_back,
                    value="I like giving presentations",
                ),
                CardAction(
                    title="I like qualitative work more than the quantitative one",
                    type=ActionTypes.im_back,
                    value="I like qualitative work more than the quantitative one",
                    
                ),
                CardAction(
                    title="I am good at managing data and information",
                    type=ActionTypes.im_back,
                    value="I am good at managing data and information",
                    
                ),
                CardAction(
                    title="I have an eye for detail",
                    type=ActionTypes.im_back,
                    value="I have an eye for detail",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply6)
        """

        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment6()],
        )

        return await turn_context.send_activity(message)

    async def _send_suggested_actions7(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        
        reply7 = MessageFactory.text("Do you often find yourself spending time in exploring unrealistic yet intriguing ideas?")
        ideas = True;
        print(ideas)

        reply7.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Yes",
                    type=ActionTypes.im_back,
                    value="Yes",
                ),
                CardAction(
                    title="No",
                    type=ActionTypes.im_back,
                    value="No",
                    
                ),
                CardAction(
                    title="Sometimes",
                    type=ActionTypes.im_back,
                    value="Sometimes",
                    
                ),
                CardAction(
                    title="Not sure",
                    type=ActionTypes.im_back,
                    value="Not sure",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply7)


    async def _send_suggested_actions8(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        
        reply8 = MessageFactory.text("And would you say that you have a careful and methodical approach to life?")
        approach = True;

        reply8.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Yes",
                    type=ActionTypes.im_back,
                    value="Yes",
                ),
                CardAction(
                    title="No",
                    type=ActionTypes.im_back,
                    value="No",
                    
                ),
                CardAction(
                    title="Sometimes",
                    type=ActionTypes.im_back,
                    value="Sometimes",
                    
                ),
                CardAction(
                    title="Not sure",
                    type=ActionTypes.im_back,
                    value="Not sure",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply8)

    async def _send_suggested_actions9(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply9 = MessageFactory.text("What do you like to do outside of work?")

        reply9.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="I go to the gym",
                    type=ActionTypes.im_back,
                    value="I go to the gym",
                ),
                CardAction(
                    title="I like doing volunteer work",
                    type=ActionTypes.im_back,
                    value="I like doing volunteer work",
                    
                ),
                CardAction(
                    title="I like doing household work and home improvement",
                    type=ActionTypes.im_back,
                    value="I like doing household work and home improvement",
                    
                ),
                CardAction(
                    title="I like learning, practicing and creating art forms, music, designing etc.",
                    type=ActionTypes.im_back,
                    value="I like learning, practicing and creating art forms, music, designing etc.",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply9)

        """

        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment7()],
        )

        return await turn_context.send_activity(message)

    async def _send_suggested_actions10(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        
        reply10 = MessageFactory.text("Do you enjoy social gatherings?")
        socialGatherings = True;

        reply10.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Yes",
                    type=ActionTypes.im_back,
                    value="Yes",
                ),
                CardAction(
                    title="No",
                    type=ActionTypes.im_back,
                    value="No",
                    
                ),
                CardAction(
                    title="Sometimes",
                    type=ActionTypes.im_back,
                    value="Sometimes",
                    
                ),
                CardAction(
                    title="Not sure",
                    type=ActionTypes.im_back,
                    value="Not sure",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply10)

    async def _send_suggested_actions11(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        

        
        reply11 = MessageFactory.text("Which was your favorite subject in school?")

        reply11.suggested_actions = SuggestedActions(
            actions=[
                CardAction(
                    title="Social science",
                    type=ActionTypes.im_back,
                    value="Social science",
                ),
                CardAction(
                    title="Language",
                    type=ActionTypes.im_back,
                    value="Language",
                    
                ),
                CardAction(
                    title="Science",
                    type=ActionTypes.im_back,
                    value="Science",
                    
                ),
                CardAction(
                    title="Maths",
                    type=ActionTypes.im_back,
                    value="Maths",
                    
                ),
            ]
        )

        return await turn_context.send_activity(reply11)

        """

        message = Activity(
            
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment8()],
        )

        return await turn_context.send_activity(message)


    async def _send_response12(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        
        reply12 = MessageFactory.text("Based on our assessment, the ideal MBA specialization stream for you is " + recommendationString)
        return await turn_context.send_activity(reply12)




    async def _send_response13(self, turn_context: TurnContext):
        message = Activity(
            text="Please mention your current work experience before pursuing MBA:",
            type=ActivityTypes.message,
            attachments=[self._create_adaptive_card_attachment()],
        )

        return await turn_context.send_activity(message)

    def _create_adaptive_card_attachment(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[0])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)

    def _create_adaptive_card_attachment2(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[1])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)    
    
    def _create_adaptive_card_attachment3(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[2])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)    

    def _create_adaptive_card_attachment4(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[3])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)    

    def _create_adaptive_card_attachment5(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[4])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)    

    def _create_adaptive_card_attachment6(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[5])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)

    def _create_adaptive_card_attachment7(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[6])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data)    

    def _create_adaptive_card_attachment8(self) -> Attachment:
        """
        Load a random adaptive card attachment from file.
        :return:
        """
        
        card_path = os.path.join(os.getcwd(), CARDS[7])
        with open(card_path, "rb") as in_file:
            card_data = json.load(in_file)

        return CardFactory.adaptive_card(card_data) 


    def _DataBaseAdder(self, str, inputCounter):

        inputCollection = str.split(",")
        

        if inputCounter == 0:
            userInput = ""
            userResponseDataBase.write("Please mention your current work experience before pursuing MBA\n")
            
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                if i >= 1:
                    userInput += "," + card1Inputs[index - 1 ] 
                else:
                    userInput += card1Inputs[index - 1 ] 
                #print(card1Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[3] = userInput
        elif inputCounter == 1:
            userInput = ""
            userResponseDataBase.write("Which of the options are the most valuable to you when considering future goals?\n")
            
            for i in range(len(inputCollection)):

                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card2Inputs[index - 1 ]
                else:
                    userInput += card2Inputs[index - 1 ] 
                #print(card2Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[4] = userInput

        elif inputCounter == 2:
            userInput = ""
            userResponseDataBase.write("What is your Current Functional Area?\n")
           
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card3Inputs[index - 1 ]
                else:
                    userInput += card3Inputs[index - 1 ] 
                #print(card3Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[5] = userInput

        elif inputCounter == 3:
            userInput = ""
            userResponseDataBase.write("What are your expected/desired earning goals (in USD)/annum after completing your MBA?\n")
            
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card4Inputs[index - 1 ]
                else:
                    userInput += card4Inputs[index - 1 ] 
                #print(card4Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[6] = userInput

        elif inputCounter == 4:
            userInput = ""
            userResponseDataBase.write("Which working style do you like the most?\n")
            
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card5Inputs[index - 1 ]
                else:
                    userInput += card5Inputs[index - 1 ] 
                #print(card5Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[7] = userInput

        elif inputCounter == 5:
            userInput = ""
            userResponseDataBase.write("What is your strength?\n")
            
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card6Inputs[index - 1 ]
                else:
                    userInput += card6Inputs[index - 1 ] 
                #print(card6Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[8] = userInput


        elif inputCounter == 6:
            userInput = ""
            userResponseDataBase.write("What do you like to do outside of your work?\n")
            
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card7Inputs[index - 1 ]
                else:
                    userInput += card7Inputs[index - 1 ] 
                #print(card7Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[11] = userInput

        elif inputCounter == 7:
            userInput = ""
            userResponseDataBase.write("Which was your favorite subject in school?\n")
            for i in range(len(inputCollection)):
                print(int(inputCollection[i]))
                index = int(inputCollection[i])
                
                if i >= 1:
                    userInput += "," + card8Inputs[index - 1 ]
                else:
                    userInput += card8Inputs[index - 1 ] 
                #print(card8Inputs[index - 1 ])
            print(userInput)
            userResponseDataBase.write(userInput)
            userResponseDataBase.write("\n")
            userAnswers[13] = userInput


        else:
            print("User chose an invalid option")
            userResponseDataBase.write("User chose an invalid option")
            userResponseDataBase.write("\n")



             