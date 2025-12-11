import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from app.pii_masker import PIIMasker

# ================= CONFIGURATION =================
# ⚠️ UPDATED TO MATCH YOUR NEW CSV HEADERS
CSV_PATH = "data/enterprise_emails.csv"
TEXT_COLUMN = "email"      # matches Column A in your screenshot
LABEL_COLUMN = "type"      # matches Column B in your screenshot
# =================================================

def train_and_save():
    print(f"🚀 Starting Enterprise Training Pipeline...")
    
    # 1. Load Data
    print(f"📂 Loading data from {CSV_PATH}...")
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"   Loaded {len(df)} emails.")
    except FileNotFoundError:
        print("❌ Error: File not found. Did you put 'enterprise_emails.csv' in the data folder?")
        return

    # 2. Drop empty rows (Clean Data)
    df = df.dropna(subset=[TEXT_COLUMN, LABEL_COLUMN])

    # 3. PII Masking (The Heavy Lifting)
    # Note: On 13MB, Spacy can be slow. We will use a faster Regex-only approach for training speed 
    # unless you have a GPU. For now, let's stick to Regex for the bulk training.
    print("🛡️  Masking PII (This may take a minute)...")
    masker = PIIMasker()
    
    # We use a lambda to apply masking. 
    # TIP: If this is too slow, we can skip Spacy for training and just use Regex.
    # Let's try full masking first for quality.
    df['safe_text'] = df[TEXT_COLUMN].astype(str).apply(masker.mask_all)
    
    # 4. Split Data (80% Train, 20% Test)
    print("✂️  Splitting data into Training (80%) and Testing (20%) sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        df['safe_text'], df[LABEL_COLUMN], test_size=0.2, random_state=42
    )

    # 5. Define Pipeline
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(stop_words='english', max_features=5000)), 
        ('clf', MultinomialNB())
    ])

    # 6. Train
    print(f"🧠 Training model on {len(X_train)} emails...")
    pipeline.fit(X_train, y_train)
    print("✅ Training complete!")

    # 7. Evaluate (The Moment of Truth)
    print("\n📊 Evaluating Model Performance:")
    predictions = pipeline.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"   👉 Accuracy: {accuracy*100:.2f}%")
    
    print("\n   Detailed Report:")
    print(classification_report(y_test, predictions))

    # 8. Save
    print("💾 Saving model to disk...")
    joblib.dump(pipeline, "models/email_classifier.pkl")
    print("🎉 System Upgraded. Ready for Production.")

if __name__ == "__main__":
    train_and_save()