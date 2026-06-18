import numpy as np

def rarefied_richness(
    taxa,
    sample_size,
    n_iter=1000
):
    taxa = np.array(taxa)

    richness_values = []

    for _ in range(n_iter):

        sample = np.random.choice(
            taxa,
            size=sample_size,
            replace=False
        )

        richness_values.append(
            len(set(sample))
        )

    return np.mean(richness_values)