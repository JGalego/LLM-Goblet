set dotenv-load := true

region := env_var_or_default("AWS_DEFAULT_REGION", "us-east-1")

default:
    @just --list

local stage="dev" host="0.0.0.0" port="8080":
    chalice local --host {{host}} --port {{port}} --stage {{stage}} --autoreload

# Builds and deploys the application
deploy stage="dev":
    AWS_DEFAULT_REGION={{region}} chalice deploy --stage {{stage}}

# Destroys the application
destroy stage="dev":
    AWS_DEFAULT_REGION={{region}} chalice delete --stage {{stage}}

# Checks if the REST API is up
check stage="dev":
    @curl -s `chalice url --stage {{stage}}`/health --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" -H "x-amz-security-token: $AWS_SESSION_TOKEN" --aws-sigv4 "aws:amz:{{region}}:execute-api" | jq .

# Performs text completion on a user message
talk message stage="dev" model="bedrock/us.anthropic.claude-3-haiku-20240307-v1:0":
    @curl -s -X POST `chalice url --stage {{stage}}`/chat/completions --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" --aws-sigv4 "aws:amz:{{region}}:execute-api" -H "x-amz-security-token: $AWS_SESSION_TOKEN" -H "Accept: application/json" -H "Content-Type: application/json" -d '{"model": "{{model}}", "messages": [{"role": "user", "content": "{{message}}"}], "temperature": 0}' | jq -r .choices[0].message.content

# Generates embeddings for a given input
embed text stage="dev" model="bedrock/cohere.embed-multilingual-v3":
    @curl -s -X POST `chalice url --stage {{stage}}`/embeddings --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" --aws-sigv4 "aws:amz:{{region}}:execute-api" -H "x-amz-security-token: $AWS_SESSION_TOKEN" -H "Accept: application/json" -H "Content-Type: application/json" -d '{"model": "{{model}}", "input": ["{{text}}"], "temperature": 0}' | jq -r .data[].embedding

# Generates a new image from a prompt
image prompt stage="dev" model="bedrock/stability.stable-diffusion-xl-v1" size="1024x1024" seed="42":
    @curl -s -X POST `chalice url --stage {{stage}}`/images/generations --user "$AWS_ACCESS_KEY_ID":"$AWS_SECRET_ACCESS_KEY" --aws-sigv4 "aws:amz:{{region}}:execute-api" -H "x-amz-security-token: $AWS_SESSION_TOKEN" -H "Accept: application/json" -H "Content-Type: application/json" -d '{"model": "{{model}}", "prompt": "{{prompt}}", "size": "{{size}}", "seed": {{seed}}}' | jq -r .data[0].b64_json
