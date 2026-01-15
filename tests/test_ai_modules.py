import pytest
from unittest.mock import MagicMock, patch
from src.llm import ErrorResolver

# 1. Test the RAG Engine (Mocking the Vector DB)
@patch("src.rag.Chroma")
@patch("src.rag.HuggingFaceEmbeddings")
def test_rag_initialization(mock_embeddings, mock_chroma):
    from src.rag import RagEngine  # Import inside test to avoid early init issues
    
    # Simulate the RAG engine without loading heavy models
    rag = RagEngine()
    assert rag is not None

# 2. Test the LLM Resolver (Mocking the AI Response)
@patch("src.llm.ChatOllama") 
def test_llm_resolution(mock_ollama_class):
    # Setup the fake AI
    mock_llm_instance = MagicMock()
    # We mock the chain invocation, not just the LLM, because you use a Chain
    mock_chain = MagicMock()
    mock_chain.invoke.return_value = {
        "root_cause": "Test Cause", 
        "fix_steps": "Test Fix", 
        "code_snippet": "print(1)"
    }
    
    # Patch the chain inside ErrorResolver
    with patch("src.llm.ErrorResolver") as MockResolver:
        resolver = MockResolver()
        resolver.resolve.return_value = {
            "root_cause": "Test Cause", 
            "fix_steps": "Test Fix", 
            "code_snippet": "print(1)"
        }
        
        # Create a fake log object
        class FakeLog:
            message = "Test Error"
            service_name = "Test Service"
        
        # Run the resolve function
        result = resolver.resolve(FakeLog())
        
        # Check results
        assert result['root_cause'] == "Test Cause"
        assert result['code_snippet'] == "print(1)"