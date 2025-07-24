import math


SI_PREFIXES = {
    -24: 'y', -21: 'z', -18: 'a', -15: 'f', -12: 'p', -9: 'n', -6: 'μ', -3: 'm', 0: '',
    3: 'k', 6: 'M', 9: 'G', 12: 'T', 15: 'P', 18: 'E', 21: 'Z', 24: 'Y'
}


def si_scale(value):
    if value == 0:
        return '', 0

    exponent = int(math.floor(math.log10(abs(value)) // 3 * 3))
    exponent = max(min(exponent, 24), -24)
    prefix = SI_PREFIXES[exponent]
    return prefix, 10 ** exponent
