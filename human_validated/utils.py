import numpy as np

def observed_agreement_matrix(annotations):
        #compute scotts pi:
    # categories = np.unique([category for sublist in annotations for category in sublist])
    # n_categories = len(categories)
    # observed_agreement_matrix = np.zeros((n_categories, n_categories), dtype=int)
    
    # for item_annotations in annotations:
    # # Compare annotations for each pair of annotators
    #     for i in range(len(item_annotations)):
    #         for j in range(i + 1, len(item_annotations)):
    #             annotator1_idx = np.where(categories == item_annotations[i])[0][0]
    #             annotator2_idx = np.where(categories == item_annotations[j])[0][0]
    #             observed_agreement_matrix[annotator1_idx, annotator2_idx] += 1
    #             observed_agreement_matrix[annotator2_idx, annotator1_idx] += 1  # Symmetric matrix
    n_items = len(annotations)
    n_raters = len(annotations[0])
    unique_categories = np.unique(annotations)
    n_categories = len(unique_categories)
    
    category_to_index = {category: idx for idx, category in enumerate(unique_categories)}
    
    agreement_matrix = np.zeros((n_categories, n_categories), dtype=int)
    
    for item_annotations in annotations:
        for i in range(n_raters):
            for j in range(i + 1, n_raters):
                category_i = category_to_index[item_annotations[i]]
                category_j = category_to_index[item_annotations[j]]
                agreement_matrix[category_i, category_j] += 1
                agreement_matrix[category_j, category_i] += 1
    
    return agreement_matrix

def expected_agreement_matrix(annotations):
    n_items = len(annotations)
    n_raters = len(annotations[0])
    unique_categories = np.unique(annotations)
    n_categories = len(unique_categories)
    
    category_to_index = {category: idx for idx, category in enumerate(unique_categories)}
    
    expected_matrix = np.zeros((n_categories, n_categories), dtype=int)
    
    for item_annotations in annotations:
        for category_i in unique_categories:
            for category_j in unique_categories:
                p_i = np.sum(item_annotations == category_i) / n_raters
                p_j = np.sum(item_annotations == category_j) / n_raters
                index_i = category_to_index[category_i]
                index_j = category_to_index[category_j]
                expected_matrix[index_i, index_j] += p_i * p_j
                expected_matrix[index_j, index_i] += p_i * p_j
                
    return expected_matrix

def observed_disagreement_matrix(annotations):
    agreement_matrix = observed_agreement_matrix(annotations)
    n_categories = agreement_matrix.shape[0]
    n_total = np.sum(agreement_matrix)
    
    disagreement_matrix = np.zeros((n_categories, n_categories), dtype=int)
    
    for i in range(n_categories):
        for j in range(i + 1, n_categories):
            disagreement_matrix[i, j] = n_total - agreement_matrix[i, j]
            disagreement_matrix[j, i] = n_total - agreement_matrix[j, i]
    
    return disagreement_matrix

def expected_disagreement_matrix(annotations):
    expected_matrix = expected_agreement_matrix(annotations)
    n_categories = expected_matrix.shape[0]
    n_total = np.sum(expected_matrix)
    
    disagreement_matrix = np.zeros((n_categories, n_categories), dtype=int)
    
    for i in range(n_categories):
        for j in range(i + 1, n_categories):
            disagreement_matrix[i, j] = n_total - expected_matrix[i, j]
            disagreement_matrix[j, i] = n_total - expected_matrix[j, i]
    
    return disagreement_matrix

def coincidence_matrix(annotations):
    unique_categories = np.unique(annotations)
    category_to_index = {category: idx for idx, category in enumerate(unique_categories)}
    n_categories = len(unique_categories)
    
    coincidence_matrix = np.zeros((n_categories, n_categories), dtype=int)
    
    for item_annotations in annotations:
        for i in range(len(item_annotations)):
            for j in range(i + 1, len(item_annotations)):
                category_i = category_to_index[item_annotations[i]]
                category_j = category_to_index[item_annotations[j]]
                coincidence_matrix[category_i, category_j] += 1
                coincidence_matrix[category_j, category_i] += 1
    
    return coincidence_matrix


# Example usage:
annotations = [
    ['category1', 'category2', 'category1'],
    ['category2', 'category2', 'category1'],
    ['category1', 'category2', 'category1'],
    # Add more annotations as needed
]

observed_disagreement = observed_disagreement_matrix(annotations)
expected_disagreement = expected_disagreement_matrix(annotations)

print("Observed Disagreement Matrix:")
print(observed_disagreement)
print("\nExpected Disagreement Matrix:")
print(expected_disagreement)

