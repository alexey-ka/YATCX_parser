import numpy as np

"""
Additional functions for the TCX Parser
"""


def elem2dict(node):
    """
    Convert an lxml.etree node tree into a dict.
    https://gist.github.com/jacobian/795571
    """
    result = {}

    for element in node.iterchildren():
        # Remove namespace prefix
        key = element.tag.split('}')[1] if '}' in element.tag else element.tag

        # Process element as tree element if the inner XML contains non-whitespace content
        if element.text and element.text.strip():
            value = element.text
        else:
            value = elem2dict(element)
        if key in result:

            if type(result[key]) is list:
                result[key].append(value)
            else:
                tempvalue = result[key].copy()
                result[key] = [tempvalue, value]
        else:
            result[key] = value
    return result


def interpolate_nans(res):
    res = np.array(res)
    nans, x = np.isnan(res), lambda x: x.nonzero()[0]
    if sum(nans) < len(res):
        res[nans] = np.interp(x(nans), x(~nans), res[~nans])
    return list(res)


def calculate_grade_arcsin(grades):
    """ Slope in a radians"""
    rad = 15.915
    grades[0] = grades[1]
    return np.arcsin(grades) * rad
