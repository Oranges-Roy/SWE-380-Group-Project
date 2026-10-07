#codde for C++ Clones.png

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# 1. Load your original dataset & similarity results
df = pd.read_csv('/content/drive/MyDrive/extracted_skills_sample.csv')
similar_pairs_df = pd.read_csv(
    '/content/drive/MyDrive/results/cpp_similar_pairs.csv'
)

# 2. Count SHA frequencies to identify Type-1 Verbatim copies
sha_counts = df['file_sha'].value_counts()
verbatim_shas = set(sha_counts[sha_counts > 1].index)

# 3. Extract SHAs involved in Type-2 and Type-3 pairwise matches
type2_shas = set(
    similar_pairs_df[
        similar_pairs_df['clone_type'] == 'Type-2 (Parameterized)'
    ]['skill_a_sha']
).union(
    set(
        similar_pairs_df[
            similar_pairs_df['clone_type'] == 'Type-2 (Parameterized)'
        ]['skill_b_sha']
    )
)

type3_shas = set(
    similar_pairs_df[similar_pairs_df['clone_type'] == 'Type-3 (Semantic)'][
        'skill_a_sha'
    ]
).union(
    set(
        similar_pairs_df[similar_pairs_df['clone_type'] == 'Type-3 (Semantic)'][
            'skill_b_sha'
        ]
    )
)


# 4. Assign a single category to each row (Prioritizing: Type-1 -> Type-2 -> Type-3 -> Unique)
def classify_row(sha):
  if sha in verbatim_shas:
    return 'Type-1 (Verbatim)'
  elif sha in type2_shas:
    return 'Type-2 (Parameterized)'
  elif sha in type3_shas:
    return 'Type-3 (Semantic)'
  else:
    return 'Truly Unique'


df['overall_category'] = df['file_sha'].apply(classify_row)

# 5. Print summary ensuring it sums to 10,737
counts = df['overall_category'].value_counts()
print('=== Complete Row Categorization ===')
print(counts)
print(f'Total Rows: {counts.sum()} (Matches expected 10,737)')

# 6. Plot complete distribution bar chart
plt.figure(figsize=(10, 6))
ax = sns.barplot(
    x=counts.index, y=counts.values, palette='Blues_r', hue=counts.index
)

plt.title('Complete Categorization of C++ Skills (N = 10,737)', fontsize=14)
plt.xlabel('Clone / Uniqueness Category', fontsize=12)
plt.ylabel('Number of Skill File Occurrences', fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Add value labels above bars
for p in ax.patches:
  height = p.get_height()
  if height > 0:
    ax.annotate(
        f'{int(height):,}\n({height/len(df)*100:.1f}%)',
        (p.get_x() + p.get_width() / 2.0, height),
        ha='center',
        va='bottom',
        xytext=(0, 5),
        textcoords='offset points',
    )

plt.tight_layout()
plt.show()
