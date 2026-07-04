def similarity_score(distance):

    score = 1 / (1 + distance)

    return score * 100

def relevance_label(score):
    if score >= 70:
        return "High"
    
    elif score >= 40:
        return "Medium"
    
    else:
        return "Low"