def reconstruct_url(in_url):
    start = in_url.find('q=') + 2
    end = in_url.find('&')

    clean_url = in_url[start:end]

    splits = clean_url.split('%') # split weird symbols
    splits[1:] = [s[2:] for s in splits[1:]] # remove junk values
    
    url = '='.join(splits[1:]) # join correct arguments
    url = '?'.join([splits[0], url]) # add argument to url

    return url

def create_url(name):
    name = name.lower()
    args = name.split(' ') + ['rate', 'my', 'professor']
    return f"https://www.google.com/search?client=firefox-b-1-d&q={'+'.join(args)}"