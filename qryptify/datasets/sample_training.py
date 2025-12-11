import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings
warnings.filterwarnings('ignore')

print("="*70)
print("NIST CRYPTOGRAPHIC ALGORITHM CLASSIFICATION")
print("="*70)

print("\n[STEP 1] Loading and preprocessing dataset...")
df = pd.read_csv(r"C:\Users\Dell\Downloads\nist_test.csv")
print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

print("\n[STEP 2] Shuffling dataset...")
df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print("✓ Dataset shuffled with random_state=42")

print("\nFirst 10 algorithms after shuffle (should be mixed):")
print(df['Algorithm'].head(10).tolist())

print(f"\nDataset statistics:")
print(f"  - Unique Algorithms: {df['Algorithm'].nunique()}")
print(f"  - Unique Categories: {df['Category'].nunique()}")
print(f"  - Unique Algorithm Types: {df['Algorithm_Type'].nunique()}")

print("\nSamples per algorithm:")
algo_counts = df['Algorithm'].value_counts().sort_index()
print(f"  Min: {algo_counts.min()}, Max: {algo_counts.max()}, Mean: {algo_counts.mean():.0f}")


print("\n[STEP 3] Encoding labels...")
le_cat = LabelEncoder()
le_type = LabelEncoder()
le_algo = LabelEncoder()

y_cat = le_cat.fit_transform(df["Category"])
y_type = le_type.fit_transform(df["Algorithm_Type"])
y_algo = le_algo.fit_transform(df["Algorithm"])

print(f"✓ Encoded classes:")
print(f"  - Categories: {len(le_cat.classes_)}")
print(f"  - Algorithm Types: {len(le_type.classes_)}")
print(f"  - Algorithms: {len(le_algo.classes_)}")

X = df.drop(["Category", "Algorithm_Type", "Algorithm"], axis=1)
print(f"\n✓ Feature matrix: {X.shape[1]} features")

print("\n[STEP 4] Scaling features...")
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns, index=X.index)
print("✓ Features scaled using StandardScaler")

print("\n[STEP 5] Splitting data (80% train, 20% test)...")
X_train, X_test, y_cat_train, y_cat_test = train_test_split(
    X_scaled, y_cat, test_size=0.2, random_state=42, stratify=y_cat
)

_, _, y_type_train, y_type_test = train_test_split(
    X_scaled, y_type, test_size=0.2, random_state=42, stratify=y_type
)

_, _, y_algo_train, y_algo_test = train_test_split(
    X_scaled, y_algo, test_size=0.2, random_state=42, stratify=y_algo
)

print(f"✓ Train set: {X_train.shape[0]} samples")
print(f"✓ Test set: {X_test.shape[0]} samples")

print("\n" + "="*70)
print("MODEL TRAINING")
print("="*70)

print("\n[MODEL 1/4] Training Direct Algorithm Classifier...")
print("  → Predicting all 25 algorithms directly")

direct_model = XGBClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    eval_metric="mlogloss",
    random_state=42,
    tree_method='hist',
    n_jobs=-1,
    early_stopping_rounds=50
)

direct_model.fit(X_train, y_algo_train, 
                 eval_set=[(X_test, y_algo_test)],
                 verbose=False)

direct_pred = direct_model.predict(X_test)
direct_acc = accuracy_score(y_algo_test, direct_pred)
print(f"✓ Direct Model trained - Accuracy: {direct_acc*100:.2f}%")

print("\n[MODEL 2/4] Training Category Model...")
print("  → First level: Predict cryptographic category")

cat_model = XGBClassifier(
    n_estimators=400,
    max_depth=7,
    learning_rate=0.06,
    subsample=0.85,
    colsample_bytree=0.85,
    min_child_weight=2,
    gamma=0.05,
    reg_alpha=0.05,
    reg_lambda=0.5,
    eval_metric="mlogloss",
    random_state=42,
    tree_method='hist',
    n_jobs=-1,
    early_stopping_rounds=30
)

cat_model.fit(X_train, y_cat_train,
              eval_set=[(X_test, y_cat_test)],
              verbose=False)

cat_pred_train = cat_model.predict(X_train)
cat_pred_test = cat_model.predict(X_test)
cat_acc = accuracy_score(y_cat_test, cat_pred_test)
print(f"✓ Category Model trained - Accuracy: {cat_acc*100:.2f}%")

print("\n[MODEL 3/4] Training Algorithm Type Model...")
print("  → Second level: Predict algorithm type using category")

X_with_cat_train = X_train.copy()
X_with_cat_train["cat_pred"] = cat_pred_train
X_with_cat_test = X_test.copy()
X_with_cat_test["cat_pred"] = cat_pred_test

type_model = XGBClassifier(
    n_estimators=400,
    max_depth=7,
    learning_rate=0.06,
    subsample=0.85,
    colsample_bytree=0.85,
    min_child_weight=2,
    gamma=0.05,
    reg_alpha=0.05,
    reg_lambda=0.5,
    eval_metric="mlogloss",
    random_state=42,
    tree_method='hist',
    n_jobs=-1,
    early_stopping_rounds=30
)

