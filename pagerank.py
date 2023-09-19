import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages
#

def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    distribution = dict()
    
    page_links = corpus[page]
    if len(page_links) == 0:
        page_links = set(corpus.keys())
    damping_factor_rate = (1 - damping_factor) / len(corpus.keys())
    #print(damping_factor_rate)
    for page in set(corpus.keys()):
        if page in page_links:
            distribution[page] = (1 / len(page_links)) * damping_factor + damping_factor_rate
        else:
            distribution[page] = damping_factor_rate
    
    #print("distribution:")
    #print(distribution)
    #print()
    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    results = dict()
    for page in corpus:
        results[page] = 0
    i = 1
    choices = list(corpus.keys())
    page = random.choice(choices)
    results[page] = results[page] + 1
    while i < n:
        i += 1
        t = transition_model(corpus, page, damping_factor)
        t_choices = list(t.keys())
        t_weights = list(t.values())
        choice = random.choices(t_choices, weights=t_weights)[0]

        page = choice
        results[page] = results[page] + 1
        

    PageRanks = dict()
    for result in results:
        key = result
        value = results[key]
        PageRanks[key] = value / n
    return PageRanks
    
def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    PageRank = dict()
    for page in pages:
        PageRank[page] = 1 / len(pages)

    converge = True
    i = 0 
    while converge:
        i += 1
        c_PageRank = PageRank.copy()
        #print(f"pages: {pages}")
        for page in pages:
            #print(f"{page}")
            sum = 0
            print(sum)
            for page_s in pages:
                sum += (c_PageRank[page_s]) / len(corpus[page_s])
                print(sum)
            pagerank_p = ((1 - damping_factor) / len(pages)) + (sum * damping_factor)
            PageRank[page] = pagerank_p
            #print(PageRank)
        
        converges = 0
        for page in list(c_PageRank.keys()):
            if (((c_PageRank[page] - PageRank[page]) <= 0.001) and ((c_PageRank[page] - PageRank[page]) >= 0)) or ((PageRank[page] - c_PageRank[page] <= 0.001) and (PageRank[page] - c_PageRank[page] <= 0)):
                print(c_PageRank[page] - PageRank[page])
                converges += 1
                #print(converge)
                #continue
        if converges == len(corpus.keys()) and i != 1:
            converge = False
            continue
    return PageRank


if __name__ == "__main__":
    main()
