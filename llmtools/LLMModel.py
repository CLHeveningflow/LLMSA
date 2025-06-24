import json

def get_model_info(provider_name):
    with open('llm.json', 'r') as file:
        llm_data = json.load(file)

    provider_info = llm_data.get(provider_name)
    if provider_info:
        model = provider_info.get("model")
        api_base = provider_info.get("api_base")
        api_key = provider_info.get("api_key")
        return {
            "model": model,
            "api_base": api_base,
            "api_key": api_key
        }
    else:
        return None
    
def get_openai_model_info(provider_name):
    with open('llm.json', 'r') as file:
        llm_data = json.load(file)

    provider_info = llm_data.get(provider_name)
    if provider_info:
        model = provider_info.get("model")
        api_base = provider_info.get("api_base")
        api_key = provider_info.get("api_key")
        return {
            "model": model,
            "openai_api_base": api_base,
            "openai_api_key": api_key
        }
    else:
        return None