type_model.fit(X_with_cat_train, y_type_train,
               eval_set=[(X_with_cat_test, y_type_test)],
               verbose=False)

type_pred_train = type_model.predict(X_with_cat_train)
type_pred_test = type_model.predict(X_with_cat_test)
type_acc = accuracy_score(y_type_test, type_pred_test)
print(f"✓ Algorithm Type Model trained - Accuracy: {type_acc*100:.2f}%")

print("\n[MODEL 4/4] Training Final Algorithm Model (Hierarchical)...")
print("  → Third level: Predict specific algorithm using category + type")

X_with_both_train = X_train.copy()
X_with_both_train["cat_pred"] = cat_pred_train
X_with_both_train["type_pred"] = type_pred_train

X_with_both_test = X_test.copy()
X_with_both_test["cat_pred"] = cat_pred_test
X_with_both_test["type_pred"] = type_pred_test

hier_algo_model = XGBClassifier(
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    eval_metric="mlogloss",
    random_state=42,
    tree_method='hist',
    n_jobs=-1,
    early_stopping_rounds=50
)

hier_algo_model.fit(X_with_both_train, y_algo_train,
                    eval_set=[(X_with_both_test, y_algo_test)],
                    verbose=False)

hier_pred = hier_algo_model.predict(X_with_both_test)
hier_acc = accuracy_score(y_algo_test, hier_pred)
print(f"✓ Hierarchical Algorithm Model trained - Accuracy: {hier_acc*100:.2f}%")

print("\n[ENSEMBLE] Creating weighted ensemble...")
print("  → Combining direct and hierarchical predictions")

ensemble_pred = []
for i in range(len(y_algo_test)):
    direct_prob = direct_model.predict_proba(X_test.iloc[[i]])[0]
    hier_prob = hier_algo_model.predict_proba(X_with_both_test.iloc[[i]])[0]
    combined_prob = (direct_acc * direct_prob + hier_acc * hier_prob) / (direct_acc + hier_acc)
    ensemble_pred.append(np.argmax(combined_prob))

ensemble_pred = np.array(ensemble_pred)
ensemble_acc = accuracy_score(y_algo_test, ensemble_pred)
print(f"✓ Ensemble Model created - Accuracy: {ensemble_acc*100:.2f}%")

def evaluate_model(name, y_true, y_pred, label_encoder):
    print("\n" + "="*70)
    print(f"EVALUATION: {name}")
    print("="*70)
    
    y_true_labels = label_encoder.inverse_transform(y_true)
    y_pred_labels = label_encoder.inverse_transform(y_pred)
    
    acc = accuracy_score(y_true_labels, y_pred_labels)
    f1 = f1_score(y_true_labels, y_pred_labels, average='weighted')
    
    print(f"\n📊 Overall Metrics:")
    print(f"   Accuracy:  {acc*100:.2f}%")
    print(f"   F1-Score:  {f1*100:.2f}%")
    
    print("\n📋 Per-Class Performance:")
    report = classification_report(y_true_labels, y_pred_labels, digits=3, output_dict=True)

    print(f"   Average Precision: {report['weighted avg']['precision']*100:.2f}%")
    print(f"   Average Recall:    {report['weighted avg']['recall']*100:.2f}%")
    print(f"   Average F1-Score:  {report['weighted avg']['f1-score']*100:.2f}%")
    
    print("\n📄 Detailed Classification Report:")
    print(classification_report(y_true_labels, y_pred_labels, digits=3))
    
    cm = confusion_matrix(y_true_labels, y_pred_labels)
    
    if len(label_encoder.classes_) <= 10:
        plt.figure(figsize=(12, 10))
        sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", 
                    xticklabels=label_encoder.classes_, 
                    yticklabels=label_encoder.classes_)
        plt.title(f"{name} – Confusion Matrix")
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    else:
        plt.figure(figsize=(16, 14))
        sns.heatmap(cm, annot=False, cmap="Blues", cbar=True)
        plt.title(f"{name} – Confusion Matrix (25 classes)")
        plt.xlabel("Predicted Algorithm")
        plt.ylabel("True Algorithm")
        plt.tight_layout()
        plt.show()
    
    return acc, f1

print("\n\n" + "="*70)
print("DETAILED MODEL EVALUATION")
print("="*70)

cat_acc_eval, cat_f1 = evaluate_model("Category Model", y_cat_test, cat_pred_test, le_cat)
type_acc_eval, type_f1 = evaluate_model("Algorithm Type Model", y_type_test, type_pred_test, le_type)
direct_acc_eval, direct_f1 = evaluate_model("Direct Algorithm Model", y_algo_test, direct_pred, le_algo)
hier_acc_eval, hier_f1 = evaluate_model("Hierarchical Algorithm Model", y_algo_test, hier_pred, le_algo)
ensemble_acc_eval, ensemble_f1 = evaluate_model("Ensemble Model", y_algo_test, ensemble_pred, le_algo)

