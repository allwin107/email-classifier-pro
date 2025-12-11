import spacy
import sklearn
import fastapi
import pandas

print("✅ Success! All libraries are installed.")
print(f"Spacy Version: {spacy.__version__}")
print(f"Scikit-Learn Version: {sklearn.__version__}")

# Test loading the English model
try:
    nlp = spacy.load("en_core_web_sm")
    print("✅ Spacy English model loaded successfully.")
except OSError:
    print("❌ Error: Spacy model not found. Run 'python -m spacy download en_core_web_sm'")