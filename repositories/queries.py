queries = {
    'get_foundation_with_goals_and_actual_amount': '''
        SELECT 
            SUM(d.amount) AS total_amount,
            gc.max_amount AS goal_amount,
            MAX(d.created_at) AS last_donation_date
        FROM foundations f
        LEFT JOIN goals g ON f.id = g.foundation_id
        LEFT JOIN donations d ON g.donation_id = d.id
        LEFT JOIN goal_categories gc ON g.category_id = gc.id
        WHERE 
            f.id = :foundation_id
        GROUP BY
            f.name,
            gc.max_amount
        ORDER BY
            last_donation_date DESC
        LIMIT 3;
    ''',
    'get_donors_by_foundation_id': '''
        SELECT
            d.person_name,
            d.amount
        FROM foundations f
        LEFT JOIN goals g
            ON g.foundation_id = f.id
        LEFT JOIN donations d 
            ON g.donation_id = d.id
        WHERE 
            f.id = :foundation_id
        ORDER BY
            d.created_at DESC
        LIMIT 5
    ''',
}