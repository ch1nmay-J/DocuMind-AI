from src.utils import (
    separator,
    similarity_score,
    relevance_label
    )


def format_sources(results, distances, chunks):

    print("\nSources:\n")

    for rank, (index, distance) in enumerate(
        zip(results, distances),
        start=1
    ):
        score = similarity_score(distance)
        label = relevance_label(score)

        print(f"Retrieval Quality : {label}")
        print(f"Distance : {distance:.4f}")
        
        print(f"Result {rank}")
        print(f"File : {chunks[index]['file']}")
        print(f"Page : {chunks[index]['page']}")
        print(f"Chunk: {chunks[index]['chunk_id']}")
        print(separator())
    
    print(f"Total Sources Retrieved: {len(results)}")