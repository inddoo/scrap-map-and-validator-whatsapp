"""
Query normalization utilities
"""

# Mapping kata Indonesia ke berbagai variasi
CATEGORY_VARIATIONS = {
    'kafe': ['cafe', 'kafe', 'coffee shop', 'kedai kopi'],
    'cafe': ['cafe', 'kafe', 'coffee shop', 'kedai kopi'],
    'restoran': ['restoran', 'restaurant', 'rumah makan', 'tempat makan'],
    'restaurant': ['restoran', 'restaurant', 'rumah makan', 'tempat makan'],
    'hotel': ['hotel', 'penginapan', 'hostel'],
    'salon': ['salon', 'barbershop', 'pangkas rambut'],
    'gym': ['gym', 'fitness', 'tempat fitness'],
    'apotek': ['apotek', 'pharmacy', 'apotik'],
    'toko': ['toko', 'shop', 'store'],
    'mall': ['mall', 'pusat perbelanjaan', 'shopping center'],
    'rumah sakit': ['rumah sakit', 'hospital', 'rs'],
    'klinik': ['klinik', 'clinic'],
    'sekolah': ['sekolah', 'school'],
    'universitas': ['universitas', 'university', 'kampus'],
    'masjid': ['masjid', 'mosque'],
    'gereja': ['gereja', 'church'],
    'bank': ['bank', 'atm'],
    'spbu': ['spbu', 'pom bensin', 'gas station'],
}


def normalize_category(category: str) -> str:
    """
    Normalize category to most common variation
    
    Args:
        category: Original category string
        
    Returns:
        Normalized category string
    """
    cat_lower = category.lower().strip()
    
    # Check if category matches any variation
    for main_cat, variations in CATEGORY_VARIATIONS.items():
        if cat_lower in variations:
            # Return the first variation (most common)
            return variations[0]
    
    # If no match, return original
    return category.strip()


def build_search_query(category: str, location: str) -> str:
    """
    Build optimized search query for Google Maps
    
    Args:
        category: Category/type of place
        location: Location string
        
    Returns:
        Optimized search query
    """
    # Normalize category
    norm_cat = normalize_category(category)
    
    # Clean location
    clean_loc = location.strip()
    
    # Build query
    query = f"{norm_cat} {clean_loc}"
    
    return query


def get_alternative_queries(category: str, location: str) -> list:
    """
    Get alternative query variations
    
    Args:
        category: Category/type of place
        location: Location string
        
    Returns:
        List of alternative queries
    """
    cat_lower = category.lower().strip()
    variations = []
    
    # Find all variations for this category
    for main_cat, var_list in CATEGORY_VARIATIONS.items():
        if cat_lower in var_list:
            variations = var_list
            break
    
    # If no variations found, use original
    if not variations:
        variations = [category.strip()]
    
    # Build queries with each variation
    queries = []
    for var in variations[:3]:  # Limit to 3 variations
        queries.append(f"{var} {location.strip()}")
    
    return queries
