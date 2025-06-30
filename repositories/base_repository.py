from logging import getLogger


class BaseRepository:
    """Base repository class with common functionality for all repositories"""
    logger = getLogger(__name__)
    
    def _update_fields(self, target_object, source_object, exclude_fields=None):
        """
        Utility method to update only non-None fields from source to target object
        
        Args:
            target_object: Object to be updated (from database)
            source_object: Object with new values
            exclude_fields: List of field names to exclude from update (e.g., ['id', 'created_at'])
        """
        if exclude_fields is None:
            exclude_fields = ['id', 'created_at', 'deleted_at']
        
        updated_fields = []
        
        # Get only the model fields from SQLModel, not all attributes
        if hasattr(source_object, '__fields__'):
            # For Pydantic v1 (older versions)
            model_fields = source_object.__fields__.keys()
        elif hasattr(source_object, 'model_fields'):
            # For Pydantic v2 (newer versions)
            model_fields = source_object.model_fields.keys()
        else:
            # Fallback to manual field detection
            model_fields = [attr for attr in dir(source_object) 
                          if not attr.startswith('_') 
                          and not callable(getattr(source_object, attr))
                          and attr not in ['metadata', 'registry']]
        
        # Iterate only through actual model fields
        for field_name in model_fields:
            # Skip excluded fields
            if field_name in exclude_fields:
                continue
                
            # Get the value from source object
            field_value = getattr(source_object, field_name, None)
            
            # Only update if the value is not None and the target has this attribute
            if field_value is not None and hasattr(target_object, field_name):
                setattr(target_object, field_name, field_value)
                updated_fields.append(f"{field_name}='{field_value}'")
        
        if updated_fields:
            self.logger.info(f"Updated fields: {', '.join(updated_fields)}")
        else:
            self.logger.info("No fields were updated")

    def create_response_body(self, data: dict, message: str, status_code: int):
        return {
            "message": message,
            "data": data,
            "status_code": status_code
        }