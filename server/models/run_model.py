import sys
import json
import os
from openai import AzureOpenAI


def main():
    endpoint = "aaa"
    subscription_key = "aaa"
    api_version = "2024-12-01-preview"

    if len(sys.argv) < 3:
        print("Usage: python run_model.py <model> <question>")
        sys.exit(1)

    model = sys.argv[1]
    question = sys.argv[2]
    # print(f"Using model: {model} with question: {question}")

    # model = "gpt-4o"  # Default model
    # question = "I am going to Paris, what should I see?"  # Default question
    deployment = model
    # print(f"Using model: {model} with deployment: {deployment}")

    # client = AzureOpenAI(
    #     api_version=api_version,
    #     azure_endpoint=endpoint,
    #     api_key=subscription_key,
    # )

    try:
        # response = client.chat.completions.create(
        #     messages=[
        #         {
        #             "role": "system",
        #             "content": "You are a helpful assistant.",
        #         },
        #         {
        #             "role": "user",
        #             "content": question,
        #         }
        #     ],
        #     max_completion_tokens=4096,
        #     temperature=1.0,
        #     top_p=1.0,
        #     model=deployment
        # )
        # print(response.choices[0].message.content+f"({model})")
        print(f"Simulated response for model {model} with question: {question}")
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
