from django import template

register = template.Library()

def stars(number):
    full = int(number)
    part = number - full
    if part > 0:
        part = True
        remaining = 9 - full
    else:
        part = False
        remaining = 10 - full

    full = [i for i in range(full)]
    remaining = [i for i in range(remaining)]

    t = template.loader.get_template('movies/partials/stars.html')
    return t.render(template.Context({'full': full, 'part': part, 'remaining': remaining}))
register.filter('stars', stars)

