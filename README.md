# ajrlewis_billing

## About

Automatically creates agreement for work and receipt for that work PDFs using LaTeX.

## Running

Create the following JSON input in `data/`:

```json
{
    "Client": "",
    "Reference": "",
    "BTC Address": "",
    "Transaction IDs": {
        "Deposit Date": "Transaction ID",
        "Balance Paid Date": "Transaction ID",
    },
    "Project Details": {
        "Title": "",
        "Summary": "",
        "Technology": "",
        "Estimated Duration": "5 days",
        "Estimated Cost": "btc 1.00 000 000"
    },
    "Outline of Proposed Work": {
        "Title": "Description",
        "Title 1": "Description 1"
    },
    "Success Criteria": [
        "All code functions in accordance to the details outlined above."
    ],
    "Terms & Conditions": {
        "Confidentiality": "All concepts for this project are the property of the client. A.J.R. Lewis will maintain confidentiality and not disclose any proprietary information. Replication of client data or ideas without permission is strictly prohibited.",
        "Payment Terms": "A.J.R. Lewis and the client agree to a 50% downpayment of the quoted amount at the start of their collaboration. The remainder will be paid at the time of delivery of the agreed work. Both parties agree that an on-chain transaction to the above address with 3 confirmations constitutes as payment received by A.J.R. Lewis. It is the responsibility of A.J.R. Lewis to ensure correct payment details are sent to the client.",
        "Ownership Rights": "A.J.R. Lewis retains ownership of any software created for the client until full payment is made. Upon full payment for the completed work, A.J.R. Lewis agrees to transfer to the client the copyright of the aforementioned work, including but not limited to all rights of reproduction, distribution, public performance, and adaptation, in all fields of exploitation, both currently known and hereafter devised. This transfer is triggered by the receipt of the full payment by A.J.R. Lewis (as defined above) and should take place immediately thereafter. A.J.R. Lewis shall execute all documents and take all actions necessary to effectuate such copyright transfer to the client, ensuring the client acquires full and exclusive rights to the work for its entire duration of copyright under the law."
    }
}
```

Run the code to generate the LaTeX PDF:

```bash
python3 code/generate.py <Agreement or Receipt>
```
