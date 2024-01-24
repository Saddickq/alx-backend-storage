#!/usr/bin/env python3
"""a Python function that lists all documents in a collection"""
import pymongo


def list_all(mongo_collection):
    """Main method"""
    return list(mongo_collection.find())
