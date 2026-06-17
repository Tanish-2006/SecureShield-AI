import pandas as pd
from pathlib import Path
from transformers import DistilBertTokenizer
from datasets import Dataset
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from transformers import (
    DistilBertForSequenceClassification,
    TrainingArguments,
    Trainer
)


BASE_DIR = Path(__file__).resolve().parent


def load_dataset():

    print("Loading dataset...")

    file_path = (
        BASE_DIR /
        "data" /
        "processed" /
        "secureshield_dataset.csv"
    )

    df = pd.read_csv(file_path)

    print(df.head())

    print("\nDataset Shape:")
    print(df.shape)

    return df


def encode_labels(df):

    print("\nEncoding labels...")

    encoder = LabelEncoder()

    df["label_encoded"] = encoder.fit_transform(
        df["label"]
    )

    print("\nLabel Mapping:")

    for i, label in enumerate(
        encoder.classes_
    ):
        print(
            f"{label} -> {i}"
        )

    models_dir = (
        BASE_DIR /
        "models"
    )

    models_dir.mkdir(
        exist_ok=True
    )

    joblib.dump(
        encoder,
        models_dir /
        "label_encoder.pkl"
    )

    return df


def split_dataset(df):

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"],
        df["label_encoded"],
        test_size=0.2,
        random_state=42,
        stratify=df["label_encoded"]
    )

    print(
        f"Train Samples: {len(X_train)}"
    )

    print(
        f"Test Samples: {len(X_test)}"
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test
    )


def create_tokenizer():

    print("\nLoading DistilBERT Tokenizer...")

    tokenizer = DistilBertTokenizer.from_pretrained(
        "distilbert-base-uncased"
    )

    return tokenizer


def create_hf_dataset(
    X_train,
    X_test,
    y_train,
    y_test
):

    train_dataset = Dataset.from_dict(
        {
            "text": list(X_train),
            "label": list(y_train)
        }
    )

    test_dataset = Dataset.from_dict(
        {
            "text": list(X_test),
            "label": list(y_test)
        }
    )

    print(
        "\nHuggingFace datasets created."
    )

    return train_dataset, test_dataset


def tokenize_dataset(
    dataset,
    tokenizer
):

    return dataset.map(
        lambda x: tokenizer(
            x["text"],
            truncation=True,
            padding="max_length",
            max_length=128
        ),
        batched=True
    )


def create_model():

    print("\nLoading DistilBERT Model...")

    model = DistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased",
        num_labels=6
    )

    return model


def train_model(
    model,
    train_dataset,
    test_dataset
):

    training_args = TrainingArguments(
        output_dir="./results",
        eval_strategy="epoch",
        save_strategy="epoch",
        num_train_epochs=2,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        logging_steps=100,
        load_best_model_at_end=True
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset
    )

    trainer.train()

    return trainer


def save_model(
    trainer
):

    model_path = (
        BASE_DIR /
        "models" /
        "secureshield_model"
    )

    trainer.save_model(
        model_path
    )

    print(
        f"\nModel saved to:\n{model_path}"
    )


if __name__ == "__main__":

    df = load_dataset()

    df = encode_labels(df)

    X_train, X_test, y_train, y_test = split_dataset(
        df
    )
    tokenizer = create_tokenizer()

    train_dataset, test_dataset = create_hf_dataset(
        X_train,
        X_test,
        y_train,
        y_test
    )

    train_dataset = tokenize_dataset(
        train_dataset,
        tokenizer
    )

    test_dataset = tokenize_dataset(
        test_dataset,
        tokenizer
    )

    print("\nTokenization Complete")
    model = create_model()

    trainer = train_model(
        model,
        train_dataset,
        test_dataset
    )

    save_model(
        trainer
    )