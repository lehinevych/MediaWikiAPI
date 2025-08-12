"""
Base class for Wikipedia page implementations.

This module provides the abstract base class that both synchronous and
asynchronous Wikipedia page implementations extend.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, TypeVar, Protocol, Awaitable

from ..exceptions import PageError, RedirectError, ODD_ERROR_MESSAGE

# Type variable for generic specialization
T = TypeVar('T')  # For return type from request methods


class BaseWikipediaPage(ABC):
    """
    Abstract base class for Wikipedia page representations.
    
    This class contains shared functionality between synchronous and asynchronous
    implementations of Wikipedia pages. It defines the interface and common
    operations, leaving I/O-specific operations to derived classes.
    """
    
    def __init__(
        self,
        request: Union[Callable[[Dict[str, Any]], Dict[str, Any]], 
                      Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]],
        title: Optional[str] = None,
        pageid: Optional[int] = None,
        original_title: str = "",
    ) -> None:
        """
        Initialize a Wikipedia page.
        
        Args:
            request: Function to make API requests
            title: Title of the page (mutually exclusive with pageid)
            pageid: Page ID (mutually exclusive with title)
            original_title: Original title of the page if redirected
        """
        if title is not None:
            self.title: str = title
            self.original_title: str = original_title or title
        elif pageid is not None:
            self.pageid: int = pageid
        else:
            raise ValueError("Either a title or a pageid must be specified")
            
        self.request = request
    
    def __eq__(self, other: object) -> bool:
        """Check if two Wikipedia pages are equal"""
        if not isinstance(other, BaseWikipediaPage):
            return NotImplemented
        try:
            return (
                self.pageid == other.pageid
                and self.title == other.title
                and self.url == other.url
            )
        except Exception:
            return False
    
    @property
    def _title_query_param(self) -> Dict[str, Union[str, int]]:
        """Get the title or pageid query parameter for API requests"""
        if hasattr(self, "title"):
            return {"titles": self.title}
        else:
            return {"pageids": self.pageid}
    
    @abstractmethod
    def __repr__(self) -> str:
        """String representation of the page"""
        pass
    
    # Helper methods for query parameter construction
    def _build_extracts_params(self, sentences: Optional[int], chars: Optional[int]) -> Dict[str, Union[str, int]]:
        """Build parameters for extracts (summary/content)"""
        params: Dict[str, Union[str, int]] = {
            "prop": "extracts",
            "explaintext": "",
        }
        params.update(self._title_query_param)
        
        if sentences:
            params["exsentences"] = sentences
        elif chars:
            params["exchars"] = chars
        else:
            params["exintro"] = ""
            
        return params
    
    def _build_parse_params(self) -> Dict[str, Union[str, int]]:
        """Build parameters for page parsing"""
        params: Dict[str, Union[str, int]] = {
            "action": "parse",
            "prop": "sections",
        }
        
        if hasattr(self, "title"):
            params.update({"page": self.title})
        else:
            params.update({"pageid": self.pageid})
            
        return params
    
    def _build_links_params(self, namespace: int, limit: str) -> Dict[str, Any]:
        """Build parameters for retrieving page links"""
        params = {
            "prop": "links",
            "plnamespace": namespace,
            "pllimit": limit,
        }
        params.update(self._title_query_param)
        return params
    
    def _build_categories_params(self, limit: str) -> Dict[str, Any]:
        """Build parameters for retrieving page categories"""
        params = {
            "prop": "categories",
            "cllimit": limit,
        }
        params.update(self._title_query_param)
        return params
    
    def _build_images_params(self, limit: str) -> Dict[str, Any]:
        """Build parameters for retrieving page images"""
        params = {
            "generator": "images",
            "gimlimit": limit,
            "prop": "imageinfo",
            "iiprop": "url",
        }
        params.update(self._title_query_param)
        return params
    
    def _build_coordinates_params(self, limit: str) -> Dict[str, Any]:
        """Build parameters for retrieving page coordinates"""
        params = {
            "prop": "coordinates",
            "colimit": limit,
        }
        params.update(self._title_query_param)
        return params
    
    def _build_references_params(self, limit: str) -> Dict[str, Any]:
        """Build parameters for retrieving page references"""
        params = {
            "prop": "extlinks",
            "ellimit": limit,
        }
        params.update(self._title_query_param)
        return params
    
    def _build_langlinks_params(self, lang_code: str) -> Dict[str, Any]:
        """Build parameters for retrieving language links"""
        params = {
            "prop": "langlinks",
            "llurl": True,
            "lllang": lang_code,
        }
        params.update(self._title_query_param)
        return params
    
    # Common helper method for section extraction
    def _extract_section_text(self, content: str, section_title: str) -> Optional[str]:
        """Extract section text from page content"""
        section = f"== {section_title} =="
        try:
            index = content.index(section) + len(section)
        except ValueError:
            return None

        try:
            next_index = content.index("==", index)
        except ValueError:
            next_index = len(content)

        return content[index:next_index].lstrip("=").strip()
    
    # Abstract methods to be implemented by derived classes
    @abstractmethod
    def html(self) -> Any:
        """
        Get full page HTML.
        
        Returns:
            Full HTML content of the page
        """
        pass
    
    @abstractmethod
    def section(self, section_title: str) -> Optional[str]:
        """
        Get the plain text content of a section from the page.
        
        Args:
            section_title: Title of the section to retrieve
            
        Returns:
            Content of the section or None if not found
        """
        pass
    
    @abstractmethod
    def lang_title(self, lang_code: str) -> Optional[str]:
        """
        Get the title of this page in a different language.
        
        Args:
            lang_code: Language code to get title for
            
        Returns:
            Title in the requested language or None if not available
        """
        pass