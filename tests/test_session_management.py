"""
Tests for session management functionality in MediaWikiAPI.
"""

import pytest
from unittest.mock import patch, MagicMock

from mediawikiapi.sync.mediawikiapi import MediaWikiAPI
from mediawikiapi.sync.requestsession import RequestSession
from mediawikiapi.async_api.async_mediawikiapi import AsyncMediaWikiAPI
from mediawikiapi.async_api.async_requestsession import AsyncRequestSession


class TestSessionManagement:
    """Test session management features"""
    
    def test_sync_context_manager(self):
        """Test that synchronous RequestSession works as a context manager"""
        with patch('requests.Session.close') as mock_close:
            with RequestSession() as session:
                # Session should be created but not closed yet
                assert mock_close.call_count == 0
            # Session should be closed after exiting the context
            assert mock_close.call_count == 1
    
    def test_sync_mediawiki_context_manager(self):
        """Test that MediaWikiAPI works as a context manager"""
        with patch('mediawikiapi.sync.requestsession.RequestSession.close') as mock_close:
            with MediaWikiAPI() as api:
                # Session should be created but not closed yet
                assert mock_close.call_count == 0
            # Session should be closed after exiting the context
            assert mock_close.call_count == 1
    
    def test_sync_explicit_close(self):
        """Test explicit closing of MediaWikiAPI"""
        with patch('mediawikiapi.sync.requestsession.RequestSession.close') as mock_close:
            api = MediaWikiAPI()
            assert mock_close.call_count == 0
            api.close()
            assert mock_close.call_count == 1
    
    def test_sync_new_session(self):
        """Test creating a new session in MediaWikiAPI"""
        with patch('mediawikiapi.sync.requestsession.RequestSession.close') as mock_close:
            api = MediaWikiAPI()
            original_session = api.session
            api.new_session()
            assert mock_close.call_count == 1
            assert api.session is not original_session
    
    @pytest.mark.asyncio
    async def test_async_context_manager(self):
        """Test that asynchronous RequestSession works as a context manager"""
        with patch('aiohttp.ClientSession.close') as mock_close:
            mock_close.return_value = MagicMock()
            # Make the mock return a coroutine-compatible object
            mock_close.return_value.__await__ = lambda: (yield from [])
            
            async with AsyncRequestSession() as session:
                # Session should be created but not closed yet
                assert mock_close.call_count == 0
            # Session should be closed after exiting the context
            assert mock_close.call_count >= 1
    
    @pytest.mark.asyncio
    async def test_async_mediawiki_context_manager(self):
        """Test that AsyncMediaWikiAPI works as a context manager"""
        with patch('mediawikiapi.async_api.async_requestsession.AsyncRequestSession.close') as mock_close:
            mock_close.return_value = MagicMock()
            # Make the mock return a coroutine-compatible object
            mock_close.return_value.__await__ = lambda: (yield from [])
            
            async with AsyncMediaWikiAPI() as api:
                # Session should be created but not closed yet
                assert mock_close.call_count == 0
            # Session should be closed after exiting the context
            assert mock_close.call_count == 1
    
    @pytest.mark.asyncio
    async def test_async_explicit_close(self):
        """Test explicit closing of AsyncMediaWikiAPI"""
        with patch('mediawikiapi.async_api.async_requestsession.AsyncRequestSession.close') as mock_close:
            mock_close.return_value = MagicMock()
            # Make the mock return a coroutine-compatible object
            mock_close.return_value.__await__ = lambda: (yield from [])
            
            api = AsyncMediaWikiAPI()
            assert mock_close.call_count == 0
            await api.close()
            assert mock_close.call_count == 1


    def test_sync_session_reuse_policy(self):
        """Test session reuse policy for synchronous RequestSession"""
        session = RequestSession()
        assert session.increment_reuse_counter() == 1
        assert session.increment_reuse_counter() == 2
        
        # Set a lower limit and check it refreshes
        session.set_max_reuse_count(5)
        assert session.should_refresh_session() == False
        
        # Increment to reach the limit
        for _ in range(3):
            session.increment_reuse_counter()
            
        # Should now indicate refresh needed
        assert session.should_refresh_session() == True
    
    def test_sync_session_reuse_in_request(self):
        """Test that session is refreshed during requests when limit is reached"""
        with patch('mediawikiapi.sync.requestsession.RequestSession.new_session') as mock_new_session:
            session = RequestSession()
            session.set_max_reuse_count(3)
            
            # Configure the session.get method to be callable without making real requests
            session.session.get = MagicMock()
            response_mock = MagicMock()
            response_mock.status_code = 200
            response_mock.raise_for_status = MagicMock()
            response_mock.json = MagicMock(return_value={})
            session.session.get.return_value = response_mock
            
            # First 3 requests should not trigger new_session
            for _ in range(3):
                session.request({}, MagicMock())
                
            assert mock_new_session.call_count == 0
            
            # Fourth request should trigger new_session
            session.request({}, MagicMock())
            assert mock_new_session.call_count == 1
    
    @pytest.mark.asyncio
    async def test_async_session_reuse_policy(self):
        """Test session reuse policy for asynchronous RequestSession"""
        session = AsyncRequestSession()
        assert session.increment_reuse_counter() == 1
        assert session.increment_reuse_counter() == 2
        
        # Set a lower limit and check it refreshes
        session.set_max_reuse_count(5)
        assert session.should_refresh_session() == False
        
        # Increment to reach the limit
        for _ in range(3):
            session.increment_reuse_counter()
            
        # Should now indicate refresh needed
        assert session.should_refresh_session() == True
        
        # Clean up
        await session.close()
        

if __name__ == "__main__":
    pytest.main()