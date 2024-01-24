#!/usr/bin/env python3
"""a Python function that changes all
topics of a school document based on the name"""


def update_topics(mongo_collection, name, topics):
    """update topic method"""
    mongo_collection.update(
            {"name": name},
            {$set: {"topics": topics}},
            {multi: true}
    )
