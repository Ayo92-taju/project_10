from werkzeug.security import generate_password_hash, check_password_hash

def calculate_grade(total_score):
    if total_score >= 70:
        return 'A', 5
    elif total_score >= 60:
        return 'B', 4
    elif total_score >= 50:
        return 'C', 3
    elif total_score >= 45:
        return 'D', 2
    elif total_score >= 40:
        return 'E', 1
    else:
        return 'F', 0

def calculate_gpa(results):
    total_weight = sum(r['unit_weight'] for r in results)
    if total_weight == 0:
        return 0.0
    total_points = sum(r['grade_point'] * r['unit_weight'] for r in results)
    return round(total_points / total_weight, 2)

def hash_password(password):
    return generate_password_hash(password)

def verify_password(password, hashed):
    return check_password_hash(hashed, password)