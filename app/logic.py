import random
from app.models import Assignment

def assign_variant(user_id, experiment_id, db, variants):
    existing = db.query(Assignment).filter_by(
        user_id=user_id,
        experiment_id=experiment_id
    ).first()

    if existing:
        return existing.variant_id

    total = sum(v.weight for v in variants)
    r = random.randint(1, total)

    upto = 0
    for v in variants:
        if upto + v.weight >= r:
            chosen = v
            break
        upto += v.weight

    assignment = Assignment(
        user_id=user_id,
        experiment_id=experiment_id,
        variant_id=chosen.id
    )

    db.add(assignment)
    db.commit()

    return chosen.id