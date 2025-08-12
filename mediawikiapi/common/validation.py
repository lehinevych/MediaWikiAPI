"""
Parameter validation utilities for the MediaWikiAPI package.

This module provides common parameter validation functions used across
both synchronous and asynchronous implementations.
"""

from decimal import Decimal, InvalidOperation
from typing import Any, Optional, Union


def validate_title_or_pageid(title: Optional[Any] = None, pageid: Optional[Any] = None) -> None:
    """
    Validate that either a title or pageid is provided, but not both.
    
    Args:
        title: Title of the Wikipedia page
        pageid: Page ID of the Wikipedia page
        
    Raises:
        ValueError: If both are provided or neither is provided
    """
    if title is None and pageid is None:
        raise ValueError("Either a title or a pageid must be specified")
    if title is not None and pageid is not None:
        raise ValueError("Please specify only a title or only a pageid, not both")


def validate_geosearch_params(
    latitude: Any, longitude: Any, radius: int, results: int
) -> None:
    """
    Validate geosearch parameters.
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        radius: Search radius in meters (must be between 10 and 10000)
        results: Maximum number of results (must be positive)
        
    Raises:
        ValueError: If parameters are invalid
        InvalidOperation: If coordinates can't be converted to Decimal
    """
    try:
        lat_dec = Decimal(latitude)
        lon_dec = Decimal(longitude)
    except (InvalidOperation, ValueError, TypeError):
        raise ValueError("Latitude and longitude must be valid numbers")
        
    if not (-90 <= float(lat_dec) <= 90):
        raise ValueError("Latitude must be between -90 and 90")
        
    if not (-180 <= float(lon_dec) <= 180):
        raise ValueError("Longitude must be between -180 and 180")
        
    if not (10 <= radius <= 10000):
        raise ValueError("Radius must be between 10 and 10000 meters")
        
    if results <= 0:
        raise ValueError("Number of results must be positive")


def validate_search_params(query: str, results: int) -> None:
    """
    Validate search parameters.
    
    Args:
        query: Search query string
        results: Maximum number of results
        
    Raises:
        ValueError: If parameters are invalid
    """
    if not query:
        raise ValueError("Query cannot be empty")
        
    if results <= 0:
        raise ValueError("Number of results must be positive")


def validate_limit(limit: Union[int, str], max_value: int = 500) -> None:
    """
    Validate a limit parameter.
    
    Args:
        limit: The limit value, either an integer or "max"/"max_value"
        max_value: The maximum allowed value for numerical limits
        
    Raises:
        ValueError: If the limit is invalid
    """
    if isinstance(limit, str):
        if limit.lower() not in ["max", "max_value"]:
            raise ValueError(
                f"String limit must be 'max' or 'max_value', got '{limit}'"
            )
    elif isinstance(limit, int):
        if limit <= 0:
            raise ValueError("Limit must be positive")
        if limit > max_value:
            raise ValueError(f"Limit cannot exceed {max_value}")
    else:
        raise ValueError(f"Limit must be an integer or 'max'/'max_value', got {type(limit)}")


def validate_category_params(
    title: Optional[str] = None, 
    pageid: Optional[int] = None, 
    cmtype: str = "page"
) -> None:
    """
    Validate category member parameters.
    
    Args:
        title: Category title
        pageid: Category page ID
        cmtype: Type of category members to retrieve
        
    Raises:
        ValueError: If parameters are invalid
    """
    if title is not None and pageid is not None:
        raise ValueError(
            "Please specify only a category title or only a pageid, not both"
        )
        
    if title is None and pageid is None:
        raise ValueError("Either a category title or a pageid must be specified")
        
    if cmtype not in ["page", "subcat", "file"]:
        raise ValueError(
            "Category member type must be one of: 'page', 'subcat', or 'file'"
        )


def validate_sentences_and_chars(sentences: Optional[int], chars: Optional[int]) -> None:
    """
    Validate that sentences and chars parameters are valid.
    
    Args:
        sentences: Number of sentences to retrieve
        chars: Number of characters to retrieve
        
    Raises:
        ValueError: If parameters are invalid
    """
    if sentences is not None and sentences < 0:
        raise ValueError("Number of sentences must be non-negative")
        
    if chars is not None and chars < 0:
        raise ValueError("Number of characters must be non-negative")
        
    if sentences is not None and chars is not None and sentences > 0 and chars > 0:
        raise ValueError("Specify only one of sentences or chars, not both")
