import multiprocessing as mp


if __name__ == '__main__':
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.starmap(merge_names, product(names, repeat=2))
    print(results)
