# import google.generativeai as genai


# def get_compnay_details(compnay_name):
#   genai.configure(api_key="YOUR_API_KEY")

# # Set up the model
#   generation_config = {
#     "temperature": 0.9,
#     "top_p": 1,
#     "top_k": 1,
#     "max_output_tokens": 2048,
#   }
#   model = genai.GenerativeModel(model_name="gemini-pro",
#                                 generation_config=generation_config)
#   json_formate = {
#       "what":"description of what commpnay do",
#       "impact":"description of what impact is in general of there work to environment and climate",
#       "future_impact":"what can be there future impact on environment and climate"
#   }
#   prompt_parts = [
#     f"""extract compnay details given ticker {compnay_name} which include what they do , what impact on enviroment, what can be future impact on climate change
#     provide result in json formate and no extra text
#     ###JSON FORMATE IS###
#     {str(json_formate)}
#     """,
#   ]
#   response = model.generate_content(prompt_parts)
#   output = response.text
#   print(response.text)
#   # output = json.loads(response.text)
#   # print(output['what'])
#   # output = json.loads(response.text)
#   with open(f"about_{compnay_name}.json","w") as f:
#     f.write(response.text)
#   return output

# # get_compnay_details("apple")