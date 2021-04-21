import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    #print(crawl("corpus0"))
    #print(transition_model(crawl("corpus0"), "2.html", DAMPING))
    #print(sample_pagerank(crawl("corpus0"), DAMPING, 1000))
    #print(iterate_pagerank(crawl("corpus0"), DAMPING))
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


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if corpus[page] == 0:
        return 1 / len(corpus[page])
    probabilities = {}
    for key in corpus[page]:
        if key != page:
            probabilities[key] = (damping_factor / len(corpus[page])) + ((1 - damping_factor) / len(corpus.keys()))
            #probabilities[key] = round((damping_factor / len(corpus[page])) + ((1 - damping_factor) / len(corpus.keys())), 3)
    for p in corpus.keys():
        if p not in probabilities.keys():
            probabilities[p] = (1 - damping_factor) * 1 / len(corpus.keys())
            #probabilities[p] = round((1 - damping_factor) * 1 / len(corpus.keys()), 3)
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    keys = []
    rank = {}
    for key in corpus.keys():
        keys.append(key)
    sample = keys[random.randrange(len(corpus.keys()))]
    for key in corpus.keys():
            if key not in rank.keys():
                rank[key] = 0
    rank[sample] = 1
    for tryies in range(n - 1):
        probabilities = transition_model(corpus, sample, damping_factor)
        values = []
        for key in probabilities.keys():
            for i in range(int(1000 * probabilities[key])):
                values.append(key)
        sample = values[random.randrange(len(values))]
        rank[sample] += 1
    for key in rank.keys():
        rank[key] = rank[key] / n
    return rank      


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank = {}
    newRank = {}
    n = len(corpus.keys())
    for key in corpus.keys():
        rank[key] = 1 / n
    while True:
        changed = False
        for key in rank.keys():
            start = rank[key]
            newRank[key] = (1 - damping_factor) / n
            pages = 0
            for i in rank.keys():
                #if i != key:
                    links = len(corpus[i])
                    if links != 0:
                        if key in corpus[i]:
                            pages += rank[i] / links
                    else:
                        pages += 1 / n
            newRank[key] += damping_factor * pages
        for key in rank.keys():
            if abs(newRank[key] - rank[key]) > 0.001:
                changed = True
            rank[key] = newRank[key]
        if not changed:
            break
    #for key in rank.keys():
    #    rank[key] = round(rank[key], 3)
    return rank

if __name__ == "__main__":
    main()
