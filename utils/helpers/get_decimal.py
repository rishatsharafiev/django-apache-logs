from decimal import Decimal, InvalidOperation


def get_decimal(entity, key, default=None):
    """Get decimal or default value"""
    try:
        return Decimal(entity.get(key))
    except (InvalidOperation, TypeError):
        return default
