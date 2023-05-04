import numpy as np

def _truncate(w, needed):
    """Truncate window by 1 sample if needed for DFT-even symmetry"""
    if needed:
        return w[:-1]
    else:
        return w
    
def _extend(M, sym):
    """Extend window by 1 sample if needed for DFT-even symmetry"""
    if not sym:
        return M + 1, True
    else:
        return M, False

def general_cosine(M, a, sym=True):
    """
    Generic weighted sum of cosine terms window
    Parameters
    ----------
    M : int
        Number of points in the output window
    a : array_like
        Sequence of weighting coefficients. This uses the convention of being
        centered on the origin, so these will typically all be positive
        numbers, not alternating sign.
    sym : bool, optional
        When True (default), generates a symmetric window, for use in filter
        design.
        When False, generates a periodic window, for use in spectral analysis.
    Returns
    -------
    w : ndarray
        The array of window values.
    """

    M, needs_trunc = _extend(M, sym)

    fac = np.linspace(-np.pi, np.pi, M)
    w = np.zeros(M)
    for k in range(len(a)):
        w += a[k] * np.cos(k * fac)

    return _truncate(w, needs_trunc)

def BlackmanHarris3(M, sym=True):
    """Generate 3 terms Blackman-Harris window function
    Parameters for the window function:
    a0 = 0.42323; 
    a1 = 0.49755; 
    a2 = 0.07922; 
    
    Args:
        M (Number of points): 
    """
    a=[0.42323801, 0.4973406, 0.0782793]
    #a=[0.35875, 0.48829, 0.14128, 0.01168]

    return general_cosine(M, a, sym)