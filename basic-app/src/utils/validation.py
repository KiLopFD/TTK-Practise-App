from ttkbootstrap.validation import validator, add_validation, ValidationEvent

class ValidationUtils:
    check_state = False
    @staticmethod
    def validate_nullable(entry):
        @validator
        def check_name(event: ValidationEvent):
            if len(event.postchangetext) == 0:
                ValidationUtils.check_state = False
                return False
            ValidationUtils.check_state = True
            return True
        add_validation(entry, check_name)
