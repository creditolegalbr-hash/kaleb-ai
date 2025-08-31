# External Integrations Framework

## Overview

The external integrations framework enables the intelligent automation system to connect with various external services and tools. This document outlines the integration architecture, supported services, and implementation patterns.

## Integration Architecture

### Core Components

1. **IntegrationManager**: Central manager for all integrations
2. **IntegrationAdapters**: Service-specific adapters
3. **ConnectionPool**: Manages connections to external services
4. **AuthenticationHandler**: Handles authentication for services
5. **RateLimiter**: Controls request rates to prevent abuse
6. **ErrorRetryHandler**: Manages retry logic for failed requests

### IntegrationManager

```python
class IntegrationManager:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.adapters = {}
        self.connection_pool = ConnectionPool()
        self.auth_handler = AuthenticationHandler()
        self.rate_limiter = RateLimiter()
        self.retry_handler = ErrorRetryHandler()
        
    def register_adapter(self, service_name: str, adapter: 'BaseAdapter'):
        """Register integration adapter"""
        self.adapters[service_name] = adapter
    
    def get_adapter(self, service_name: str) -> 'BaseAdapter':
        """Get registered adapter by service name"""
        return self.adapters.get(service_name)
    
    def execute_request(self, service_name: str, request: dict) -> dict:
        """Execute request through integration adapter"""
        adapter = self.get_adapter(service_name)
        if not adapter:
            raise ValueError(f"No adapter registered for service: {service_name}")
        
        # Check rate limits
        if not self.rate_limiter.check_limit(service_name):
            raise Exception(f"Rate limit exceeded for service: {service_name}")
        
        # Execute with retry logic
        return self.retry_handler.execute_with_retry(
            lambda: adapter.execute(request)
        )
```

### BaseAdapter

```python
class BaseAdapter:
    def __init__(self, config: dict):
        self.config = config
        self.service_name = config.get('service_name')
        self.base_url = config.get('base_url')
        self.auth_type = config.get('auth_type', 'none')
        
    def execute(self, request: dict) -> dict:
        """Execute request to external service"""
        raise NotImplementedError("Must be implemented by subclass")
    
    def _prepare_request(self, request: dict) -> dict:
        """Prepare request with authentication and headers"""
        # Add authentication
        auth_headers = self._get_auth_headers()
        request['headers'].update(auth_headers)
        
        # Add default headers
        request['headers']['User-Agent'] = 'IntelligentAutomation/1.0'
        
        return request
    
    def _get_auth_headers(self) -> dict:
        """Get authentication headers"""
        if self.auth_type == 'api_key':
            return {'Authorization': f'Bearer {self.config["api_key"]}'}
        elif self.auth_type == 'basic':
            # Implement basic auth
            pass
        return {}
    
    def _handle_response(self, response: dict) -> dict:
        """Handle and process response"""
        if response.get('status_code') >= 400:
            raise Exception(f"Request failed: {response.get('error')}")
        return response.get('data', {})
```

## Supported Integrations

### 1. Google Calendar Integration

#### Adapter Implementation

```python
class GoogleCalendarAdapter(BaseAdapter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.service_name = 'google_calendar'
        self.scopes = ['https://www.googleapis.com/auth/calendar']
        
    def create_event(self, event_data: dict) -> dict:
        """Create calendar event"""
        request = {
            'method': 'POST',
            'url': f'{self.base_url}/calendars/primary/events',
            'headers': {},
            'data': event_data
        }
        return self.execute(request)
    
    def list_events(self, time_min: str, time_max: str) -> dict:
        """List calendar events"""
        request = {
            'method': 'GET',
            'url': f'{self.base_url}/calendars/primary/events',
            'headers': {},
            'params': {
                'timeMin': time_min,
                'timeMax': time_max
            }
        }
        return self.execute(request)
    
    def check_availability(self, time_slot: dict) -> bool:
        """Check if time slot is available"""
        events = self.list_events(time_slot['start'], time_slot['end'])
        return len(events.get('items', [])) == 0
```

#### Configuration

```yaml
# google_calendar_config.yaml
google_calendar:
  service_name: "google_calendar"
  base_url: "https://www.googleapis.com/calendar/v3"
  auth_type: "oauth2"
  client_id: "your_client_id"
  client_secret: "your_client_secret"
  redirect_uri: "http://localhost:8080/callback"
  scopes:
    - "https://www.googleapis.com/auth/calendar"
```

### 2. Email Service Integration

#### Adapter Implementation

