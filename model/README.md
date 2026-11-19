# Hosted model setup — secret contract

Status: preparation only. No model deployment code or hosted endpoint exists yet.

Use Modal's Custom secret type in workspace `r-delune`, environment `main`:

| Field | Value |
|---|---|
| Secret name | `fhir-test` |
| Environment-variable key | `PREFLIGHT_API_KEY` |
| Environment-variable value | A newly generated random token, kept private |

The planned deployment must load `modal.Secret.from_name("fhir-test")` and use
`PREFLIGHT_API_KEY` to authenticate requests to our inference endpoint. The local
client will need the same value when that integration is implemented. Keep it in
a password manager; do not paste it into chat, screenshots, source code or git.
This is our endpoint token, separate from Modal account/CLI credentials.

Creating this secret alone does not deploy or connect the model. The app still
uses its mock adapter. Pricing, GPU/region choice and deployment authorization
remain outstanding; the screenshot shows only $1 currently available credit.

Reference: https://modal.com/docs/guide/secrets
