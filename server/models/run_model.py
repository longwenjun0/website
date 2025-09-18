import sys
import json
import os
from openai import AzureOpenAI

def main():
    endpoint = os.getenv("END_POINT")
    subscription_key = os.getenv("API_KEY")
    api_version = "2024-12-01-preview"

    if len(sys.argv) < 3:
        print("Usage: python run_model.py <model> <question>", flush=True)
        sys.exit(1)

    model = sys.argv[1]
    question = sys.argv[2]

    deployment = model

    client = AzureOpenAI(
        api_version=api_version,
        azure_endpoint=endpoint,
        api_key=subscription_key,
    )

    try:
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ],
            max_completion_tokens=4096,
            temperature=1.0,
            top_p=1.0
        )

        print(response.choices[0].message.content, flush=True)

    except Exception as e:
        # 输出到 stderr 并返回非零退出码
        print(f"Python script error: {str(e)}", file=sys.stderr, flush=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
