#
# Cascade Optimizer LLM 
# 14/09/2024
#
# Newtech Intelligence

import openai

import subprocess
import os
from pathlib import Path



def generate_text(prompt : str):
    """
    Prompt must be in the format
    "Average, [(date, estimated_time / real_time), ...]"
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  #tgi
            messages=[
                {"role": "system", "content": """
                Generate small reports that include if a specific employee is achieving his quota. 
                The small text report should make a brief description of his performance.
                The input will be in the format: "Average, [(date, estimated_time / real_time), ...]".
                Do not include ANY metadata on the text, just the text report.
                Average > 1 implies over quota, Average < 1 implies under quota, and Average close to 1 implies on quota. Average == 1 is the expected quota always. 
                If the way workload should change is not clear, specify so."""},
                
                {"role": "user", "content": prompt}
            ], # The report must be accurate and specific. DO NOT use words like 'consider' or 'recommend', be direct and specific, instead say: increase work, decrease work, mantain work.
            max_tokens=1500,  
            temperature=0.2,  
        )
        return response['choices'][0]['message']['content'].strip()
    except:
        return "Server connection error. AI analysis could not be executed"

