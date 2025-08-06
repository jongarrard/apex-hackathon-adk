def myTool(message: str = "Hello World") -> str:
    """
    A simple greeting tool that returns a customizable message.
    
    Args:
        message (str): The message to return. Defaults to "Hello World".
    
    Returns:
        str: The greeting message.
    """
    return f"🤖 Tool says: {message}"


def get_current_time() -> str:
    """
    Get the current date and time.
    
    Returns:
        str: Current date and time in a readable format.
    """
    import datetime
    now = datetime.datetime.now()
    return f"Current time: {now.strftime('%Y-%m-%d %H:%M:%S')}"


def calculate(expression: str) -> str:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression (str): Mathematical expression to evaluate (e.g., "2 + 2", "10 * 5")
    
    Returns:
        str: Result of the calculation or error message.
    """
    try:
        # Only allow safe mathematical operations
        allowed_chars = set('0123456789+-*/.() ')
        if not all(c in allowed_chars for c in expression):
            return "Error: Only basic mathematical operations are allowed"
        
        result = eval(expression)
        return f"Result: {expression} = {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"