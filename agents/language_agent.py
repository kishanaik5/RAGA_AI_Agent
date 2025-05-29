# agents/language_agent.py

from llama_cpp import Llama
import os

# Update this path to your actual model location if needed
model_path = os.getenv(
    "LLM_PATH",
    r"C:\Users\kisha\.lmstudio\models\lmstudio-community\DeepSeek-R1-Distill-Qwen-7B-GGUF\DeepSeek-R1-Distill-Qwen-7B-Q4_K_M.gguf"
)
llm = Llama(model_path=model_path, n_ctx=1024)

def format_prompt(exposure_pct, earnings_surprises, regional_sentiment):
    earnings_lines = []
    for ticker, surprise in earnings_surprises.items():
        verdict = "beat estimates" if surprise >= 0 else "missed estimates"
        earnings_lines.append(f"{ticker} {verdict} by {abs(surprise)}%.")

    earnings_summary = " ".join(earnings_lines)
    
    prompt = (
        f"Today, your Asia tech allocation is {exposure_pct}% of AUM. "
        f"{earnings_summary} Regional sentiment is {regional_sentiment}."
        " Return this as a spoken market brief in under 50 words."
    )
    return prompt


def generate_brief(exposure_pct, earnings_surprises, regional_sentiment="neutral with a cautionary tilt"):
    prompt = format_prompt(exposure_pct, earnings_surprises, regional_sentiment)

    try:
        output = llm(
            prompt,
            max_tokens=100,
            temperature=0.7,
            stop=["\n"]
        )
        # llama-cpp-python returns a dict with 'choices'
        return output["choices"][0]["text"].strip()
    except Exception as e:
        return f"Error generating brief: {e}"


if __name__ == "__main__":
    # Sample data
    sample_exposure = 22
    sample_earnings = {
        "TSMC": 4,
        "Samsung": -2
    }

    brief = generate_brief(sample_exposure, sample_earnings)
    print("Generated Market Brief:\n", brief)
