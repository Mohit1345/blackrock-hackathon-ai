# Reference - About compnay - What they do , what impact they make in environment, what future impact they can have as we are moving towards more sustainable development

# Risk assestment based sorting

###ESG direct scores [-3,+3] (20%)

###Realtime Social Score (30%)
# ----employee feedbacks (+1,0,-1)
# ----clients rating (+1,0,-1)
# ----Political and Geopoligical impact of company (+1,0,-1)
# ----commpany news sentiments (+1,0,-1)
# ----Company announcement specific to care of environment, climate change (compnay policies)

# ----Profitable (predict.py) (+1,-1) (10%)

# Compnay Fundamentals
#  ----Patrioski [0,9] (40%)

# final_scoring = [-8,17]

# equation 

# news, google trends

# 10 compnaies (sort in descreasing order -> Min risk)
import pandas as pd 
from openai_f import get_compnay_details, scoring
from realtime  import get_realtime_info
from predict import get_pf
from pitroski import get_patrioski
import json
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def calculate_final_score(ESG, E, C, P, N, Pr, F):
    # Define the weights
    W_ESG = 0.2
    W_SS = 0.3
    W_Pr = 0.1
    W_F = 0.4
    
    # Calculate the contributions
    ESG_contribution = W_ESG * ESG
    
    # Calculate the average of the social scores
    social_score = (E + C + P + N) / 4
    social_score_contribution = W_SS * social_score
    
    # Profitable score contribution
    profitable_contribution = W_Pr * Pr
    
    # Fundamentals contribution
    fundamentals_contribution = W_F * (F / 9) * 6
    
    # Calculate the final score
    final_score = ESG_contribution + social_score_contribution + profitable_contribution + fundamentals_contribution
    
    return final_score

esg_data = pd.read_csv("esg.csv")
# companies = ['AAPL',"TSLA",'DIS',"ABNB","ADBE","META","NVDA","JPM","KO","DPZ"]
companies = ['TSLA']
complete_data = []
level_map = {
    "High":3,
    "Medium":2,
    "Low":1
}
import json
import os

company_map = {
    'AAPL':"Apple",
    "TSLA":"Tesla",
    "DIS":"Walt Disney Co",
    "ANBN":"Airbnb",
    "ADBE":"Adobe",
    "META":"Meta",
    "NVDA":"Nvidia",
    "JPM":"JP Morgan and Chase Co.",
    "KO":"Coca-cola",
    "DPZ":"Dominos"
}


def get_recommendation(companies):
    final_mappings = []
    complete_datas = []

    for company in companies:
        if os.path.exists(f"company_data_{company}.json"):
            data = read_json_file(f"company_data_{company}.json")
            complete_datas.append(data)
            continue
        company_data = {}
        company_data['stock'] = company
        company_data['company_name'] = company_map[company]
        company_data['about_company'] = get_compnay_details(company)
        # Initialize the 'esg_scores' dictionary
        company_data['esg_scores'] = {}

        print(type(level_map[esg_data[esg_data['ticker'] == company.lower()]['total_level'].iloc[0]]))
        print(type(esg_data[esg_data['ticker'] == company.lower()]['total_score'].iloc[0]))

        # Extraction of ESG Values from recorded data
        company_data['esg_scores']['environment_level'] = level_map[esg_data[esg_data['ticker'] == company.lower()]['environment_level'].iloc[0]]
        company_data['esg_scores']['social_level'] = level_map[esg_data[esg_data['ticker'] == company.lower()]['social_level'].iloc[0]]
        company_data['esg_scores']['governance_level'] = level_map[esg_data[esg_data['ticker'] == company.lower()]['governance_level'].iloc[0]]
        company_data['esg_scores']['total_level'] = level_map[esg_data[esg_data['ticker'] == company.lower()]['total_level'].iloc[0]]
        company_data['esg_scores']['total_esg_score'] = int(esg_data[esg_data['ticker'] == company.lower()]['total_score'].iloc[0])

        ESG = company_data['esg_scores']['environment_level'] + company_data['esg_scores']['social_level'] + company_data['esg_scores']['governance_level']

        company_data['real_time_info'] = get_realtime_info(company)
        company_data['real_time_scores'] = scoring(company, company_data['real_time_info'])
        print(company_data['real_time_scores'])
        E = company_data['real_time_scores'][0]['score']
        C = company_data['real_time_scores'][1]['score']
        P = company_data['real_time_scores'][2]['score']
        N = company_data['real_time_scores'][3]['score']

        company_data['pitroski'] = get_patrioski(company)
        F = company_data['pitroski']

        Pr = get_pf(company)
        final_score = calculate_final_score(ESG, E, C, P, N, Pr, F)
        final_mappings.append({company: final_score})
        print(final_mappings)
        company_data['final_score'] = final_score

        with open(f"company_data_{company}.json", "w") as file:
            json.dump(company_data, file, indent=4)
        complete_datas.append(company_data)
    sorted_data = sorted(complete_datas, key=lambda x: x['final_score'])
    return sorted_data

# get_recommendation(companies)