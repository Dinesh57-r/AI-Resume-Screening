import sys
sys.path.insert(0, '.')
print('Testing imports...')
from utils.parser import clean_text, parse_txt
from utils.extractor import extract_all, extract_keywords_from_jd
from utils.scorer import rank_candidates, get_tier
from utils.visualizer import score_bar_chart, skill_frequency_chart
print('All imports OK!')

# Test with sample data
sample_text = open('sample_resumes/john_smith_data_scientist.txt', encoding='utf-8').read()
candidate = extract_all(sample_text, filename='john_smith.txt')
print("Name:", candidate["name"])
print("Email:", candidate["email"])
print("Phone:", candidate["phone"])
print("Skills count:", len(candidate["skills"]))
print("Top skills:", candidate["skills"][:8])
print("Education:", candidate["education"])
print("Experience:", candidate["experience_years"], "years")

jd = 'Data Scientist with 5+ years in Python, Machine Learning, TensorFlow, NLP, SQL, AWS, Docker, Kubernetes'
kws = extract_keywords_from_jd(jd)
print("JD Keywords:", kws)

ranked = rank_candidates([candidate], jd_text=jd, jd_keywords=kws, required_experience=5)
c = ranked[0]
print("Score:", c["percentage_score"], "%")
print("Matched:", c["matched_skills"])
print("Missing:", c["missing_skills"])
label, color = get_tier(c['composite_score'])
print("Tier:", label)
print("All functions working correctly!")
