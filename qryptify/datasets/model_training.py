import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from sklearn.preprocessing import LabelEncoder, StandardScaler
from xgboost import XGBClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import warnings

warnings.filterwarnings("ignore")

# Set publication-quality style
plt.style.use("seaborn-v0_8-paper")
sns.set_palette("husl")
plt.rcParams["figure.dpi"] = 300
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["font.size"] = 10
plt.rcParams["font.family"] = "serif"

print("=" * 80)
print("NIST CRYPTOGRAPHIC ALGORITHM CLASSIFICATION (ROBUST & CLEAN PLOTS)")
print("=" * 80)

# =============================================================================
# STEP 1: Load and validate data
# =============================================================================
print("\n[STEP 1] Loading dataset...")
df = pd.read_csv(
    r"C:\Users\Dell\Desktop\DESKTOP_FOLDER\FINAL YEAR PROJECT\qryptify\nistest1.csv"
)
print(f"✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

required_cols = ["Category", "Algorithm_Type", "Algorithm"]
if not all(col in df.columns for col in required_cols):
    print(f"❌ ERROR: Missing columns. Need: {required_cols}")
    raise SystemExit(1)

# =============================================================================
# STEP 2: Data quality + feature analysis
# =============================================================================
print("\n[STEP 2] Data quality check...")
df = df.fillna(0.0).replace([np.inf, -np.inf], 0.0)
print("✓ Missing/infinite values handled")

df = df.sample(frac=1, random_state=42).reset_index(drop=True)
print("✓ Dataset shuffled")

print("\n[STEP 3] Feature analysis...")
metadata_cols = ["Category", "Algorithm_Type", "Algorithm"]
X = df.drop(metadata_cols, axis=1)

pvalue_features = [col for col in X.columns if "pvalue" in col.lower()]
pass_features = [col for col in X.columns if "pass" in col.lower()]
enhanced_features = [col for col in X.columns if col not in pvalue_features + pass_features]

print(f"  Total Features: {X.shape[1]}")
print(f"  ├─ NIST P-values: {len(pvalue_features)}")
print(f"  ├─ NIST Pass/Fail: {len(pass_features)}")
print(f"  └─ Enhanced: {len(enhanced_features)}")

# =============================================================================
# VISUALIZATION 1: Dataset Overview
# =============================================================================
print("\n📈 Creating Visualization 1: Dataset Overview (Separated plots)...")

# Category distribution
plt.figure(figsize=(6, 5))
cat_counts = df["Category"].value_counts()
bars = plt.bar(
    cat_counts.index,
    cat_counts.values,
    color=["#3498db", "#e74c3c", "#2ecc71"],
    edgecolor="black",
    alpha=0.8,
)
plt.title("Category Distribution", fontsize=12, fontweight="bold")
plt.ylabel("Count", fontsize=10)
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)
for bar in bars:
    h = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        h,
        f"{int(h)}",
        ha="center",
        va="bottom",
        fontweight="bold",
    )
