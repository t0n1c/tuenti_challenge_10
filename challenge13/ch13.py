import fileinput
from itertools import cycle
from itertools import count


def perimeter_papers(layer, dimensions, tower_height):
    n, m = dimensions
    if layer == tower_height:
        return n * m * layer  # my tower was hollow! (on Mon May 4 08:10:01 CEST 2020)
    if n == m:
        if n == 1:
            return layer
        return 4 * (n - 1) * layer
    else:
        assert abs(n - m) == 1
        return 2 * (n + m - 2) * layer


def dimension_delta(tower_height):
    """This function is a slightly different version of the four times
     triangular number (https://oeis.org/A046092). Our sequence starts in
     3. It basically computes "how fast" the toilet paper available will
     decrease as the fortress is being build for different tower sizes. 
     So this assumes we vary the dimension of the tower while keeping the height
     constant!."""
    return 2 * (tower_height ** 2 - tower_height)


def inc_layers(layer):
    yield layer
    while True:
        for add_layer in cycle([-2, 1]):
            layer += add_layer
            if add_layer == 1 and layer == 2:
                yield layer
                raise StopIteration
            yield layer


def inc_dimensions(dimensions, inc=2):
    yield dimensions
    while True:
        dimensions = tuple(dim + 2 for dim in dimensions)
        yield dimensions


def used_papers(tower_height, tower_size, papers_available):
    """Try to "build" a fortress if possible and return the number of toilet
    paper packs used for building it."""

    total_used = 0
    dim_layers = zip(inc_dimensions(tower_size), inc_layers(tower_height))
    for dimensions, layer in dim_layers:
        requested_papers = perimeter_papers(layer, dimensions, tower_height)
        #layer_count[layer] += requested_papers // layer
        papers_available -= requested_papers
        if papers_available < 0:
            return None
        total_used += requested_papers
        # print(dimensions, layer, total_used)
    # print(sorted(layer_count.items(), key=lambda item: item[0]))
    return total_used


def dim_iterator_test():
    count1 = count(1)
    count2 = count(1)
    prev1, prev2 = next(count1), next(count2)
    yield prev1, prev2
    while True:
        if prev1 == prev2:
            prev1 = next(count1)
        else:
            prev2 = next(count2)
        yield prev1, prev2


def inner_tower_size(n):
    # https://oeis.org/search?q=1%2C2%2C4%2C6%2C9&language=english&go=Search
    if n < 0:
        return 0
    return n**2//4



def max_tower_height(papers_available, start=3):
    # our actual bound is h = 952696, size = (3,3), below that is possible
    # to build a fortress
    min_height, max_height = start, 952695
    if papers_available < 43: # min papers to build the smallest fortress
        return None
    if papers_available < max_height:
        max_height = papers_available
    lower_bound, upper_bound = min_height, max_height
    total = 0
    index_height = lower_bound + (upper_bound - lower_bound) // 2
    while lower_bound <= upper_bound:
        papers = used_papers(index_height, (1, 1), papers_available)
        if papers is None:
            upper_bound = index_height - 1
        else:
            lower_bound = index_height + 1
            if papers > total:
                total = papers
        index_height = lower_bound + (upper_bound - lower_bound) // 2
    delta = dimension_delta(index_height)
    papers = used_papers(index_height, (1, 2), papers_available)
    if papers is not None:
        total = papers
        for i in count():
            inner_papers = inner_tower_size(i) * index_height
            if total + delta <= papers_available:
                if total + delta + inner_papers > papers_available:
                    inner_papers = inner_tower_size(i-1) * index_height
                    break
                else:
                    total += delta
            else:
                inner_papers = inner_tower_size(i-1) * index_height
                break      
        total += inner_papers
    return index_height, total



def upper_bound(max_papers=2**62):
    # 952696, random upper bound 1000000
    #bounds = [bound for bound in [10**p for p in range(1,7)]]
    for height in reversed(range(952696)):
        total = used_papers(height, (1, 1), max_papers)
        if total != None:
            return height


def main():
    lines = fileinput.input()
    _ = next(lines)
    for i,line in enumerate(lines, 1):
        result = max_tower_height(int(line))
        if result is None:
            print(f'Case #{i}: IMPOSSIBLE')
        else:
            height, total = result
            print(f'Case #{i}: {height} {total}')



if __name__ == "__main__":
    main()
        
