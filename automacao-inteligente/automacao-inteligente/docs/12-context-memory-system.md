# Context and Memory Management System

## Overview

The context and memory management system is a critical component for creating intelligent agents that can maintain state, learn from interactions, and provide personalized responses. This system will enable agents to remember past interactions, maintain conversation context, and build a knowledge base over time.

## System Architecture

### Core Components

1. **ContextManager**: Manages conversation context and session state
2. **MemoryStore**: Persistent storage for long-term memory
3. **ContextSerializer**: Serializes/deserializes context for storage
4. **MemoryIndexer**: Indexes memory for fast retrieval
5. **RAGInterface**: Interface to Retrieval-Augmented Generation system

### ContextManager

```python
class ContextManager:
    def __init__(self, max_history: int = 100):
        self.max_history = max_history
        self.sessions = {}  # Session storage
        self.current_session_id = None
    
    def create_session(self, session_id: str = None) -> str:
        """Create a new session"""
        if not session_id:
            session_id = self._generate_session_id()
        
        self.sessions[session_id] = {
            'context': {},
            'history': [],
            'created_at': datetime.now(),
            'last_accessed': datetime.now()
        }
        
        self.current_session_id = session_id
        return session_id
    
    def update_context(self, key: str, value: any, session_id: str = None):
        """Update context with new information"""
        session = self._get_session(session_id)
        session['context'][key] = value
        session['last_accessed'] = datetime.now()
    
    def add_to_history(self, interaction: dict, session_id: str = None):
        """Add interaction to conversation history"""
        session = self._get_session(session_id)
        session['history'].append(interaction)
        
        # Maintain history size limit
        if len(session['history']) > self.max_history:
            session['history'] = session['history'][-self.max_history:]
        
        session['last_accessed'] = datetime.now()
    
    def get_context(self, session_id: str = None) -> dict:
        """Retrieve current context"""
        session = self._get_session(session_id)
        return session['context'].copy()
    
    def get_history(self, session_id: str = None) -> list:
        """Retrieve conversation history"""
        session = self._get_session(session_id)
        return session['history'].copy()
    
    def _get_session(self, session_id: str = None) -> dict:
        """Get session by ID or current session"""
        sid = session_id or self.current_session_id
        if not sid or sid not in self.sessions:
            raise ValueError(f"Session {sid} not found")
        return self.sessions[sid]
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"session_{int(datetime.now().timestamp() * 1000000)}"
```

### MemoryStore

```python
class MemoryStore:
    def __init__(self, storage_path: str = "memory.db"):
        self.storage_path = storage_path
        self.connection = None
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage database"""
        # Implementation for SQLite or other storage
        pass
    
    def store_memory(self, memory_item: dict) -> str:
        """Store memory item and return ID"""
        # Store memory item in database
        # Return unique ID for the stored item
        pass
    
    def retrieve_memory(self, query: dict, limit: int = 10) -> list:
        """Retrieve memory items matching query"""
        # Query memory database
        # Return matching items
        pass
    
    def update_memory(self, memory_id: str, updates: dict):
        """Update existing memory item"""
        # Update memory item in database
        pass
    
    def delete_memory(self, memory_id: str):
        """Delete memory item"""
        # Delete memory item from database
        pass
```

### MemoryIndexer

```python
class MemoryIndexer:
    def __init__(self, memory_store: MemoryStore):
        self.memory_store = memory_store
        self.index = {}  # In-memory index for fast access
    
    def index_memory(self, memory_item: dict):
        """Index memory item for fast retrieval"""
        # Extract keywords and metadata
        # Update index structures
        pass
    
    def search(self, query: str, limit: int = 10) -> list:
        """Search memory using indexed terms"""
        # Search index for matching items
        # Return ranked results
        pass
    
    def get_related_memories(self, memory_id: str) -> list:
        """Find memories related to specified memory"""
        # Find semantically related memories
        pass
```

## Integration with Agents

### BaseAgent Enhancement

