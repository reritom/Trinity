import random

def graph_maker(name_min, name_max, name_chance, node_min, node_max, node_chance, spread, topology):
    '''
        Relay name range (i.e 1-100 or 101-200), this allows..
        ..for bridging of seperate graphs

        Spread (between 0-1) to do with cluster density

        Chance determines how many relays within the range will be made

    '''

    def roll(chance):
        '''
            Roll the dice
        '''
        chance_num = random.randint(1,101)
        return chance*100 <= chance_num

    topologies = ['cyclic', 'web', 'star', 'branch', 'all']
    if topology not in topologies:
        return False

    Graph = dict()

    num_of_relays = 0

    print(str(name_min) + ' ' + str(name_max))

    for potential_relay in range(name_min, name_max):
        if roll(name_chance):
            Graph[potential_relay] = list()
            # Add to graph, then run same process for neighbours
            # Must be at least one neighbour

    if topology == 'cyclic':
        # Have last relays be neighbours with first relays
        pass
    elif topology == 'branch':
        # Have last not overlap with first
        pass
    elif topology == 'web':
        # Have everything overlap slightly with everything
        pass
    elif topology == 'star':
        # One node which routes everything
        pass
    elif topology == 'all':
        # Have everything connected to everything (cascade)
        pass

    print(num_of_relays)

    return Graph

if __name__ == '__main__':
    graph_maker(1,100,0.5,1,6,0.5,0.8, 'tree')
