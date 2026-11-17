"""Sanctions name-match screening for outgoing payments.

A payee name is compared with each watchlist name. A score at or above
SANCTIONS_MATCH_THRESHOLD is a hit, and the payment is held for review by
Financial Crime Compliance. The threshold is set by compliance; see
CONTRIBUTING.md before you change it.
"""

import unicodedata
from difflib import SequenceMatcher

SANCTIONS_MATCH_THRESHOLD = 0.85


def normalise_name(name):
    """Lower case, accents removed, single spaces."""
    plain = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return " ".join(plain.lower().split())


def name_similarity(a, b):
    """A score from 0.0 (nothing alike) to 1.0 (the same name)."""
    return SequenceMatcher(None, normalise_name(a), normalise_name(b)).ratio()


def is_sanctions_hit(score):
    return score >= SANCTIONS_MATCH_THRESHOLD


def best_match(payee, watchlist):
    """The closest watchlist name and its score, as (name, score)."""
    return max(((entry, name_similarity(payee, entry)) for entry in watchlist), key=lambda m: m[1])


def format_review_date(d):
    """The date of a review-queue entry, as an ISO 8601 date (YYYY-MM-DD)."""
    return d.strftime("%d/%m/%Y")