```python
class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.context_manager = ContextManager()
        self.memory_store = MemoryStore()
        self.memory_indexer = MemoryIndexer(self.memory_store)
        self.rag_interface = RAGInterface()
    
    def handle(self, task: dict) -> dict:
        """Enhanced handle method with context and memory"""
        # Get current context
        context = self.context_manager.get_context()
        
        # Add current task to history
        interaction = {
            'task': task,
            'timestamp': datetime.now(),
            'agent': self.name
        }
        self.context_manager.add_to_history(interaction)
        
        # Check memory for relevant information
        relevant_memories = self._retrieve_relevant_memories(task)
        
        # Process task with context and memories
        result = self._process_with_context(task, context, relevant_memories)
        
        # Store result in memory
        self._store_memory(task, result, context)
        
        # Update context with result
        self.context_manager.update_context(f"last_{self.name}_result", result)
        
        return result
    
    def _retrieve_relevant_memories(self, task: dict) -> list:
        """Retrieve relevant memories for task"""
        # Use RAG to find relevant memories
        query_text = task.get('task', '')
        return self.rag_interface.search(query_text)
    
    def _process_with_context(self, task: dict, context: dict, memories: list) -> dict:
        """Process task using context and memories"""
        # Implementation specific to each agent
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")
    
    def _store_memory(self, task: dict, result: dict, context: dict):
        """Store interaction in memory"""
        memory_item = {
            'agent': self.name,
            'task': task,
            'result': result,
            'context': context,
            'timestamp': datetime.now(),
            'session_id': self.context_manager.current_session_id
        }
        
        memory_id = self.memory_store.store_memory(memory_item)
        self.memory_indexer.index_memory(memory_item)
```

## Memory Types

### 1. Episodic Memory
- Stores specific events and interactions
- Time-stamped experiences
- Conversation history

### 2. Semantic Memory
- General knowledge and facts
- Learned information
- Domain-specific knowledge

### 3. Procedural Memory
- Skills and processes
- How to perform tasks
- Workflow knowledge

### 4. Working Memory
- Current context and state
- Temporary information
- Active conversation context

## RAG Integration

### Retrieval Process

1. **Query Analysis**: Analyze incoming task for key concepts
2. **Memory Search**: Search indexed memories for relevant items
3. **Relevance Ranking**: Rank memories by relevance to query
4. **Context Assembly**: Assemble relevant memories into context
5. **Response Generation**: Generate response using context

### Implementation

```python
class RAGInterface:
    def __init__(self, memory_indexer: MemoryIndexer):
        self.memory_indexer = memory_indexer
        # Initialize embedding model
        # Initialize similarity functions
    
    def search(self, query: str, limit: int = 5) -> list:
        """Search for relevant memories using RAG"""
        # Convert query to embeddings
        # Search memory index
        # Rank results by similarity
        # Return most relevant memories
        pass
    
    def generate_context(self, query: str, memories: list) -> str:
        """Generate context string from relevant memories"""
        # Format memories into context string
        # Prioritize most relevant items
        pass
```

## Configuration

### Memory Configuration

```yaml
# memory_config.yaml
memory:
  context_manager:
    max_history: 100
    session_timeout: 3600  # 1 hour
  memory_store:
    type: "sqlite"
    path: "memory.db"
    max_size: 1000000  # 1GB
  indexing:
    enabled: true
    update_frequency: 300  # 5 minutes
  rag:
    model: "sentence-transformers/all-MiniLM-L6-v2"
    similarity_threshold: 0.7
    max_context_length: 2000
```

## Usage Examples

### Basic Context Management

```python
# Create context manager
context_manager = ContextManager(max_history=50)

# Create session
session_id = context_manager.create_session()

# Update context
context_manager.update_context("user_name", "John Doe")
context_manager.update_context("company", "Tech Corp")

# Add to history
interaction = {
    "input": "What is the status of my invoice?",
    "output": "Your invoice #12345 is pending approval.",
    "timestamp": datetime.now()
}
context_manager.add_to_history(interaction)
```

### Memory Storage and Retrieval

```python
# Store memory
memory_store = MemoryStore("memory.db")
memory_item = {
    "type": "interaction",
    "content": "User asked about invoice status",
    "tags": ["invoice", "status", "billing"],
    "timestamp": datetime.now()
}
memory_id = memory_store.store_memory(memory_item)

# Retrieve memory
relevant_memories = memory_store.retrieve_memory(
    {"tags": ["invoice"]}, 
    limit=10
)
```

### Agent with Memory

```python
class EnhancedEmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EnhancedEmailAgent")
    
    def _process_with_context(self, task: dict, context: dict, memories: list) -> dict:
        # Use memories to enhance response
        memory_context = "\n".join([
            f"Previous interaction: {mem['content']}" 
            for mem in memories[:3]  # Use top 3 memories
        ])
        
        # Generate response using context
        response = f"Processing email with context:\n{memory_context}"
        
        return {
            "response": response,
            "memories_used": len(memories[:3]),
            "context_keys": list(context.keys())
        }
```

## Benefits

1. **Personalization**: Agents can remember user preferences and history
2. **Context Awareness**: Maintain conversation context across interactions
3. **Knowledge Building**: Accumulate knowledge over time
4. **Improved Responses**: Use past experiences to enhance responses
5. **Learning Capability**: System can learn from interactions
6. **Scalability**: Efficient storage and retrieval of memories