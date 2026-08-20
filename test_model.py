# test_model.py
import joblib
import numpy as np

print("=" * 60)
print("  🧪 Testing Model Loading")
print("=" * 60)
print()

try:
    # Load models
    model = joblib.load('models/kmeans_user_segmentation.pkl')
    print("✅ Model loaded successfully!")
    print(f"   - Type: {type(model).__name__}")
    print(f"   - Clusters: {model.n_clusters}")
    
    scaler = joblib.load('models/user_segmentation_scaler.pkl')
    print("✅ Scaler loaded successfully!")
    print(f"   - Type: {type(scaler).__name__}")
    
    # Test prediction
    test_data = [[100, 50, 20]]
    scaled = scaler.transform(test_data)
    prediction = model.predict(scaled)
    print(f"✅ Test prediction: Cluster {prediction[0]}")
    
    print()
    print("🎉 Everything is working! Run: run.bat")
    
except Exception as e:
    print(f"❌ Error: {e}")