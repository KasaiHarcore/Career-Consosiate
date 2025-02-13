from model import claude, common, gpt, groq, openrouter

def register_all_models() -> None:
    """
    Register all models. This is called in main.
    """
    # API models
    common.register_model(gpt.Gpt4_Turbo20240409())
    common.register_model(gpt.Gpt4_0125Preview())
    common.register_model(gpt.Gpt4_1106Preview())
    common.register_model(gpt.Gpt35_Turbo0125())
    common.register_model(gpt.Gpt35_Turbo1106())
    common.register_model(gpt.Gpt35_Turbo16k_0613())
    common.register_model(gpt.Gpt35_Turbo0613())
    common.register_model(gpt.Gpt4_0613())
    common.register_model(gpt.Gpt4_O())

    common.register_model(claude.Claude3Opus())
    common.register_model(claude.Claude3Sonnet())
    common.register_model(claude.Claude3Haiku())
    common.register_model(claude.Claude2_1())
    common.register_model(claude.Claude2_0())
    common.register_model(claude.Claude_Instant())
    
    common.register_model(groq.Llama3_8B())
    common.register_model(groq.Llama3_70B())
    common.register_model(groq.Mixtral_8x7B())
    common.register_model(groq.Gemma_7B())
    common.register_model(groq.Llama_31_70B())
    common.register_model(groq.Llama_31_8B_8192())
    
    common.register_model(openrouter.GPT4())
    common.register_model(openrouter.Llama31_405B_Instruct())
    common.register_model(openrouter.Llama31_70B_Instruct())
    common.register_model(openrouter.Qwen2_7B_Instruct())
    common.register_model(openrouter.Gemma2_9B())
    common.register_model(openrouter.DeepSeek_R1())
    common.register_model(openrouter.OpenAI_O3_Mini())

    # register default model as selected
    common.SELECTED_MODEL = gpt.Gpt35_Turbo0125()
