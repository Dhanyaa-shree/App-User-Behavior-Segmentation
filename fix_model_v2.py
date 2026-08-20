# fix_model_v2.py
import joblib
import numpy as np
import os
import pickle

print("=" * 60)
print("  🔧 Fixing Model Files - Version 2")
print("=" * 60)
print(f"NumPy version: {np.__version__}")
print()

# Create models folder if it doesn't exist
os.makedirs('models', exist_ok=True)

try:
    # Try loading with joblib first
    print("📂 Attempting to load models with joblib...")
    try:
        model = joblib.load('models/kmeans_user_segmentation.pkl')
        scaler = joblib.load('models/user_segmentation_scaler.pkl')
        print("✅ Models loaded successfully with joblib!")
    except Exception as e:
        print(f"⚠️ Joblib load failed: {e}")
        print("📂 Attempting to load with pickle...")
        try:
            with open('models/kmeans_user_segmentation.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('models/user_segmentation_scaler.pkl', 'rb') as f:
                scaler = pickle.load(f)
            print("✅ Models loaded successfully with pickle!")
        except Exception as e2:
            print(f"⚠️ Pickle load failed: {e2}")
            print("🔄 Creating new models from data...")
            raise
    
    # Re-save with current numpy version
    print("💾 Re-saving models...")
    joblib.dump(model, 'models/kmeans_user_segmentation.pkl')
    joblib.dump(scaler, 'models/user_segmentation_scaler.pkl')
    
    print("✅ Models fixed successfully!")
    print()
    print("🔄 Now restart your application")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("🔄 Creating new models from data...")
    
    try:
        import pandas as pd
        from sklearn.cluster import KMeans
        from sklearn.preprocessing import StandardScaler
        
        # Load data
        print("📂 Loading data...")
        try:
            df = pd.read_csv('data/app_user_segmentation_results.csv')
            print("✅ Data loaded from results file!")
        except FileNotFoundError:
            df = pd.read_csv('data/app_user_behavior.csv')
            print("✅ Data loaded from behavior file!")
        
        # Create features
        if 'weekly_engagement_minutes' not in df.columns:
            print("📊 Creating features...")
            df['weekly_engagement_minutes'] = df['sessions_per_week'] * df['avg_session_duration_min']
            df['interaction_score'] = df['feature_clicks_per_session'] + df['notifications_opened_per_week'] + df['in_app_search_count']
            df['content_activity'] = df['content_downloads'] + df['social_shares']
        
        features = ['weekly_engagement_minutes', 'interaction_score', 'content_activity']
        X = df[features].copy()
        
        print(f"📊 Features: {features}")
        print(f"📊 Data shape: {X.shape}")
        
        # Scale
        print("📊 Scaling features...")
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Train model
        print("📊 Training K-Means model...")
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=30)
        kmeans.fit(X_scaled)
        
        # Save models
        print("💾 Saving models...")
        joblib.dump(kmeans, 'models/kmeans_user_segmentation.pkl')
        joblib.dump(scaler, 'models/user_segmentation_scaler.pkl')
        
        print()
        print("✅ New models created successfully!")
        print(f"   - Clusters: {kmeans.n_clusters}")
        print(f"   - Features: {features}")
        print()
        print("🔄 Now restart your application with: run.bat")
        
    except Exception as e3:
        print(f"❌ Failed to create new models: {e3}")
        print()
        print("Please check that your data file exists in 'data/' folder")
        print("And that you have required packages installed.")