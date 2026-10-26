#!/usr/bin/env python3
"""Abstract lifecycle model, not PHP execution or real memory corruption."""
import json

def simulate(reset):
    state = {'owner_request': 1, 'reference_id': 'request-1-data'}
    live = {'request-1-data': 'temporary data'}
    if reset:
        state['reference_id'] = None
    del live['request-1-data']
    ref = state['reference_id']
    return {'reset_before_release': reset,
            'invariant_ok': ref is None or ref in live,
            'consumer_outcome': 'no stale reference' if ref is None
                                else 'invalid reference detected',
            'real_uaf_or_rce_executed': False}

if __name__ == '__main__':
    print(json.dumps({'scope': 'abstract_state_lifetime_model',
                      'without_reset': simulate(False),
                      'with_reset': simulate(True)}, indent=2))
