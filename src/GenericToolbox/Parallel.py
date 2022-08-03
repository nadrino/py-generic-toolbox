#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Globals
nbThreads = 1


def runParallel(function_, listToProcess_):
    from tqdm import tqdm
    from multiprocessing.dummy import Pool as ThreadPool
    from multiprocessing import cpu_count

    global nbThreads

    with ThreadPool(processes=nbThreads) as pool:
        with tqdm(total=len(listToProcess_)) as progress_bar:
            for i, _ in enumerate(pool.imap_unordered(function_, listToProcess_)):
                progress_bar.update()