```python
class EmailAdapter(BaseAdapter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.service_name = 'email'
        
    def send_email(self, email_data: dict) -> dict:
        """Send email"""
        request = {
            'method': 'POST',
            'url': f'{self.base_url}/send',
            'headers': {'Content-Type': 'application/json'},
            'data': email_data
        }
        return self.execute(request)
    
    def receive_emails(self, folder: str = 'inbox') -> dict:
        """Receive emails from specified folder"""
        request = {
            'method': 'GET',
            'url': f'{self.base_url}/messages',
            'headers': {},
            'params': {'folder': folder}
        }
        return self.execute(request)
```

#### Configuration

```yaml
# email_config.yaml
email:
  service_name: "email"
  base_url: "https://api.emailservice.com/v1"
  auth_type: "api_key"
  api_key: "your_api_key"
```

### 3. Database Integration

#### Adapter Implementation

```python
class DatabaseAdapter(BaseAdapter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.service_name = 'database'
        self.connection = None
        self._connect()
        
    def _connect(self):
        """Establish database connection"""
        # Implementation depends on database type
        pass
    
    def execute_query(self, query: str, params: dict = None) -> dict:
        """Execute database query"""
        # Execute query and return results
        pass
    
    def insert_record(self, table: str, data: dict) -> dict:
        """Insert record into table"""
        # Insert data into specified table
        pass
    
    def update_record(self, table: str, where: dict, data: dict) -> dict:
        """Update record in table"""
        # Update data in specified table
        pass
```

#### Configuration

```yaml
# database_config.yaml
database:
  service_name: "database"
  type: "postgresql"
  host: "localhost"
  port: 5432
  database: "automation_db"
  username: "user"
  password: "password"
```

### 4. File Storage Integration

#### Adapter Implementation

```python
class FileStorageAdapter(BaseAdapter):
    def __init__(self, config: dict):
        super().__init__(config)
        self.service_name = 'file_storage'
        
    def upload_file(self, file_path: str, destination: str) -> dict:
        """Upload file to storage"""
        # Implementation for file upload
        pass
    
    def download_file(self, file_id: str, destination: str) -> dict:
        """Download file from storage"""
        # Implementation for file download
        pass
    
    def list_files(self, folder: str) -> dict:
        """List files in folder"""
        # Implementation for listing files
        pass
```

#### Configuration

```yaml
# file_storage_config.yaml
file_storage:
  service_name: "file_storage"
  type: "s3"
  bucket: "automation-files"
  region: "us-east-1"
  access_key: "your_access_key"
  secret_key: "your_secret_key"
```

## Integration with Agents

### SchedulerAgent Integration

```python
class SchedulerAgent(BaseAgent):
    def __init__(self):
        super().__init__("SchedulerAgent")
        self.integration_manager = IntegrationManager()
        self._setup_integrations()
    
    def _setup_integrations(self):
        """Setup required integrations"""
        # Load Google Calendar configuration
        calendar_config = self._load_config('google_calendar_config.yaml')
        calendar_adapter = GoogleCalendarAdapter(calendar_config)
        self.integration_manager.register_adapter('google_calendar', calendar_adapter)
    
    def handle(self, task: dict) -> dict:
        """Handle scheduling task with Google Calendar integration"""
        task_description = task.get('task', '')
        
        # Parse scheduling request
        schedule_request = self._parse_schedule_request(task_description)
        
        # Check availability
        is_available = self._check_availability(schedule_request['time_slot'])
        
        if is_available:
            # Create event
            event_data = self._prepare_event_data(schedule_request)
            result = self._create_event(event_data)
            return {
                'status': 'success',
                'message': f'Event scheduled: {result.get("summary")}',
                'event_id': result.get('id')
            }
        else:
            return {
                'status': 'error',
                'message': 'Time slot not available'
            }
    
    def _check_availability(self, time_slot: dict) -> bool:
        """Check availability using Google Calendar"""
        calendar_adapter = self.integration_manager.get_adapter('google_calendar')
        return calendar_adapter.check_availability(time_slot)
    
    def _create_event(self, event_data: dict) -> dict:
        """Create event using Google Calendar"""
        calendar_adapter = self.integration_manager.get_adapter('google_calendar')
        return calendar_adapter.create_event(event_data)
```

### EmailAgent Integration

