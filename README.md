# smart-reschedule-assistant-genaimodel
Smart Reschedule Assistant Generative AI Model

## 📂 Repository Structure

```text
├── main.py                     # Main FastAPI application entrypoint
├── requirements.txt            # Python dependencies
├── models/
│   ├── best_intent_classifier.joblib  # Trained SVM model for intent classification
│   └── tfidf_vectorizer.joblib        # TF-IDF vectorizer for text preprocessing
└── gym_vector_db/              # Persistent ChromaDB vector database directory
    ├── chroma.sqlite3
    └── [uuid-folders]
```
