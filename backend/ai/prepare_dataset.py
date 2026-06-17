import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


def load_prompt_injection():

    print("Loading Prompt Injection Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "prompt_injection.csv"
    )

    df = pd.read_json(
        file_path,
        lines=True
)

    print(df.head())

    return df


def load_pii():

    print("\nLoading PII Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "pii.csv"
    )

    df = pd.read_csv(
        file_path,
        sep="\t"
)

    print(df.head())

    return df


def load_adversarial():

    print("\nLoading Adversarial Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "adversarial.csv"
    )

    df = pd.read_csv(
        file_path,
        sep="\t"
)

    print(df.head())

    return df


def prepare_prompt_injection(df):

    prepared_rows = []

    for _, row in df.iterrows():

        if row["label"] == "malicious":
            label = "PROMPT_INJECTION"
        else:
            label = "SAFE"

        prepared_rows.append(
            {
                "text": row["prompt"],
                "label": label
            }
        )

    return pd.DataFrame(
        prepared_rows
    )


def prepare_pii(df):

    prepared_rows = []

    for _, row in df.iterrows():

        prepared_rows.append(
            {
                "text": row[df.columns[0]],
                "label": "PII_EXPOSURE"
            }
        )

    return pd.DataFrame(
        prepared_rows
    )


def prepare_adversarial(df):

    prepared_rows = []

    for _, row in df.iterrows():

        prepared_rows.append(
            {
                "text": row["persuasive_prompt"],
                "label": "PROMPT_INJECTION"
            }
        )

    return pd.DataFrame(
        prepared_rows
    )


def merge_datasets(
    prompt_df,
    pii_df,
    adversarial_df,
    safe_df,
    secrets_df,
    passwords_df,
    api_keys_df,
    tokens_df
):

    merged_df = pd.concat(
    [
        prompt_df,
        pii_df,
        adversarial_df,
        safe_df,
        secrets_df,
        passwords_df,
        api_keys_df,
        tokens_df
    ],
    ignore_index=True
    )

    print(
        f"\nTotal Samples: {len(merged_df)}"
    )

    print(
        merged_df["label"].value_counts()
    )
    merged_df["label"].value_counts().to_csv(
    BASE_DIR /
    "data" /
    "processed" /
    "label_distribution.csv"
)

    merged_df = merged_df.dropna()

    merged_df = merged_df.drop_duplicates()

    merged_df = merged_df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    return merged_df


def save_dataset(df):

    output_path = (
        BASE_DIR /
        "data" /
        "processed" /
        "secureshield_dataset.csv"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"\nDataset saved to:\n{output_path}"
    )


def load_safe():

    print("\nLoading SAFE Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "safe.csv"
    )

    df = pd.read_csv(
        file_path,
        sep="\t"
    )

    df = df.head(5000)

    print(df.head())
    print(df.columns)

    return df


def prepare_safe(df):

    prepared_rows = []

    for _, row in df.iterrows():

        prepared_rows.append(
            {
                "text": row["question"],
                "label": "SAFE"
            }
        )

    return pd.DataFrame(
        prepared_rows
    )


def load_secrets():

    print("\nLoading Secrets Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "secrets.csv"
    )

    df = pd.read_csv(file_path)

    print(df.head())

    return df

def prepare_secrets(df):

    prepared_rows = []

    for _, row in df.iterrows():

        prepared_rows.append(
            {
                "text": row["text"],
                "label": row["label"]
            }
        )

    return pd.DataFrame(
        prepared_rows
    )


def load_passwords():

    print("\nLoading Password Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "passwords.csv"
    )

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f.readlines()]

    df = pd.DataFrame(
        passwords[1:],   # skip header
        columns=["password"]
    )

    print(df.head())
    print("Total Password Rows:", len(df))

    return df


def prepare_passwords(df):

    df = df.sample(
    n=5000,
    random_state=42
    )
    
    prepared_rows = []

    for _, row in df.iterrows():

        prepared_rows.append(
            {
                "text": f"password={row['password']}",
                "label": "PASSWORD_EXPOSURE"
            }
        )

    return pd.DataFrame(prepared_rows)


def load_api_keys():

    print("\nLoading API Keys Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "api_keys.csv"
    )

    df = pd.read_csv(file_path)

    print(df.head())

    return df


def prepare_api_keys(df):

    df = pd.concat(
        [df] * 30,
        ignore_index=True
    )

    return pd.DataFrame(
        {
            "text": df["text"],
            "label": df["label"]
        }
    )

def load_tokens():

    print("\nLoading Tokens Dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "raw" /
        "tokens.csv"
    )

    df = pd.read_csv(file_path)

    print(df.head())

    return df


def prepare_tokens(df):

    df = pd.concat(
        [df] * 30,
        ignore_index=True
    )

    return pd.DataFrame(
        {
            "text": df["text"],
            "label": df["label"]
        }
    )


if __name__ == "__main__":

    prompt_df = load_prompt_injection()
    pii_df = load_pii()
    adversarial_df = load_adversarial()
    safe_df = load_safe()
    secrets_df = load_secrets()
    passwords_df = load_passwords()
    api_keys_df = load_api_keys()
    tokens_df = load_tokens()

    prepared_prompt_df = prepare_prompt_injection(prompt_df)
    prepared_pii_df = prepare_pii(pii_df)
    prepared_adversarial_df = prepare_adversarial(adversarial_df)
    prepared_safe_df = prepare_safe(safe_df)
    prepared_secrets_df = prepare_secrets(secrets_df)
    prepared_passwords_df = prepare_passwords(passwords_df)
    prepared_api_keys_df = prepare_api_keys(
    api_keys_df
    )

    prepared_tokens_df = prepare_tokens(
        tokens_df
    )


    merged_df = merge_datasets(
        prepared_prompt_df,
        prepared_pii_df,
        prepared_adversarial_df,
        prepared_safe_df,
        prepared_secrets_df,
        prepared_passwords_df,
        prepared_api_keys_df,
        prepared_tokens_df
    )

    save_dataset(
        merged_df
    )