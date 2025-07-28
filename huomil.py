
# huomil.py - High Utility Occupancy Pattern Mining (HUOMIL)

def compute_utility(item, qty, profit_table):
    return qty * profit_table.get(item, 0)

def build_indexed_list(transactions, profit_table):
    index = {}
    for tx in transactions:
        tid = tx['id']
        for item, qty in tx['items'].items():
            utility = compute_utility(item, qty, profit_table)
            if item not in index:
                index[item] = []
            index[item].append({'tid': tid, 'qty': qty, 'util': utility})
    return index

def prune_items(index, min_util, min_occup, total_tx):
    result = {}
    for item, entries in index.items():
        total_util = sum(e['util'] for e in entries)
        occup = len(entries) / total_tx
        if total_util >= min_util and occup >= min_occup:
            result[item] = {
                'total_utility': total_util,
                'occupancy': occup,
                'entries': entries
            }
    return result

def mine_high_utility_occupancy_patterns(transactions, profit_table, min_util=10, min_occup=0.3):
    total_tx = len(transactions)
    indexed_list = build_indexed_list(transactions, profit_table)
    pruned = prune_items(indexed_list, min_util, min_occup, total_tx)
    return [(item, data['total_utility'], round(data['occupancy'], 2)) for item, data in pruned.items()]
