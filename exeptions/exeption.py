class QueryNotFoundError(Exception):
    """Exception raised when a query is not found"""
    def __init__(self, query_name: str):
        self.query_name = query_name
        super().__init__(f"Query '{query_name}' not found")