print("\n\n" + "="*70)
print("🏆 FINAL ACCURACY COMPARISON")
print("="*70)
print(f"\n{'Model':<30} {'Accuracy':<12} {'F1-Score':<12}")
print("-" * 70)
print(f"{'Direct Model':<30} {direct_acc*100:>6.2f}%      {direct_f1*100:>6.2f}%")
print(f"{'Hierarchical Model':<30} {hier_acc*100:>6.2f}%      {hier_f1*100:>6.2f}%")
print(f"{'Ensemble Model':<30} {ensemble_acc*100:>6.2f}%      {ensemble_f1*100:>6.2f}%")
print("-" * 70)

best_model_name = max(
    [("Direct", direct_acc), ("Hierarchical", hier_acc), ("Ensemble", ensemble_acc)],
    key=lambda x: x[1]
)[0]

print(f"\n✨ RECOMMENDATION: Use {best_model_name} Model (highest accuracy)")

def predict_algorithm(sample_features, use_ensemble=True):
    sample_scaled = pd.DataFrame(scaler.transform(sample_features), 
                                 columns=sample_features.columns)
    
    if use_ensemble:
        direct_prob = direct_model.predict_proba(sample_scaled)[0]
        cat_pred_sample = cat_model.predict(sample_scaled)[0]
        sample_with_cat = sample_scaled.copy()
        sample_with_cat["cat_pred"] = cat_pred_sample
        
        type_pred_sample = type_model.predict(sample_with_cat)[0]
        sample_with_both = sample_with_cat.copy()
        sample_with_both["type_pred"] = type_pred_sample
        
        hier_prob = hier_algo_model.predict_proba(sample_with_both)[0]
        combined_prob = (direct_acc * direct_prob + hier_acc * hier_prob) / (direct_acc + hier_acc)
        pred_idx = np.argmax(combined_prob)
        top5_idx = np.argsort(combined_prob)[-5:][::-1]
        top5_algos = [(le_algo.inverse_transform([idx])[0], combined_prob[idx]) 
                      for idx in top5_idx]
        return {
            "algorithm": le_algo.inverse_transform([pred_idx])[0],
            "confidence": combined_prob[pred_idx] * 100,
            "category": le_cat.inverse_transform([cat_pred_sample])[0],
            "type": le_type.inverse_transform([type_pred_sample])[0],
            "top5": top5_algos
        }
    else:
        direct_prob = direct_model.predict_proba(sample_scaled)[0]
        pred_idx = np.argmax(direct_prob)
        
        top5_idx = np.argsort(direct_prob)[-5:][::-1]
        top5_algos = [(le_algo.inverse_transform([idx])[0], direct_prob[idx]) 
                      for idx in top5_idx]
        
        return {
            "algorithm": le_algo.inverse_transform([pred_idx])[0],
            "confidence": direct_prob[pred_idx] * 100,
            "top5": top5_algos
        }

print("\n\n" + "="*70)
print("🔍 SAMPLE PREDICTION TEST")
print("="*70)

sample = X.iloc[[100]] 
result = predict_algorithm(sample, use_ensemble=True)

print(f"\n✅ Predicted Algorithm: {result['algorithm']}")
print(f"   Confidence: {result['confidence']:.2f}%")
if 'category' in result:
    print(f"   Category: {result['category']}")
    print(f"   Type: {result['type']}")

print("\n📊 Top 5 Predictions:")
for i, (alg, prob) in enumerate(result['top5'], 1):
    bar = "█" * int(prob * 50)  # Visual bar
    print(f"   {i}. {alg:<25} {prob*100:>6.2f}% {bar}")

print("\n\n" + "="*70)
print("💾 SAVING MODELS")
print("="*70)

joblib.dump(direct_model, "direct_algo_model.joblib")
joblib.dump(cat_model, "cat_model.joblib")
joblib.dump(type_model, "type_model.joblib")
joblib.dump(hier_algo_model, "hier_algo_model.joblib")
joblib.dump(scaler, "feature_scaler.joblib")

joblib.dump(le_cat, "le_cat.joblib")
joblib.dump(le_type, "le_type.joblib")
joblib.dump(le_algo, "le_algo.joblib")

joblib.dump({'direct_acc': direct_acc, 'hier_acc': hier_acc}, "model_weights.joblib")

print("\n✓ All models saved successfully!")
print("\n📁 Saved files:")
print("   • direct_algo_model.joblib (Direct classifier)")
print("   • hier_algo_model.joblib (Hierarchical classifier)")
print("   • cat_model.joblib (Category classifier)")
print("   • type_model.joblib (Type classifier)")
print("   • feature_scaler.joblib ⚠️  REQUIRED for predictions")
print("   • le_cat.joblib, le_type.joblib, le_algo.joblib (Label encoders)")
print("   • model_weights.joblib (Ensemble weights)")

print("\n" + "="*70)
print("✨ TRAINING COMPLETE!")
print("="*70)

