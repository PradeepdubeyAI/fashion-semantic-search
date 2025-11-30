from app.services.processor import parse_query_filters

QUERIES = [
    "navy long sleeve floor-length dress",
    "dark blue maxi",
    "red ballgown",  # typo
    "navy long sleev",  # typo
    "pink dress",
    "white fit and flare",
]


def main():
    for q in QUERIES:
        filters = parse_query_filters(q)
        print(f"Query: {q}\nFilters: {filters}\n")


if __name__ == "__main__":
    main()
