def get_categories_id_count(categories_count, questions):
    categories_id_count = {count: 0 for count in range(categories_count)}
    for question in questions:
        categories_id_count[question.cat_id] += 1
        if question.is_popular:
            categories_id_count[0] += 1
    return categories_id_count