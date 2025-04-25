from django.template.defaultfilters import register
    
    
@register.filter
def get_stars(rating):
    stars = ''
    for i in range(rating):
        stars += '⭐'  # Adjust CSS class for star icon
    return stars
    