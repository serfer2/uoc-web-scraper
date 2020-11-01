
def full_url(base_url, relative_url):
    if relative_url.startswith('http'):
        return relative_url

    if relative_url[0] != '/':
        relative_url = f'/{relative_url}'

    if not base_url.startswith('http'):
        raise ValueError('base_url shoul start with http')

    start = base_url.find('//') + 2
    if base_url[start:].find('/') != -1:
        return f"{base_url[:base_url.find('/', start)]}{relative_url}"

    return f"{base_url}{relative_url}"


def clean_html(text):
    # Clean HTML text format
    return text.replace('\n', '').replace('\t', '').replace('      ', ' ').replace('     ', ' ').replace('    ', ' ').replace('   ', ' ').replace('  ', ' ').replace('  ', ' ').replace('> <', '><').strip()