```python
class EmailAgent(BaseAgent):
    def __init__(self):
        super().__init__("EmailAgent")
        self.integration_manager = IntegrationManager()
        self._setup_integrations()
    
    def _setup_integrations(self):
        """Setup required integrations"""
        # Load email configuration
        email_config = self._load_config('email_config.yaml')
        email_adapter = EmailAdapter(email_config)
        self.integration_manager.register_adapter('email', email_adapter)
    
    def handle(self, task: dict) -> dict:
        """Handle email task with email service integration"""
        task_description = task.get('task', '')
        
        # Parse email request
        email_request = self._parse_email_request(task_description)
        
        # Send email
        result = self._send_email(email_request)
        
        return {
            'status': 'success',
            'message': f'Email sent to {result.get("recipient")}',
            'email_id': result.get('id')
        }
    
    def _send_email(self, email_data: dict) -> dict:
        """Send email using email service"""
        email_adapter = self.integration_manager.get_adapter('email')
        return email_adapter.send_email(email_data)
```

## Error Handling and Retry Logic

### ErrorRetryHandler

```python
class ErrorRetryHandler:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 1.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute_with_retry(self, func: callable) -> dict:
        """Execute function with retry logic"""
        last_exception = None
        
        for attempt in range(self.max_retries + 1):
            try:
                return func()
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    # Calculate backoff delay
                    delay = self.backoff_factor * (2 ** attempt)
                    time.sleep(delay)
                else:
                    # Max retries exceeded
                    raise Exception(f"Max retries exceeded. Last error: {str(e)}")
        
        raise last_exception
```

### RateLimiter

```python
class RateLimiter:
    def __init__(self):
        self.limits = {}  # Service limits
        self.requests = {}  # Request tracking
    
    def check_limit(self, service_name: str) -> bool:
        """Check if service is within rate limits"""
        if service_name not in self.limits:
            return True  # No limit set
        
        limit = self.limits[service_name]
        current_time = time.time()
        
        # Clean up old requests
        self._cleanup_old_requests(service_name, current_time)
        
        # Check if within limit
        request_count = len(self.requests.get(service_name, []))
        return request_count < limit['requests_per_window']
    
    def _cleanup_old_requests(self, service_name: str, current_time: float):
        """Remove requests outside the time window"""
        if service_name in self.requests:
            window = self.limits[service_name]['window_seconds']
            self.requests[service_name] = [
                req_time for req_time in self.requests[service_name]
                if current_time - req_time < window
            ]
```

## Configuration Management

### Integration Configuration

```yaml
# integrations_config.yaml
integrations:
  google_calendar:
    enabled: true
    max_rate_limit: 100  # requests per 100 seconds
    retry_attempts: 3
    
  email:
    enabled: true
    max_rate_limit: 50
    retry_attempts: 2
    
  database:
    enabled: true
    max_connections: 10
    retry_attempts: 3
    
  file_storage:
    enabled: true
    max_rate_limit: 200
    retry_attempts: 3
```

## Security Considerations

### Credential Management

1. **Environment Variables**: Store sensitive credentials in environment variables
2. **Encrypted Storage**: Encrypt configuration files containing credentials
3. **Access Control**: Limit access to configuration files
4. **Rotation**: Implement credential rotation mechanisms

### Secure Configuration Loading

```python
class SecureConfigLoader:
    def __init__(self):
        self.encryption_key = os.getenv('CONFIG_ENCRYPTION_KEY')
    
    def load_config(self, config_path: str) -> dict:
        """Load and decrypt configuration file"""
        # Load encrypted config file
        # Decrypt using encryption key
        # Return decrypted configuration
        pass
```

## Usage Examples

### Setting Up Integrations

```python
# Initialize integration manager
integration_manager = IntegrationManager()

# Register adapters
calendar_config = load_config('google_calendar_config.yaml')
calendar_adapter = GoogleCalendarAdapter(calendar_config)
integration_manager.register_adapter('google_calendar', calendar_adapter)

email_config = load_config('email_config.yaml')
email_adapter = EmailAdapter(email_config)
integration_manager.register_adapter('email', email_adapter)
```

### Using Integrations in Agents

```python
# In SchedulerAgent
def schedule_meeting(self, meeting_details: dict) -> dict:
    # Check availability
    is_available = self.integration_manager.execute_request(
        'google_calendar',
        {
            'method': 'check_availability',
            'data': meeting_details['time_slot']
        }
    )
    
    if is_available:
        # Create event
        result = self.integration_manager.execute_request(
            'google_calendar',
            {
                'method': 'create_event',
                'data': self._prepare_event_data(meeting_details)
            }
        )
        return result
```

## Benefits

1. **Modularity**: Easy to add new integrations
2. **Consistency**: Standardized interface for all integrations
3. **Reliability**: Built-in error handling and retry logic
4. **Performance**: Connection pooling and rate limiting
5. **Security**: Secure credential management
6. **Scalability**: Configurable limits and resource management
7. **Maintainability**: Clear separation of concerns