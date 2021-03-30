import pytest
import socketio


class MockWebSocketConnection:
    """Class simulating one-to-one websocket connection"""

    def __init__(self):
        self.clients_events_to_funcs = {}
        self.servers_events_to_funcs = {}

    def _from_server(self, name, data=None):
        if name in self.clients_events_to_funcs:
            if data:
                self.clients_events_to_funcs[name](data)
            else:
                self.clients_events_to_funcs[name]()

    def _from_client(self, name, data=None):
        if name in self.servers_events_to_funcs:
            if data:
                self.servers_events_to_funcs[name](data)
            else:
                self.servers_events_to_funcs[name]()

    def _connect(self):
        for d in (self.servers_events_to_funcs, self.clients_events_to_funcs):
            if 'connect' in d:
                d['connect']()

    def _disconnect(self):
        for d in (self.servers_events_to_funcs, self.clients_events_to_funcs):
            if 'disconnect' in d:
                d['disconnect']()

class _OnDecorator:
    """Functor definig decorator "on" in MockClient, MockServer"""

    def __init__(self, d: dict, name: str):
        self.d = d
        self.name = name

    def __call__(self, target):
        self.d[self.name] = target

class MockClient:
    """Class mocking socketio.Client"""

    def __init__(self, parent: MockWebSocketConnection):
        self.parent = parent

    # decorators
    def event(self, target):
        self.parent.clients_events_to_funcs[target.__name__] = target

    def on(self, name):
        return _OnDecorator(self.parent.clients_events_to_funcs, name)

    # mocked methods
    def connect(self, server):
        self.parent._connect()

    def wait(self):
        pass

    def emit(self, name, data=None):
        self.parent._from_client(name, data)

    def _close_connection(self):
        self.parent._disconnect()


class MockServer:
    """Class mimicking socketio server"""

    def __init__(self, parent: MockWebSocketConnection):
        self.parent = parent

    def event(self, target):
        self.parent.servers_events_to_funcs[target.__name__] = target

    def on(self, name):
        return _OnDecorator(self.parent.servers_events_to_funcs, name)

    def emit(self, name, data=None):
        self.parent._from_server(name, data)


@pytest.fixture
def client_server(monkeypatch):
    websocket_connection = MockWebSocketConnection()
    client = MockClient(websocket_connection)
    server = MockServer(websocket_connection)

    monkeypatch.setattr(socketio, 'Client', lambda: client)

    yield (client, server)

    client._close_connection()

@pytest.fixture
def client_server_with_gathered_logs(client_server):
    client, server = client_server

    class LogGatherer:
        def __init__(self):
            self.logs = []

        def __call__(self, log):
            self.logs.append(log)

        def messages(self):
            return (log.msg for log in self.logs)

        def messages_from(self, name):
            return (log.msg for log in self.logs if log.name == name)

    log_gatherer = LogGatherer()
    server.on('log')(log_gatherer)

    return (client, server, log_gatherer)
