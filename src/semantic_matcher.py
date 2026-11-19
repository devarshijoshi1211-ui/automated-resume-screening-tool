from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_similarity(jd, resume):
    jd_embedding = model.encode(jd, convert_to_tensor=True)
    resume_embedding = model.encode(resume, convert_to_tensor=True)

    score = util.cos_sim(jd_embedding, resume_embedding).item()

    return round(score, 4)