plt.tight_layout()
plt.savefig("01a_category_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

# Algorithm Type distribution
plt.figure(figsize=(10, 6))
type_counts = df["Algorithm_Type"].value_counts().sort_values()
plt.barh(
    range(len(type_counts)),
    type_counts.values,
    color=plt.cm.tab10(np.linspace(0, 1, len(type_counts))),
    edgecolor="black",
    alpha=0.8,
)
plt.yticks(range(len(type_counts)), type_counts.index, fontsize=9)
plt.title("Algorithm Type Distribution", fontsize=12, fontweight="bold")
plt.xlabel("Count", fontsize=10)
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("01b_algorithm_type_distribution.png", dpi=300, bbox_inches="tight")
plt.close()

# Algorithm distribution (top 15)
plt.figure(figsize=(12, 6))
algo_counts = df["Algorithm"].value_counts().head(15)
plt.bar(
    range(len(algo_counts)),
    algo_counts.values,
    color=plt.cm.viridis(np.linspace(0, 1, len(algo_counts))),
    edgecolor="black",
    alpha=0.8,
)
plt.xticks(range(len(algo_counts)), range(1, len(algo_counts) + 1))
plt.title("Top 15 Algorithms", fontsize=12, fontweight="bold")
plt.xlabel("Rank", fontsize=10)
plt.ylabel("Count", fontsize=10)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("01c_top_15_algorithms.png", dpi=300, bbox_inches="tight")
plt.close()

# Feature breakdown
plt.figure(figsize=(6, 6))
feature_counts = [len(pvalue_features), len(pass_features), len(enhanced_features)]
plt.pie(
    feature_counts,
    labels=["P-values", "Pass/Fail", "Enhanced"],
    colors=["#3498db", "#e74c3c", "#2ecc71"],
    autopct="%1.1f%%",
    startangle=90,
    textprops={"fontsize": 9, "weight": "bold"},
)
plt.title("Feature Types", fontsize=12, fontweight="bold")
plt.tight_layout()
plt.savefig("01d_feature_types.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Saved 01a to 01d.")

# =============================================================================
# VISUALIZATION 2: Feature Analysis
# =============================================================================
print("\n📈 Creating Visualization 2: Feature Analysis (Separated plots)...")

# Enhanced features boxplot
if len(enhanced_features) > 0:
    plt.figure(figsize=(10, 6))
    sample = X[enhanced_features].sample(min(1000, len(X)), random_state=42)
    bp = plt.boxplot(
        [sample[col] for col in enhanced_features],
        patch_artist=True,
        widths=0.6,
    )
    for patch, color in zip(bp["boxes"], plt.cm.Set3(np.linspace(0, 1, len(enhanced_features)))):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    plt.xticks(
        range(1, len(enhanced_features) + 1),
        [f[:8] for f in enhanced_features],
        rotation=90,
        fontsize=7,
    )
    plt.title("Enhanced Features Distribution", fontweight="bold")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("02a_enhanced_features_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

# Feature variance
plt.figure(figsize=(8, 6))
var_top = X.var().sort_values(ascending=False).head(15)
plt.barh(
    range(len(var_top)),
    var_top.values,
    color=plt.cm.plasma(np.linspace(0, 1, len(var_top))),
    edgecolor="black",
    alpha=0.8,
)
plt.yticks(range(len(var_top)), [f[:20] for f in var_top.index], fontsize=8)
plt.title("Top 15 by Variance", fontweight="bold")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("02b_feature_variance.png", dpi=300, bbox_inches="tight")
plt.close()

# NIST pass rates
if len(pass_features) > 0:
    plt.figure(figsize=(8, 6))
    pass_rates = df[pass_features].mean().sort_values(ascending=False)
    colors = [
        "green" if x > 0.95 else "orange" if x > 0.8 else "red" for x in pass_rates
    ]
    plt.barh(range(len(pass_rates)), pass_rates.values, color=colors, alpha=0.7)
    plt.yticks(
        range(len(pass_rates)),
        [f.replace("_pass", "")[:20] for f in pass_rates.index],
        fontsize=7,
    )
    plt.title("NIST Test Pass Rates", fontweight="bold")
    plt.xlim([0, 1])
    plt.axvline(0.95, color="green", linestyle="--", alpha=0.5)
    plt.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    plt.savefig("02c_nist_pass_rates.png", dpi=300, bbox_inches="tight")
    plt.close()

# Correlation matrix (top 10 enhanced)
if len(enhanced_features) >= 10:
    plt.figure(figsize=(8, 8))
    subset = enhanced_features[:10]
    corr = X[subset].corr()
    sns.heatmap(corr, cmap="coolwarm", vmin=-1, vmax=1, annot=False)
    plt.xticks(
        range(len(subset)),
        [f[:8] for f in subset],
        rotation=90,
        fontsize=7,
    )
    plt.yticks(range(len(subset)), [f[:8] for f in subset], fontsize=7)
    plt.title("Feature Correlation (Top 10 Enhanced)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("02d_feature_correlation.png", dpi=300, bbox_inches="tight")
    plt.close()

# P-value distribution
if len(pvalue_features) > 0:
    plt.figure(figsize=(7, 5))
    all_pvals = df[pvalue_features].values.flatten()
    plt.hist(all_pvals, bins=50, color="steelblue", edgecolor="black", alpha=0.7)
    plt.axvline(0.01, color="red", linestyle="--", linewidth=2, label="α=0.01")
    plt.title("P-Value Distribution", fontweight="bold")
    plt.xlabel("P-value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig("02e_pvalue_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

# Class balance
plt.figure(figsize=(7, 5))
algo_dist = df["Algorithm"].value_counts()
plt.hist(algo_dist.values, bins=20, color="teal", edgecolor="black", alpha=0.7)
plt.axvline(
    algo_dist.mean(),
    color="red",
    linestyle="--",
    label=f"Mean: {algo_dist.mean():.0f}",
)
plt.title("Class Balance (Algorithms)", fontweight="bold")
plt.xlabel("Samples/Algorithm")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("02f_class_balance.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Saved 02a to 02f.")

# =============================================================================
# STEP 3: Encoding and scaling
# =============================================================================
print("\n[STEP 4] Encoding labels...")
le_cat = LabelEncoder()
le_type = LabelEncoder()
le_algo = LabelEncoder()

y_cat = le_cat.fit_transform(df["Category"])
y_type = le_type.fit_transform(df["Algorithm_Type"])
y_algo = le_algo.fit_transform(df["Algorithm"])

print(f"  Categories: {len(le_cat.classes_)}")
print(f"  Types: {len(le_type.classes_)}")
print(f"  Algorithms: {len(le_algo.classes_)}")

print("\n[STEP 5] Scaling features...")
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
print("✓ StandardScaler applied")

# =============================================================================
# STEP 4: Train-Validation-Test Split (consistent indices)
# =============================================================================
print("\n[STEP 6] Train-Validation-Test split (70/10/20)...")

idx = np.arange(len(X_scaled))

# 80/20 split using Category for stratification
idx_trainval, idx_test = train_test_split(
    idx, test_size=0.2, random_state=42, stratify=y_cat
)

# 70/10 split inside trainval (overall 70/10)
idx_train, idx_val = train_test_split(
    idx_trainval, test_size=0.125, random_state=42, stratify=y_cat[idx_trainval]
)

X_train = X_scaled.iloc[idx_train]
X_val = X_scaled.iloc[idx_val]
X_test = X_scaled.iloc[idx_test]

y_cat_train, y_cat_val, y_cat_test = (
    y_cat[idx_train],
    y_cat[idx_val],
    y_cat[idx_test],
)
y_type_train, y_type_val, y_type_test = (
    y_type[idx_train],
    y_type[idx_val],
    y_type[idx_test],
)
y_algo_train, y_algo_val, y_algo_test = (
    y_algo[idx_train],
    y_algo[idx_val],
    y_algo[idx_test],
)

print(
    f"  Train: {X_train.shape[0]} | Validation: {X_val.shape[0]} | Test: {X_test.shape[0]}"
)

# =============================================================================
# VISUALIZATION 3: Train-Validation-Test Split
# =============================================================================
print("\n📈 Creating Visualization 3: Train-Validation-Test Split (Separated plots)...")

datasets = [
    (y_cat_train, y_cat_val, y_cat_test, le_cat, "Category", "03a_category_split.png"),
    (y_type_train, y_type_val, y_type_test, le_type, "Type", "03b_type_split.png"),
    (
        y_algo_train,
        y_algo_val,
        y_algo_test,
        le_algo,
        "Algorithm",
        "03c_algorithm_split.png",
    ),
]

for y_tr, y_val_, y_te, le, name, filename in datasets:
    plt.figure(figsize=(6, 5))
    tr_cnt = pd.Series(y_tr).value_counts().sort_index()
    val_cnt = pd.Series(y_val_).value_counts().sort_index()
    te_cnt = pd.Series(y_te).value_counts().sort_index()
    x = np.arange(len(tr_cnt))

    plt.bar(
        x - 0.3,
        tr_cnt.values,
        0.3,
        label="Train",
        color="#3498db",
        edgecolor="black",
    )
    plt.bar(
        x,
        val_cnt.values,
        0.3,
        label="Validation",
        color="orange",
        edgecolor="black",
    )
    plt.bar(
        x + 0.3,
        te_cnt.values,
        0.3,
        label="Test",
        color="#e74c3c",
        edgecolor="black",
    )

    plt.title(f"{name} Class Distribution Across Splits", fontweight="bold")
    plt.ylabel("Count")
    plt.legend()
    plt.grid(axis="y", alpha=0.3)

    if len(tr_cnt) <= 10:
        plt.xticks(x, le.classes_, rotation=45, ha="right", fontsize=8)
    else:
        plt.xticks(x[::5], [f"C{i}" for i in x[::5]])

    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()

print("✓ Saved 03a to 03c.")

# =============================================================================
# MODEL TRAINING
# =============================================================================
print("\n" + "=" * 80)
print("MODEL TRAINING (FIXED & ROBUST)")
print("=" * 80)

n_classes_algo = len(le_algo.classes_)
n_classes_cat = len(le_cat.classes_)
n_classes_type = len(le_type.classes_)

# -----------------------------------------------------------------------------
# Direct Model (Algorithm)
# -----------------------------------------------------------------------------
print("\n[1/4] Training Direct Model...")
direct_model = XGBClassifier(
    objective="multi:softprob",
    num_class=n_classes_algo,
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    tree_method="hist",
    n_jobs=-1,
    early_stopping_rounds=50,
)

direct_model.fit(X_train, y_algo_train, eval_set=[(X_val, y_algo_val)], verbose=False)
direct_pred = direct_model.predict(X_test)
direct_acc = accuracy_score(y_algo_test, direct_pred)
direct_f1 = f1_score(y_algo_test, direct_pred, average="weighted")
print(f"✓ Direct: Acc={direct_acc*100:.2f}%, F1={direct_f1*100:.2f}%")

print("\n📋 Direct Model Classification Report:")
print(
    classification_report(
        y_algo_test,
        direct_pred,
        labels=np.arange(len(le_algo.classes_)), 
        target_names=le_algo.classes_,
        digits=3,
        zero_division=0,
    )
)

# -----------------------------------------------------------------------------
# Category Model (Level 1)
# -----------------------------------------------------------------------------
print("\n[2/4] Training Category Model...")
cat_model = XGBClassifier(
    objective="multi:softprob",
    num_class=n_classes_cat,
    n_estimators=400,
    max_depth=7,
    learning_rate=0.06,
    subsample=0.85,
    colsample_bytree=0.85,
    min_child_weight=2,
    gamma=0.05,
    reg_alpha=0.05,
    reg_lambda=0.5,
    random_state=42,
    tree_method="hist",
    n_jobs=-1,
    early_stopping_rounds=30,
)

cat_model.fit(X_train, y_cat_train, eval_set=[(X_val, y_cat_val)], verbose=False)
cat_pred_train = cat_model.predict(X_train)
cat_pred_val = cat_model.predict(X_val)
cat_pred_test = cat_model.predict(X_test)
cat_acc = accuracy_score(y_cat_test, cat_pred_test)
cat_f1 = f1_score(y_cat_test, cat_pred_test, average="weighted")
print(f"✓ Category: Acc={cat_acc*100:.2f}%, F1={cat_f1*100:.2f}%")

print("\n📋 Category Model Classification Report:")
print(
    classification_report(
        y_cat_test,
        cat_pred_test,
        labels=np.arange(len(le_cat.classes_)),
        target_names=le_cat.classes_,
        digits=3,
        zero_division=0,
    )
)

# -----------------------------------------------------------------------------
# Type Model (Level 2)
# -----------------------------------------------------------------------------
print("\n[3/4] Training Type Model...")
X_with_cat_train = X_train.copy()
X_with_cat_train["L1_cat_pred"] = cat_pred_train
X_with_cat_val = X_val.copy()
X_with_cat_val["L1_cat_pred"] = cat_pred_val
X_with_cat_test = X_test.copy()
X_with_cat_test["L1_cat_pred"] = cat_pred_test

type_model = XGBClassifier(
    objective="multi:softprob",
    num_class=n_classes_type,
    n_estimators=400,
    max_depth=7,
    learning_rate=0.06,
    subsample=0.85,
    colsample_bytree=0.85,
    min_child_weight=2,
    gamma=0.05,
    reg_alpha=0.05,
    reg_lambda=0.5,
    random_state=42,
    tree_method="hist",
    n_jobs=-1,
    early_stopping_rounds=30,
)

type_model.fit(
    X_with_cat_train, y_type_train, eval_set=[(X_with_cat_val, y_type_val)], verbose=False
)
type_pred_train = type_model.predict(X_with_cat_train)
type_pred_val = type_model.predict(X_with_cat_val)
type_pred_test = type_model.predict(X_with_cat_test)
type_acc = accuracy_score(y_type_test, type_pred_test)
type_f1 = f1_score(y_type_test, type_pred_test, average="weighted")
print(f"✓ Type: Acc={type_acc*100:.2f}%, F1={type_f1*100:.2f}%")

print("\n📋 Type Model Classification Report:")
print(
    classification_report(
        y_type_test,
        type_pred_test,
        labels=np.arange(len(le_type.classes_)), 
        target_names=le_type.classes_,
        digits=3,
        zero_division=0,
    )
)

# -----------------------------------------------------------------------------
# Hierarchical Model (Level 3 - Algorithm)
# -----------------------------------------------------------------------------
print("\n[4/4] Training Hierarchical Model...")
X_with_both_train = X_train.copy()
X_with_both_train["L1_cat_pred"] = cat_pred_train
X_with_both_train["L2_type_pred"] = type_pred_train

X_with_both_val = X_val.copy()
X_with_both_val["L1_cat_pred"] = cat_pred_val
X_with_both_val["L2_type_pred"] = type_pred_val

X_with_both_test = X_test.copy()
X_with_both_test["L1_cat_pred"] = cat_pred_test
X_with_both_test["L2_type_pred"] = type_pred_test

hier_model = XGBClassifier(
    objective="multi:softprob",
    num_class=n_classes_algo,
    n_estimators=500,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=3,
    gamma=0.1,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    tree_method="hist",
    n_jobs=-1,
    early_stopping_rounds=50,
)

hier_model.fit(
    X_with_both_train,
    y_algo_train,
    eval_set=[(X_with_both_val, y_algo_val)],
    verbose=False,
)
hier_pred = hier_model.predict(X_with_both_test)
hier_acc = accuracy_score(y_algo_test, hier_pred)
hier_f1 = f1_score(y_algo_test, hier_pred, average="weighted")
print(f"✓ Hierarchical: Acc={hier_acc*100:.2f}%, F1={hier_f1*100:.2f}%")

print("\n📋 Hierarchical Model Classification Report:")
print(
    classification_report(
        y_algo_test,
        hier_pred,
        labels=np.arange(len(le_algo.classes_)),   
        target_names=le_algo.classes_,
        digits=3,
        zero_division=0,
    )
)

# -----------------------------------------------------------------------------
# Ensemble
# -----------------------------------------------------------------------------
print("\n[ENSEMBLE] Creating weighted ensemble...")

# Direct model expects original X features
X_test_direct_ready = X_test.reindex(columns=direct_model.feature_names_in_)

ensemble_pred = []
for i in range(len(y_algo_test)):
    d_prob = direct_model.predict_proba(X_test_direct_ready.iloc[[i]])[0]
    h_prob = hier_model.predict_proba(X_with_both_test.iloc[[i]])[0]
    combined = (direct_acc * d_prob + hier_acc * h_prob) / (direct_acc + hier_acc)
    ensemble_pred.append(np.argmax(combined))

ensemble_pred = np.array(ensemble_pred)
ensemble_acc = accuracy_score(y_algo_test, ensemble_pred)
ensemble_f1 = f1_score(y_algo_test, ensemble_pred, average="weighted")
print(f"✓ Ensemble: Acc={ensemble_acc*100:.2f}%, F1={ensemble_f1*100:.2f}%")

print("\n📋 Ensemble Model Classification Report:")
print(
    classification_report(
        y_algo_test,
        ensemble_pred,
        labels=np.arange(len(le_algo.classes_)), 
        target_names=le_algo.classes_,
        digits=3,
        zero_division=0,
    )
)

# =============================================================================
# VISUALIZATION 4: Model Comparison
# =============================================================================
print("\n📈 Creating Visualization 4: Model Comparison (Separated plots)...")

models = ["Direct", "Hierarchical", "Ensemble"]
accs = [direct_acc * 100, hier_acc * 100, ensemble_acc * 100]
f1s = [direct_f1 * 100, hier_f1 * 100, ensemble_f1 * 100]
colors = ["#3498db", "#e74c3c", "#2ecc71"]

# Accuracy comparison
plt.figure(figsize=(7, 6))
bars = plt.bar(models, accs, color=colors, edgecolor="black", alpha=0.8)
plt.title("Accuracy Comparison (Algorithm Level)", fontweight="bold", fontsize=12)
plt.ylabel("Accuracy (%)", fontweight="bold")
plt.ylim([min(accs) - 5, 100])
plt.grid(axis="y", alpha=0.3)
for bar, acc in zip(bars, accs):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{acc:.2f}%",
        ha="center",
        fontweight="bold",
    )
plt.tight_layout()
plt.savefig("04a_accuracy_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

# F1-Score comparison
plt.figure(figsize=(7, 6))
bars = plt.bar(models, f1s, color=colors, edgecolor="black", alpha=0.8)
plt.title("F1-Score Comparison (Algorithm Level)", fontweight="bold", fontsize=12)
plt.ylabel("F1-Score (%)", fontweight="bold")
plt.ylim([min(f1s) - 5, 100])
plt.grid(axis="y", alpha=0.3)
for bar, f1_val in zip(bars, f1s):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{f1_val:.2f}%",
        ha="center",
        fontweight="bold",
    )
plt.tight_layout()
plt.savefig("04b_f1_score_comparison.png", dpi=300, bbox_inches="tight")
plt.close()

# Hierarchical cascade performance
plt.figure(figsize=(8, 6))
cascade = ["Category", "Type", "Algorithm"]
cascade_acc = [cat_acc * 100, type_acc * 100, hier_acc * 100]
cascade_f1 = [cat_f1 * 100, type_f1 * 100, hier_f1 * 100]
x = np.arange(len(cascade))
plt.bar(x - 0.2, cascade_acc, 0.4, label="Accuracy", color="skyblue", edgecolor="black")
plt.bar(
    x + 0.2,
    cascade_f1,
    0.4,
    label="F1-Score",
    color="lightcoral",
    edgecolor="black",
)
plt.xticks(x, cascade)
plt.title("Hierarchical Cascade Performance", fontweight="bold", fontsize=12)
plt.ylabel("Score (%)", fontweight="bold")
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.ylim([80, 100])
plt.tight_layout()
plt.savefig("04c_hierarchical_cascade_performance.png", dpi=300, bbox_inches="tight")
plt.close()

# Feature importance (top 15)
plt.figure(figsize=(8, 8))
feat_imp = (
    pd.Series(hier_model.feature_importances_, index=X_with_both_train.columns)
    .sort_values(ascending=False)
    .head(15)
)
plt.barh(
    range(len(feat_imp)),
    feat_imp.values,
    color=plt.cm.viridis(np.linspace(0, 1, len(feat_imp))),
    edgecolor="black",
    alpha=0.8,
)
plt.yticks(range(len(feat_imp)), [f[:20] for f in feat_imp.index], fontsize=8)
plt.title("Top 15 Feature Importances (Hierarchical Model)", fontweight="bold", fontsize=12)
plt.xlabel("Importance", fontweight="bold")
plt.grid(axis="x", alpha=0.3)
plt.tight_layout()
plt.savefig("04d_feature_importance.png", dpi=300, bbox_inches="tight")
plt.close()

print("✓ Saved 04a to 04d.")

# =============================================================================
# VISUALIZATION 5: Per-Class F1-Score
# =============================================================================
print("\n📈 Creating Visualization 5: Per-Class F1-Score Comparison...")

direct_f1_per_class = f1_score(y_algo_test, direct_pred, average=None, zero_division=0)
hier_f1_per_class = f1_score(y_algo_test, hier_pred, average=None, zero_division=0)
ensemble_f1_per_class = f1_score(y_algo_test, ensemble_pred, average=None, zero_division=0)

plt.figure(figsize=(18, 10))
x = np.arange(len(le_algo.classes_))
width = 0.25

plt.bar(
    x - width,
    direct_f1_per_class,
    width,
    label="Direct",
    color="#3498db",
    alpha=0.8,
    edgecolor="black",
)
plt.bar(
    x,
    hier_f1_per_class,
    width,
    label="Hierarchical",
    color="#e74c3c",
    alpha=0.8,
    edgecolor="black",
)
plt.bar(
    x + width,
    ensemble_f1_per_class,
    width,
    label="Ensemble",
    color="#2ecc71",
    alpha=0.8,
    edgecolor="black",
)

plt.xlabel("Algorithm", fontweight="bold", fontsize=12)
plt.ylabel("F1-Score", fontweight="bold", fontsize=12)
plt.title(
    "Per-Algorithm F1-Score Comparison Across Models",
    fontweight="bold",
    fontsize=14,
    pad=15,
)
plt.xticks(x, le_algo.classes_, rotation=90, ha="right", fontsize=8)
plt.legend(fontsize=11)
plt.grid(axis="y", alpha=0.3)
plt.ylim([0, 1.05])

plt.tight_layout()
plt.savefig("10_per_class_f1_comparison.png", dpi=300, bbox_inches="tight")
plt.close()
print("✓ Saved: 10_per_class_f1_comparison.png")

# =============================================================================
# CONFUSION MATRICES
# =============================================================================
def plot_confusion_matrix(y_true, y_pred, le, title, filename):
    cm = confusion_matrix(y_true, y_pred)

    if len(le.classes_) <= 10:
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm,
            annot=True,
            fmt="d",
            cmap="YlGnBu",
            xticklabels=le.classes_,
            yticklabels=le.classes_,
            cbar_kws={"label": "Count"},
            linewidths=0.5,
        )
        plt.xticks(rotation=45, ha="right", fontsize=9)
        plt.yticks(rotation=0, fontsize=9)
        plt.xlabel("Predicted", fontsize=12, fontweight="bold")
        plt.ylabel("True", fontsize=12, fontweight="bold")
    else:
        plt.figure(figsize=(16, 14))
        sns.heatmap(cm, annot=False, cmap="YlGnBu", cbar_kws={"label": "Count"})
        plt.xlabel("Predicted Index", fontsize=12, fontweight="bold")
        plt.ylabel("True Index", fontsize=12, fontweight="bold")

    plt.title(title, fontsize=14, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"✓ Saved: {filename}")


print("\n📈 Creating Confusion Matrices (Separated plots)...")

plot_confusion_matrix(
    y_cat_test,
    cat_pred_test,
    le_cat,
    f"Category Model - Acc: {cat_acc*100:.2f}%",
    "05_cm_category.png",
)
plot_confusion_matrix(
    y_type_test,
    type_pred_test,
    le_type,
    f"Type Model - Acc: {type_acc*100:.2f}%",
    "06_cm_type.png",
)
plot_confusion_matrix(
    y_algo_test,
    direct_pred,
    le_algo,
    f"Direct Model - Acc: {direct_acc*100:.2f}%",
    "07_cm_direct.png",
)
plot_confusion_matrix(
    y_algo_test,
    hier_pred,
    le_algo,
    f"Hierarchical Model - Acc: {hier_acc*100:.2f}%",
    "08_cm_hierarchical.png",
)
plot_confusion_matrix(
    y_algo_test,
    ensemble_pred,
    le_algo,
    f"Ensemble Model - Acc: {ensemble_acc*100:.2f}%",
    "09_cm_ensemble.png",
)

# =============================================================================
# SAVE MODELS
# =============================================================================
print("\n💾 Saving models...")
joblib.dump(direct_model, "direct_model.joblib")
joblib.dump(cat_model, "cat_model.joblib")
joblib.dump(type_model, "type_model.joblib")
joblib.dump(hier_model, "hier_model.joblib")
joblib.dump(scaler, "scaler.joblib")
joblib.dump(le_cat, "le_cat.joblib")
joblib.dump(le_type, "le_type.joblib")
joblib.dump(le_algo, "le_algo.joblib")
joblib.dump({"direct_acc": direct_acc, "hier_acc": hier_acc}, "weights.joblib")

print("\n" + "=" * 80)
print("✨ TRAINING COMPLETE! (FIXED & ROBUST EVALUATION)")
print("=" * 80)
print(f"\n🏆 Best Model: Ensemble ({ensemble_acc*100:.2f}% accuracy)")
print("\n📊 Final Results (Robustly Measured):")
print(f"  Direct:       {direct_acc*100:.2f}% | F1: {direct_f1*100:.2f}%")
print(f"  Hierarchical: {hier_acc*100:.2f}% | F1: {hier_f1*100:.2f}%")
print(f"  Ensemble:     {ensemble_acc*100:.2f}% | F1: {ensemble_f1*100:.2f}%")
